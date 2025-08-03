from pathlib import Path

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
for time_col in ["exchHostTime", "adapterTime"]:
    diffs = converted[time_col].diff().dropna()
    threshold = diffs.mean() + 5 * diffs.std()
    if (diffs > threshold).any():
        errors.add(f"📈 {time_col} has suspiciously large time gaps")

# Проверка повторяющихся временных меток подряд
for time_col in ["exchHostTime", "adapterTime"]:
    repeats = converted[time_col] == converted[time_col].shift()
    if repeats.mean() > 0.9:
        errors.add(f"♻️ {time_col} repeats in >90% of rows (possible feed freeze)")

# ⏳ 2.1 adapterTime < exchHostTime
if {"adapterTime", "exchHostTime"}.issubset(converted.keys()):
    if (converted["adapterTime"] < converted["exchHostTime"]).any():
        errors.add("⏳ adapterTime is earlier than exchHostTime (may be invalid)")

# 🧩 3. Дубли
if df.duplicated(subset=["msgSeqNum"]).any():
    errors.add("🧩 Duplicate msgSeqNum values found")
if df.duplicated().any():
    errors.add("🧩 Completely duplicated rows found")

# Проверка дубликатов по времени и msgSeqNum в связке
time_msg_duplicates = df.duplicated(subset=["msgSeqNum", "exchHostTime"])
if time_msg_duplicates.any():
    errors.add("🧩 Duplicate rows with same msgSeqNum and exchHostTime found")

# 📉 4. Пустые заявки (ноль объема при непустой цене — ошибка)
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
                errors.add(f"📉 Zero amount with non-null {px_col} detected")

# 📊 5. Нарушения порядка в стакане
for side, op in [("buy", lambda x, y: x < y), ("sell", lambda x, y: x > y)]:
    for i in range(1, 10):
        px1 = f"px_{side}_{i}"
        px2 = f"px_{side}_{i + 1}"
        if px1 in converted and px2 in converted:
            bad_order = op(converted[px1], converted[px2])
            if bad_order.any():
                errors.add(f"📊 Order book prices misordered: {px1} vs {px2}")

# 💱 6. Сделки вне спреда (trade_px < px_buy_1 или > px_sell_1)
if {"trade_px", "px_buy_1", "px_sell_1"}.issubset(converted.keys()):
    bad_trades = (converted["trade_px"] < converted["px_buy_1"]) | (
        converted["trade_px"] > converted["px_sell_1"]
    )
    if bad_trades.any():
        errors.add("💱 Trades executed outside the spread")

# 💼 7. Логика trade_amt / trade_cnt
if {"trade_amt", "trade_cnt"}.issubset(converted.keys()):
    if ((converted["trade_amt"] > 0) & (converted["trade_cnt"] == 0)).any():
        errors.add("💼 trade_amt > 0 but trade_cnt == 0")
    if ((converted["trade_amt"] == 0) & (converted["trade_cnt"] > 0)).any():
        errors.add("💼 trade_cnt > 0 but trade_amt == 0")

# 🔁 8. trade_cnt > 0, но trade_px == 0
if {"trade_cnt", "trade_px"}.issubset(converted.keys()):
    if ((converted["trade_cnt"] > 0) & (converted["trade_px"] == 0)).any():
        errors.add("🔁 trade_cnt > 0 but trade_px == 0")

# 📐 9. Проверка согласованности trade_amt ≈ trade_px * trade_cnt (с небольшой дельтой)
if {"trade_amt", "trade_cnt", "trade_px"}.issubset(converted.keys()):
    approx = converted["trade_px"] * converted["trade_cnt"]
    mismatch = (converted["trade_amt"] - approx).abs() > 1e-3  # чуть больше дельта
    valid = (converted["trade_amt"] > 0) & (converted["trade_cnt"] > 0)
    if (valid & mismatch).any():
        errors.add("📐 trade_amt not equal to trade_px * trade_cnt")

# ❓ 10. Пропущенные значения в обязательных колонках (кроме moreTradesInBatch)
for col in df.columns:
    if df[col].isnull().any() and col != "moreTradesInBatch":
        errors.add(f"❓ NaN values found in required column '{col}'")

# 🧮 11. Проверка moreTradesInBatch
if "moreTradesInBatch" in df.columns:
    if df["moreTradesInBatch"].notnull().any():
        unexpected = set(df["moreTradesInBatch"].dropna().unique())
        allowed = {0.0, 1.0}
        if not unexpected <= allowed:
            errors.add("🧮 Unexpected values in moreTradesInBatch (not 0 or 1)")

# 📎 12. Проверка type
if "type" in df.columns:
    allowed_types = {4, 6}  # из данных
    if not converted["type"].isin(allowed_types).all():
        errors.add(f"📎 Unknown values in column 'type' (expected {allowed_types})")

# 🔍 13. Положительный trade_cnt без типа "trade" (type != 4)
if {"trade_cnt", "type"}.issubset(df.columns):
    cond = (converted["trade_cnt"] > 0) & (converted["type"] != 4)
    if cond.any():
        errors.add("🔍 trade_cnt > 0 but type != 4 (trade)")

# ♻️ 14. Повторяющиеся px_buy_1 / px_sell_1 (зависание фида)
for col in ["px_buy_1", "px_sell_1"]:
    if col in converted:
        # Проверяем длины подряд идущих повторов (максимальная)
        vals = converted[col]
        max_run = 1
        current_run = 1
        for i in range(1, len(vals)):
            if vals.iloc[i] == vals.iloc[i - 1] and pd.notna(vals.iloc[i]):
                current_run += 1
                max_run = max(max_run, current_run)
            else:
                current_run = 1
        repeats = (vals.shift() == vals) & vals.notna()
        if repeats.mean() > 0.9:
            errors.add(
                f"♻️ Value in {col} repeats in >90% of rows (possible feed freeze), max consecutive repeats = {max_run}"
            )

# 🕳️ 15. Массовые пропуски на концах стакана
for col in ["amt_buy_10", "px_sell_10"]:
    if col in df.columns:
        nan_ratio = df[col].isna().mean()
        if nan_ratio > 0.5:
            errors.add(f"🕳️ More than 50% NaNs in column '{col}' (book tail missing?)")

# 🛠️ 16. Специальная проверка px_sell_7 (object type)
if "px_sell_7" in df.columns:
    non_numeric = (
        df["px_sell_7"].apply(pd.to_numeric, errors="coerce").isnull()
        & df["px_sell_7"].notnull()
    )
    if non_numeric.any():
        errors.add("🛠️ Non-numeric values found in px_sell_7 column")

# ➕ 17. Проверка связей moreTradesInBatch с trade_cnt и trade_amt
if {"moreTradesInBatch", "trade_cnt", "trade_amt"}.issubset(df.columns):
    cond = (df["moreTradesInBatch"] == 1) & (
        (converted["trade_cnt"] == 0) | (converted["trade_amt"] == 0)
    )
    if cond.any():
        errors.add("➕ moreTradesInBatch == 1 but trade_cnt == 0 or trade_amt == 0")


# ➕ 18. Вывод примеров ошибок (по первой строке каждого типа, не более 5 для каждого)
def print_examples(cond, desc, limit=5):
    idxs = df.index[cond]
    if len(idxs) > 0:
        print(f"📌 Examples of {desc}:")
        for i in idxs[:limit]:
            print(df.loc[i].to_dict())


# Пример вывода для нескольких ошибок (раскомментируй, если нужно):
# if (converted["trade_px"] < converted["px_buy_1"]).any():
#     print_examples(converted["trade_px"] < converted["px_buy_1"], "trade_px < px_buy_1")

# ✅ Итоговый вывод
print("📋 Error Types Found:")
for e in sorted(errors):
    print("-", e)

print(f"\n✅ Total unique error types detected: {len(errors)}")
