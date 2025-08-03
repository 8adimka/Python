from pathlib import Path

import numpy as np
import pandas as pd

# 📁 Путь к файлу
BASE_DIR = Path(__file__).resolve().parent
df = pd.read_feather(BASE_DIR / "test.feather")

errors = set()
converted = {}

# 🔄 Преобразуем все object-колонки в числовые, если можно
for col in df.columns:
    converted[col] = pd.to_numeric(df[col], errors="coerce")
    if df[col].dtype == object and not df[col].equals(converted[col]):
        errors.add(f"📛 Column '{col}' contains non-numeric values (should be float)")

# 📉 1. Отрицательные значения (только там, где не должны быть)
price_columns = [col for col in df.columns if "px" in col or "trade_px" in col]
amount_columns = [col for col in df.columns if "amt" in col or "trade_amt" in col]

for col in price_columns:
    if (converted[col] < 0).any():
        errors.add(f"📉 Negative price values found in column '{col}'")

for col in amount_columns:
    if (converted[col] < 0).any():
        errors.add(f"📉 Negative amount values found in column '{col}'")

# 📈 2. Временные ошибки
for time_col in ["exchHostTime", "adapterTime"]:
    # Проверка монотонности
    if not converted[time_col].is_monotonic_increasing:
        errors.add(f"📈 {time_col} is not monotonically increasing")
    # Проверка нулевых и отрицательных таймстампов
    if (converted[time_col] <= 0).any():
        errors.add(f"📈 {time_col} contains zero or negative timestamps")
    # Проверка больших скачков времени (превышение среднего + 5 std)
    diffs = converted[time_col].diff().dropna()
    threshold = diffs.mean() + 5 * diffs.std()
    if (diffs > threshold).any():
        errors.add(f"📈 {time_col} has suspiciously large time gaps")
    # Проверка повторяющихся временных меток подряд
    repeats = converted[time_col] == converted[time_col].shift()
    if repeats.mean() > 0.9:
        errors.add(f"♻️ {time_col} repeats in >90% of rows (possible feed freeze)")
    # Проверка на будущие таймстампы (например, > текущей даты)
    current_time = pd.Timestamp.now().timestamp() * 1e9  # в наносекундах
    if (converted[time_col] > current_time).any():
        errors.add(f"📈 {time_col} contains future timestamps")

# ⏳ 2.1 adapterTime < exchHostTime и большие отклонения
if {"adapterTime", "exchHostTime"}.issubset(converted.keys()):
    time_diff = converted["adapterTime"] - converted["exchHostTime"]
    if (time_diff < 0).any():
        errors.add("⏳ adapterTime is earlier than exchHostTime")
    if (time_diff.abs() > 10_000_000_000).any():  # 10 секунд в наносекундах
        errors.add("⏳ adapterTime deviates from exchHostTime by more than 10 seconds")

# 🧩 3. Дубли
if df.duplicated(subset=["msgSeqNum"]).any():
    errors.add("🧩 Duplicate msgSeqNum values found")
if df.duplicated().any():
    errors.add("🧩 Completely duplicated rows found")
if df.duplicated(subset=["msgSeqNum", "exchHostTime"]).any():
    errors.add("🧩 Duplicate rows with same msgSeqNum and exchHostTime found")

# 📉 4. Пустые заявки (ноль объема при непустой цене)
for side in ["buy", "sell"]:
    for i in range(1, 11):
        px_col = f"px_{side}_{i}"
        amt_col = f"amt_{side}_{i}"
        if px_col in converted and amt_col in converted:
            cond = (
                (converted[amt_col] == 0)
                & (converted[px_col].notna())
                & (converted[px_col] != 0)
            )
            if cond.any():
                errors.add(f"📉 Zero amount with non-null price in {px_col}")

# 📊 5. Нарушения порядка в стакане
for side, op in [("buy", lambda x, y: x < y), ("sell", lambda x, y: x > y)]:
    for i in range(1, 10):
        px1 = f"px_{side}_{i}"
        px2 = f"px_{side}_{i + 1}"
        if px1 in converted and px2 in converted:
            bad_order = (
                op(converted[px1], converted[px2])
                & converted[px1].notna()
                & converted[px2].notna()
            )
            if bad_order.any():
                errors.add(f"📊 Order book prices misordered: {px1} vs {px2}")
        amt1 = f"amt_{side}_{i}"
        amt2 = f"amt_{side}_{i + 1}"
        if amt1 in converted and amt2 in converted:
            bad_amt_order = (
                (converted[amt2] > converted[amt1])
                & (converted[amt1] > 0)
                & converted[amt2].notna()
            )
            if bad_amt_order.any():
                errors.add(f"📊 Order book volumes misordered: {amt1} vs {amt2}")

# 💱 6. Сделки вне спреда
if {"trade_px", "px_buy_1", "px_sell_1"}.issubset(converted.keys()):
    bad_trades = (converted["trade_px"] > 0) & (
        (converted["trade_px"] < converted["px_buy_1"])
        | (converted["trade_px"] > converted["px_sell_1"])
    )
    if bad_trades.any():
        errors.add("💱 Trades executed outside the spread")
    # Проверка отрицательного или нулевого спреда
    if (converted["px_sell_1"] <= converted["px_buy_1"]).any():
        errors.add("💱 Negative or zero spread (px_sell_1 <= px_buy_1)")

# 💼 7. Логика trade_amt / trade_cnt
if {"trade_amt", "trade_cnt"}.issubset(converted.keys()):
    if ((converted["trade_amt"] > 0) & (converted["trade_cnt"] == 0)).any():
        errors.add("💼 trade_amt > 0 but trade_cnt == 0")
    if ((converted["trade_amt"] == 0) & (converted["trade_cnt"] > 0)).any():
        errors.add("💼 trade_cnt > 0 but trade_amt == 0")
    if (converted["trade_cnt"] < 0).any():
        errors.add("💼 Negative trade_cnt values found")

# 🔁 8. trade_cnt > 0, но trade_px == 0
if {"trade_cnt", "trade_px"}.issubset(converted.keys()):
    if ((converted["trade_cnt"] > 0) & (converted["trade_px"] == 0)).any():
        errors.add("🔁 trade_cnt > 0 but trade_px == 0")

# 📐 9. Проверка согласованности trade_amt ≈ trade_px * trade_cnt
if {"trade_amt", "trade_cnt", "trade_px"}.issubset(converted.keys()):
    approx = converted["trade_px"] * converted["trade_cnt"]
    mismatch = (converted["trade_amt"] - approx).abs() > 1e-3
    valid = (converted["trade_amt"] > 0) & (converted["trade_cnt"] > 0)
    if (valid & mismatch).any():
        errors.add("📐 trade_amt not equal to trade_px * trade_cnt")

# ❓ 10. Пропущенные значения в обязательных колонках
for col in df.columns:
    if col != "moreTradesInBatch" and df[col].isnull().any():
        errors.add(f"❓ NaN values found in required column '{col}'")

# 🧮 11. Проверка moreTradesInBatch
if "moreTradesInBatch" in df.columns:
    unexpected = set(df["moreTradesInBatch"].dropna().unique()) - {0.0, 1.0}
    if unexpected:
        errors.add("🧮 Unexpected values in moreTradesInBatch (not 0 or 1)")

# 📎 12. Проверка type
if "type" in df.columns:
    allowed_types = {4, 6}
    if not converted["type"].isin(allowed_types).all():
        errors.add(f"📎 Unknown values in column 'type' (expected {allowed_types})")

# 🔍 13. Положительный trade_cnt при type != 4
if {"trade_cnt", "type"}.issubset(df.columns):
    if ((converted["trade_cnt"] > 0) & (converted["type"] != 4)).any():
        errors.add("🔍 trade_cnt > 0 but type != 4 (trade)")

# ♻️ 14. Повторяющиеся px_buy_1 / px_sell_1 (зависание фида)
for col in ["px_buy_1", "px_sell_1"]:
    if col in converted:
        repeats = (converted[col].shift() == converted[col]) & converted[col].notna()
        if repeats.mean() > 0.9:
            errors.add(f"♻️ {col} repeats in >90% of rows (possible feed freeze)")

# 🕳️ 15. Массовые пропуски на концах стакана
for col in ["amt_buy_10", "amt_sell_10"]:
    if col in df.columns and df[col].isna().mean() > 0.5:
        errors.add(f"🕳️ More than 50% NaNs in column '{col}' (book tail missing?)")

# 🛠️ 16. Специальная проверка px_sell_7
if "px_sell_7" in df.columns:
    non_numeric = (
        df["px_sell_7"].apply(pd.to_numeric, errors="coerce").isnull()
        & df["px_sell_7"].notnull()
    )
    if non_numeric.any():
        errors.add("🛠️ Non-numeric values found in px_sell_7 column")

# ➕ 17. Проверка moreTradesInBatch с trade_cnt и trade_amt
if {"moreTradesInBatch", "trade_cnt", "trade_amt"}.issubset(df.columns):
    cond = (df["moreTradesInBatch"] == 1) & (
        (converted["trade_cnt"] == 0) | (converted["trade_amt"] == 0)
    )
    if cond.any():
        errors.add("➕ moreTradesInBatch == 1 but trade_cnt == 0 or trade_amt == 0")

# ➕ 18. Проверка целочисленности
for int_col in ["msgSeqNum", "trade_cnt", "type"]:
    if int_col in converted:
        is_int = (
            converted[int_col]
            .dropna()
            .apply(
                lambda x: isinstance(x, (int, np.integer))
                or (isinstance(x, float) and x.is_integer())
            )
        )
        if not is_int.all():
            errors.add(f"🔢 Column '{int_col}' contains non-integer values")

# ➕ 19. Проверка больших отклонений между adapterTime и exchHostTime
if {"adapterTime", "exchHostTime"}.issubset(converted.keys()):
    delta = (converted["adapterTime"] - converted["exchHostTime"]).abs()
    if (delta > 5_000_000_000).any():  # 5 секунд
        errors.add("⏳ Large deviation (>5s) between adapterTime and exchHostTime")

# ➕ 20. Проверка отрицательных временных разниц в exchHostTime
if "exchHostTime" in converted:
    if (converted["exchHostTime"].diff().dropna() < 0).any():
        errors.add("📈 Negative time gaps detected in exchHostTime")

# ➕ 21. Проверка больших временных разрывов
if "exchHostTime" in converted:
    diffs = converted["exchHostTime"].diff().dropna()
    threshold_gap = diffs.mean() + 3 * diffs.std()
    if (diffs > threshold_gap).any():
        errors.add("📈 Time gaps larger than mean+3std in exchHostTime")

# ➕ 22. Проверка нулевых значений в trade_cnt и trade_amt
for col in ["trade_cnt", "trade_amt"]:
    if col in converted and (converted[col] == 0).all():
        errors.add(f"⚠️ All zero values in column '{col}'")

# ➕ 23. Проверка корректности флага moreTradesInBatch
if "moreTradesInBatch" in df.columns:
    if not set(df["moreTradesInBatch"].dropna().unique()).issubset({0, 1}):
        errors.add("🧮 Unexpected values in moreTradesInBatch (not 0 or 1)")

# ➕ 24. Проверка пропусков в объемах
for side in ["buy", "sell"]:
    for i in range(1, 11):
        amt_col = f"amt_{side}_{i}"
        if amt_col in df.columns and df[amt_col].isna().mean() > 0.2:
            errors.add(f"🕳️ More than 20% NaNs in column '{amt_col}'")

# ➕ 25. Проверка нулевых цен при положительных объемах
for side in ["buy", "sell"]:
    for i in range(1, 11):
        px_col = f"px_{side}_{i}"
        amt_col = f"amt_{side}_{i}"
        if px_col in converted and amt_col in converted:
            cond = (converted[amt_col] > 0) & (converted[px_col] == 0)
            if cond.any():
                errors.add(f"⚠️ Price is 0 but amount > 0 in {px_col} / {amt_col}")

# ➕ 26. Проверка последовательности msgSeqNum по type
if "msgSeqNum" in converted and "type" in converted:
    for t in [4, 6]:
        seq = converted["msgSeqNum"][converted["type"] == t].diff().dropna()
        if (seq != 1).any():
            errors.add(f"🔢 Gaps or duplicates in msgSeqNum for type {t}")

# ➕ 27. Проверка согласованности moreTradesInBatch с последовательными сделками
if {"moreTradesInBatch", "type"}.issubset(df.columns):
    cond = (df["moreTradesInBatch"] == 1) & (df["type"].shift(-1) != 4)
    if cond.any():
        errors.add("🧮 moreTradesInBatch == 1 but next row is not a trade (type != 4)")

# ➕ 28. Проверка экстремальных значений в ценах и объемах
for col in price_columns + amount_columns:
    if col in converted:
        z_scores = (converted[col] - converted[col].mean()) / converted[col].std()
        if (z_scores.abs() > 5).any():  # z-score > 5 как порог
            errors.add(f"📈 Extreme outlier values in column '{col}' (z-score > 5)")

# ➕ 29. Проверка глубины стакана (высшие уровни не должны быть заполнены, если нижние пусты)
for side in ["buy", "sell"]:
    for i in range(1, 10):
        px1 = f"px_{side}_{i}"
        px2 = f"px_{side}_{i + 1}"
        if px1 in converted and px2 in converted:
            cond = (converted[px1].isna() | (converted[px1] == 0)) & (
                converted[px2].notna() & (converted[px2] != 0)
            )
            if cond.any():
                errors.add(
                    f"📊 Higher order book level {px2} filled while {px1} is empty"
                )

# ➕ 30. Проверка симметричности пропусков в buy/sell сторонах
for i in range(1, 11):
    buy_amt = f"amt_buy_{i}"
    sell_amt = f"amt_sell_{i}"
    if buy_amt in df.columns and sell_amt in df.columns:
        buy_nan = df[buy_amt].isna()
        sell_nan = df[sell_amt].isna()
        if (buy_nan != sell_nan).mean() > 0.5:
            errors.add(f"🕳️ Asymmetric NaN patterns between {buy_amt} and {sell_amt}")

# ➕ 31. Проверка согласованности type 4 и type 6
if "type" in df.columns:
    trade_rows = converted["type"] == 4
    lob_rows = converted["type"] == 6
    if (
        (trade_rows) & (converted["trade_px"] == 0) & (converted["trade_amt"] == 0)
    ).any():
        errors.add("📎 Type 4 (trade) rows with zero trade_px and trade_amt")
    if (
        (lob_rows) & (converted["trade_px"] != 0) | (converted["trade_amt"] != 0)
    ).any():
        errors.add("📎 Type 6 (LOB update) rows with non-zero trade_px or trade_amt")

# ✅ Итоговый вывод
print("📋 Error Types Found:")
for e in sorted(errors):
    print("-", e)

print(f"\n✅ Total unique error types detected: {len(errors)}")
