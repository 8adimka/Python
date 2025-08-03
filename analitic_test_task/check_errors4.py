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
        errors.add(
            f"📛 Колонка '{col}' содержит нечисловые значения (должна быть float)"
        )

# 📉 1. Отрицательные значения (только там, где не должны быть)
price_columns = [col for col in df.columns if "px" in col or "trade_px" in col]
amount_columns = [col for col in df.columns if "amt" in col or "trade_amt" in col]

for col in price_columns:
    if (converted[col] < 0).any():
        errors.add(f"📉 Отрицательные значения цены в колонке '{col}'")
    # Проверка на более чем два знака после запятой
    if ((converted[col] * 100).round(0) != converted[col] * 100).any():
        errors.add(f"📉 Цена в колонке '{col}' имеет более двух знаков после запятой")

for col in amount_columns:
    if (converted[col] < 0).any():
        errors.add(f"📉 Отрицательные значения объема в колонке '{col}'")

# 📈 2. Временные ошибки
for time_col in ["exchHostTime", "adapterTime"]:
    # Проверка монотонности
    if not converted[time_col].is_monotonic_increasing:
        errors.add(f"📈 {time_col} не является монотонно возрастающим")
    # Проверка нулевых и отрицательных таймстампов
    if (converted[time_col] <= 0).any():
        errors.add(f"📈 {time_col} содержит нулевые или отрицательные временные метки")
    # Проверка больших скачков времени
    diffs = converted[time_col].diff().dropna()
    threshold = diffs.mean() + 5 * diffs.std()
    if (diffs > threshold).any():
        errors.add(f"📈 {time_col} имеет подозрительно большие временные разрывы")
    # Проверка повторяющихся временных меток
    repeats = converted[time_col] == converted[time_col].shift()
    if repeats.mean() > 0.9:
        errors.add(f"♻️ {time_col} повторяется в >90% строк (возможная заморозка фида)")

# ⏳ 2.1 Проверка adapterTime vs exchHostTime
if {"adapterTime", "exchHostTime"}.issubset(converted.keys()):
    time_diff = converted["adapterTime"] - converted["exchHostTime"]
    if (time_diff < 0).any():
        errors.add("⏳ adapterTime раньше, чем exchHostTime")
    if (time_diff.abs() > 5_000_000_000).any():  # 5 секунд
        errors.add("⏳ Большое отклонение (>5с) между adapterTime и exchHostTime")

# 🧩 3. Дубли
for t in [4, 6]:
    if df[df["type"] == t]["msgSeqNum"].duplicated().any():
        errors.add(f"🧩 Дублирующиеся значения msgSeqNum для типа {t}")
if df.duplicated().any():
    errors.add("🧩 Полностью дублирующиеся строки")
if df.duplicated(subset=["msgSeqNum", "exchHostTime"]).any():
    errors.add("🧩 Дублирующиеся строки с одинаковыми msgSeqNum и exchHostTime")

# 📉 4. Пустые заявки
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
                errors.add(f"📉 Нулевой объем с ненулевой ценой в {px_col}")
            # Проверка парного соответствия NaN
            cond1 = converted[px_col].isna() & converted[amt_col].notna()
            cond2 = converted[px_col].notna() & converted[amt_col].isna()
            if cond1.any():
                errors.add(
                    f"❓ Несогласованный NaN: цена NaN, но объем не NaN в {px_col}/{amt_col}"
                )
            if cond2.any():
                errors.add(
                    f"❓ Несогласованный NaN: цена не NaN, но объем NaN в {px_col}/{amt_col}"
                )

# 📊 5. Нарушения порядка в стакане
for side, op in [("buy", lambda x, y: x <= y), ("sell", lambda x, y: x >= y)]:
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
                errors.add(f"📊 Цены в стакане неупорядочены или равны: {px1} vs {px2}")
        amt1 = f"amt_{side}_{i}"
        amt2 = f"amt_{side}_{i + 1}"
        if amt1 in converted and amt2 in converted:
            cond = (converted[amt1] == 0) & (converted[amt2] > 0)
            if cond.any():
                errors.add(
                    f"📊 Нулевой объем на уровне {i}, но положительный объем на уровне {i + 1} для стороны {side}"
                )

# 💱 6. Сделки вне спреда
if {"trade_px", "px_buy_1", "px_sell_1"}.issubset(converted.keys()):
    bad_trades = (converted["trade_px"] > 0) & (
        (converted["trade_px"] < converted["px_buy_1"])
        | (converted["trade_px"] > converted["px_sell_1"])
    )
    if bad_trades.any():
        errors.add("💱 Сделки выполнены вне спреда")
    if (converted["px_sell_1"] <= converted["px_buy_1"]).any():
        errors.add("💱 Отрицательный или нулевой спред (px_sell_1 <= px_buy_1)")

# 💼 7. Логика trade_amt / trade_cnt
if {"trade_amt", "trade_cnt"}.issubset(converted.keys()):
    if ((converted["trade_amt"] > 0) & (converted["trade_cnt"] == 0)).any():
        errors.add("💼 trade_amt > 0, но trade_cnt == 0")
    if ((converted["trade_amt"] == 0) & (converted["trade_cnt"] > 0)).any():
        errors.add("💼 trade_cnt > 0, но trade_amt == 0")
    if (converted["trade_cnt"] < 0).any():
        errors.add("💼 Отрицательные значения trade_cnt")

# 🔁 8. trade_cnt > 0, но trade_px == 0
if {"trade_cnt", "trade_px"}.issubset(converted.keys()):
    if ((converted["trade_cnt"] > 0) & (converted["trade_px"] == 0)).any():
        errors.add("🔁 trade_cnt > 0, но trade_px == 0")

# 📐 9. Проверка согласованности trade_amt и trade_cnt
if {"trade_amt", "trade_cnt", "trade_px"}.issubset(converted.keys()):
    valid = (
        (converted["trade_amt"] != 0)
        & (converted["trade_cnt"] > 0)
        & (converted["trade_px"] > 0)
    )
    if valid.any():
        errors.add(
            "📐 trade_amt не соответствует ожидаемой логике для ненулевых сделок"
        )

# ❓ 10. Пропущенные значения в обязательных колонках
for col in df.columns:
    if col != "moreTradesInBatch" and df[col].isnull().any():
        errors.add(f"❓ NaN значения в обязательной колонке '{col}'")

# 🧮 11. Проверка moreTradesInBatch
if "moreTradesInBatch" in df.columns:
    unexpected = set(df["moreTradesInBatch"].dropna().unique()) - {0.0, 1.0}
    if unexpected:
        errors.add("🧮 Неожиданные значения в moreTradesInBatch (не 0 или 1)")

# 📎 12. Проверка type
if "type" in df.columns:
    allowed_types = {4, 6}
    if not converted["type"].isin(allowed_types).all():
        errors.add(
            f"📎 Неизвестные значения в колонке 'type' (ожидаются {allowed_types})"
        )

# 🔍 13. Положительный trade_cnt при type != 4
if {"trade_cnt", "type"}.issubset(df.columns):
    if ((converted["trade_cnt"] > 0) & (converted["type"] != 4)).any():
        errors.add("🔍 trade_cnt > 0, но type != 4 (сделка)")

# ♻️ 14. Повторяющиеся px_buy_1 / px_sell_1
for col in ["px_buy_1", "px_sell_1"]:
    if col in converted:
        repeats = (converted[col].shift() == converted[col]) & converted[col].notna()
        if repeats.mean() > 0.9:
            errors.add(
                f"♻️ Значение в {col} повторяется в >90% строк (возможная заморозка фида)"
            )

# 🕳️ 15. Массовые пропуски на концах стакана
for col in ["amt_buy_10", "amt_sell_10"]:
    if col in df.columns and df[col].isna().mean() > 0.5:
        errors.add(f"🕳️ Более 50% NaN в колонке '{col}' (хвост стакана отсутствует?)")

# 🛠️ 16. Специальная проверка px_sell_7
if "px_sell_7" in df.columns:
    non_numeric = (
        df["px_sell_7"].apply(pd.to_numeric, errors="coerce").isnull()
        & df["px_sell_7"].notnull()
    )
    if non_numeric.any():
        errors.add("🛠️ Нечисловые значения в колонке px_sell_7")

# ➕ 17. Проверка moreTradesInBatch с trade_cnt и trade_amt
if {"moreTradesInBatch", "trade_cnt", "trade_amt"}.issubset(df.columns):
    cond = (df["moreTradesInBatch"] == 1) & (
        (converted["trade_cnt"] == 0) | (converted["trade_amt"] == 0)
    )
    if cond.any():
        errors.add("➕ moreTradesInBatch == 1, но trade_cnt == 0 или trade_amt == 0")

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
            errors.add(f"🔢 Колонка '{int_col}' содержит нецелочисленные значения")

# ➕ 19. Проверка последовательности msgSeqNum по type
if "msgSeqNum" in converted and "type" in converted:
    for t in [4, 6]:
        seq = converted["msgSeqNum"][converted["type"] == t].diff().dropna()
        if (seq != 1).any():
            errors.add(f"🔢 Пропуски или дубликаты в msgSeqNum для типа {t}")

# ➕ 20. Проверка согласованности type 4 и type 6
if "type" in df.columns:
    trade_rows = converted["type"] == 4
    lob_rows = converted["type"] == 6
    if (
        (trade_rows) & (converted["trade_px"] == 0) & (converted["trade_amt"] == 0)
    ).any():
        errors.add("📎 Строки типа 4 (сделка) с нулевыми trade_px и trade_amt")
    if (
        (lob_rows) & (converted["trade_px"] != 0) | (converted["trade_amt"] != 0)
    ).any():
        errors.add(
            "📎 Строки типа 6 (обновление стакана) с ненулевыми trade_px или trade_amt"
        )

# ➕ 21. Проверка экстремальных значений
for col in price_columns + amount_columns:
    if col in converted:
        z_scores = (converted[col] - converted[col].mean()) / converted[col].std()
        if (z_scores.abs() > 5).any():
            errors.add(f"📈 Экстремальные значения в колонке '{col}' (z-score > 5)")

# ➕ 22. Проверка глубины стакана
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
                    f"📊 Более высокий уровень стакана {px2} заполнен, в то время как {px1} пуст"
                )

# ✅ Итоговый вывод
print("📋 Обнаруженные типы ошибок:")
for e in sorted(errors):
    print("-", e)

print(f"\n✅ Всего обнаружено уникальных типов ошибок: {len(errors)}")
