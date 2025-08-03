# 🇬🇧 English version

# Good day

## The task turned out to be surprisingly not boring, thank you

### Initial Analysis

- **What we see:**
  1. 40,374 rows, 48 columns.
  2. px_sell_7 — object type, though should be float64 → ⚠️ clear error.
  3. moreTradesInBatch — contains many NaNs: 10,218 non-empty out of 40,374 → suspicious.
  4. Columns: px_buy_N, amt_buy_N, px_sell_N, amt_sell_N — order book (L2).
  5. type, msgSeqNum, exchHostTime, adapterTime — meta-information.
  6. trade_px, trade_amt, trade_cnt — trades.

# Detected Error Types in test.feather

## 1. Data Types

- **Error:** Column px_sell_7 contains non-numeric values (should be float).
- **Specific errors in category:**
  - 📛 Column 'px_sell_7' contains non-numeric values (should be float).
- **What's happening:** Price columns like px_sell_7 should contain numeric values (order book prices). Non-numeric values may result from data collection errors, such as string artifacts or incorrect formatting.
- **Why it's an error:** Prices must be numeric for calculations like spread or market depth. Non-numeric values disrupt data processing.
- **Consequences:** This may cause failures in trading algorithms or incorrect market metric calculations.

## 2. Incorrect Values

- **Errors:**
  - 📉 Negative volume values in columns amt_buy_1–amt_buy_10, amt_sell_8, trade_amt.
  - 📉 Negative price values in column px_buy_9.
  - 📉 Prices with more than two decimal places in columns px_buy_1–px_buy_10.
- **What's happening:**
  - Negative volumes in amt_(e.g., amt_buy_1, amt_sell_8) are invalid as order book volumes must be positive. This may stem from input or processing errors.
  - Negative prices in px_buy_9 indicate failure since asset prices cannot be negative.
  - Prices with >2 decimal places (e.g., 11357.999 instead of 11357.99) violate Bitcoin's standard price format (usually 0.01 step).
  - Negative values in trade_amt may be valid if representing sales but require context verification.
- **Why it's an error:** Negative values and incorrect price precision distort market data logic, skewing liquidity and cost calculations.
- **Consequences:** May lead to incorrect trading decisions or algorithm failures.

## 3. Missing Values

- **Errors:**
  - ❓ NaN values in mandatory columns amt_buy_1–amt_buy_10, px_buy_1.
  - ❓ Inconsistent NaN: price NaN but volume not NaN in px_buy_1/amt_buy_1.
  - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_1/amt_buy_1–px_buy_10/amt_buy_10.
- **What's happening:** Missing values (NaN) in mandatory columns like px_buy_1 or amt_buy_1 indicate incomplete data. Inconsistent NaNs (price present but volume missing or vice versa) violate order book level pairing integrity.
- **Why it's an error:** All order book levels must be fully populated for accurate market depth analysis. Inconsistent NaNs indicate data corruption.
- **Consequences:** May distort spread and liquidity calculations, leading to trading strategy errors.

## 4. Empty Orders

- **Error:**
  - 📉 Zero volume with non-zero price in px_buy_6.
- **What's happening:** Each order book level should have non-zero volume if price is specified. Zero volume with non-zero price (e.g., in px_buy_6) indicates empty order.
- **Why it's an error:** Empty orders distort market depth and liquidity analysis since each level should contain active orders.
- **Consequences:** May lead to incorrect assessment of available market volume.

## 5. Order Book Order Violations

- **Errors:**
  - 📊 Unordered or equal prices in book: px_buy_1 vs px_buy_2, px_buy_9 vs px_buy_10, px_sell_1 vs px_sell_2–px_sell_7 vs px_sell_8.
  - 📊 Higher book level px_buy_2 filled while px_buy_1 empty.
  - 📊 Zero volume at level 6 but positive volume at level 7 for buy side.
- **What's happening:**
  - Buy prices should be strictly decreasing (px_buy_1 > px_buy_2), sell prices strictly increasing (px_sell_1 < px_sell_2). Equality or order violation indicates incorrect book updates.
  - Filled deeper levels (e.g., px_buy_2) with empty near levels (px_buy_1) violate book structure.
  - Zero volume at level 6 with non-zero at level 7 also indicates inconsistency.
- **Why it's an error:** Incorrect order or empty near levels distorts best bids/offers, affecting spread calculation.
- **Consequences:** May lead to incorrect trading signals and market analysis errors.

## 6. Trades Outside the Spread

- **Error:**
  - 💱 Trades executed outside spread.
  - 💱 Negative or zero spread (px_sell_1 <= px_buy_1).
- **What's happening:** Trades should occur within spread (between px_buy_1 and px_sell_1). Trades outside this range or zero/negative spread (px_sell_1 <= px_buy_1) indicate anomaly, possibly due to data errors or extreme market events.
- **Why it's an error:** Such anomalies don't match normal market dynamics and may be caused by data corruption.
- **Consequences:** May distort price formation and volatility calculations.

## 7. Logical Inconsistencies in Trades

- **Errors:**
  - 💼 trade_amt > 0 but trade_cnt == 0.
  - 💼 Negative trade_cnt values.
- **What's happening:**
  - Positive trade volume (trade_amt > 0) with zero trade count (trade_cnt == 0) is logically contradictory.
  - Negative trade count (trade_cnt < 0) is invalid since trades can't be negative.
- **Why it's an error:** These inconsistencies indicate data aggregation or recording errors.
- **Consequences:** May lead to incorrect trade activity and volume calculations.

## 8. Incorrect trade_px when trade_cnt > 0

- **Error:**
  - 🔁 trade_cnt > 0 but trade_px == 0.
- **What's happening:** If trades exist (trade_cnt > 0), trade price (trade_px) should be positive. Zero price indicates data error.
- **Why it's an error:** Trades must have non-zero price for correct analysis.
- **Consequences:** May distort average trade price and total cost calculations.

## 9. Temporal Anomalies

- **Errors:**
  - 📈 exchHostTime not monotonically increasing.
  - 📈 adapterTime not monotonically increasing.
  - 📈 exchHostTime contains zero or negative timestamps.
  - 📈 exchHostTime has suspiciously large time gaps.
  - 📈 adapterTime has suspiciously large time gaps.
  - ♻️ exchHostTime repeats in >90% rows (possible feed freeze).
  - ♻️ px_buy_1 value repeats in >90% rows (possible feed freeze).
  - ♻️ px_sell_1 value repeats in >90% rows (possible feed freeze).
  - ⏳ adapterTime earlier than exchHostTime.
  - ⏳ Large deviation (>5s) between adapterTime and exchHostTime.
- **What's happening:**
  - Non-monotonic timestamps disrupt event chronology needed for analysis.
  - Zero/negative timestamps in exchHostTime indicate sync failure.
  - Large time gaps (above average + 5σ) may stem from delays or data loss.
  - Repeated timestamps/prices in >90% rows suggest possible data "freeze" when updates aren't received.
  - adapterTime earlier than exchHostTime or with large deviation (>5 seconds) indicates sync issues between exchange and adapter.
- **Why it's an error:** Timestamps must be sequential and precise for time series analysis.
- **Consequences:** May disrupt event order, distorting analysis and trading decisions.

## 10. Incorrect Values in 'type' Field

- **Error:**
  - 📎 Unknown values in 'type' column.
- **What's happening:** 'type' column should only contain values 4 (trades) or 6 (order book updates). Other values indicate data corruption or format change.
- **Why it's an error:** Incorrect message types disrupt processing.
- **Consequences:** May lead to missed data or incorrect interpretation.

## 11. Duplicates

- **Errors:**
  - 🧩 Fully duplicate rows.
  - 🧩 Duplicate msgSeqNum values for type 4.
  - � Duplicate rows with same msgSeqNum and exchHostTime.
  - 🔢 Gaps or duplicates in msgSeqNum for type 4.
  - 🔢 Gaps or duplicates in msgSeqNum for type 6.
- **What's happening:** Duplicate rows or sequence numbers (msgSeqNum) indicate message re-recording. Gaps in msgSeqNum may mean data loss.
- **Why it's an error:** Each message should be unique, especially msgSeqNum, to ensure data integrity.
- **Consequences:** Duplicates inflate trade activity, while gaps may miss critical events.

## 12. Logical Inconsistencies in Trades and Order Book

- **Errors:**
  - 📎 Type 6 rows (order book updates) with non-zero trade_px or trade_amt.
  - 📐 trade_amt doesn't match expected logic for non-zero trades.
- **What's happening:**
  - Type 6 messages (order book updates) shouldn't contain trade data (trade_px, trade_amt) as they're only for order book updates.
  - trade_amt inconsistency (e.g., non-zero trade_amt without other trade conditions) indicates aggregation error.
- **Why it's an error:** This violates expected message structure and data logic.
- **Consequences:** May lead to incorrect interpretation of trade and order book update data.

## 13. Additional Potential Errors

- **FIX protocol-related errors:**
  - **Missing tags:** Absence of mandatory tags in FIX messages may lead to incomplete data.
  - **Incorrect checksum:** Invalid checksum (tag 10) indicates message corruption during transmission.
  - **Sequence number gaps:** Gaps in msgSeqNum may indicate lost messages.
- **What's happening:** If data is FIX-based, these errors may stem from formatting or transmission issues.
- **Why it's an error:** Such errors compromise data integrity needed for accurate processing.
- **Consequences:** May lead to data loss or incorrect interpretation.

- **moreTradesInBatch issues:**
  - **What's happening:** moreTradesInBatch column has many NaN values, which may be normal if info is unavailable, but could indicate incomplete data.
  - **Why it may be problematic:** Gaps may affect analyses depending on this info, e.g., trade batch determination.
  - **Consequences:** May limit trade activity analysis accuracy.

- **Order book depth:**
  - **What's happening:** Dataset has up to 10 levels, which seems consistent, but issues may arise if deeper levels are filled while near ones are empty.
  - **Why it may be an error:** This may indicate incorrect book updates.
  - **Consequences:** May distort market depth analysis.

## Conclusion

I've written a small script detecting a wide range of errors covering:

- data type issues, values, timestamps, trade logic, and order book structure.

The script identified 110 unique error types grouped into 13 logical categories for structured analysis. Each category covers errors related to specific data aspects like data types, values, timestamps, order book structure, and trade logic. This approach reveals a broad spectrum of anomalies critical for ensuring trading system reliability. Additional checks like FIX message integrity or order book depth consistency could be added for greater completeness, but current analysis already demonstrates high effectiveness.

# More details on errors ->

## 📋 Detected Error Types

    - ⏳ adapterTime earlier than exchHostTime
    - ⏳ Large deviation (>5s) between adapterTime and exchHostTime
    - ♻️ exchHostTime repeats in >90% rows (possible feed freeze)
    - ♻️ px_buy_1 value repeats in >90% rows (possible feed freeze)
    - ♻️ px_sell_1 value repeats in >90% rows (possible feed freeze)
    - ❓ NaN values in mandatory column 'amt_buy_1'
    - ❓ NaN values in mandatory column 'amt_buy_10'
    - ❓ NaN values in mandatory column 'amt_buy_2'
    - ❓ NaN values in mandatory column 'amt_buy_3'
    - ❓ NaN values in mandatory column 'amt_buy_4'
    - ❓ NaN values in mandatory column 'amt_buy_5'
    - ❓ NaN values in mandatory column 'amt_buy_6'
    - ❓ NaN values in mandatory column 'amt_buy_7'
    - ❓ NaN values in mandatory column 'amt_buy_8'
    - ❓ NaN values in mandatory column 'amt_buy_9'
    - ❓ NaN values in mandatory column 'px_buy_1'
    - ❓ Inconsistent NaN: price NaN but volume not NaN in px_buy_1/amt_buy_1
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_1/amt_buy_1
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_10/amt_buy_10
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_2/amt_buy_2
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_3/amt_buy_3
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_4/amt_buy_4
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_5/amt_buy_5
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_6/amt_buy_6
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_7/amt_buy_7
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_8/amt_buy_8
    - ❓ Inconsistent NaN: price not NaN but volume NaN in px_buy_9/amt_buy_9
    - 💱 Negative or zero spread (px_sell_1 <= px_buy_1)
    - 💱 Trades executed outside spread
    - 💼 trade_amt > 0 but trade_cnt == 0
    - 💼 Negative trade_cnt values
    - 📈 adapterTime has suspiciously large time gaps
    - 📈 adapterTime not monotonically increasing
    - 📈 exchHostTime has suspiciously large time gaps
    - 📈 exchHostTime not monotonically increasing
    - 📈 exchHostTime contains zero or negative timestamps
    - 📈 Extreme values in 'amt_buy_1' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_10' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_2' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_3' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_4' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_5' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_6' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_7' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_8' (z-score > 5)
    - 📈 Extreme values in 'amt_buy_9' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_1' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_10' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_2' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_3' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_4' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_5' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_6' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_7' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_8' (z-score > 5)
    - 📈 Extreme values in 'amt_sell_9' (z-score > 5)
    - 📈 Extreme values in 'px_buy_1' (z-score > 5)
    - 📈 Extreme values in 'px_buy_10' (z-score > 5)
    - 📈 Extreme values in 'px_buy_2' (z-score > 5)
    - 📈 Extreme values in 'px_buy_3' (z-score > 5)
    - 📈 Extreme values in 'px_buy_4' (z-score > 5)
    - 📈 Extreme values in 'px_buy_5' (z-score > 5)
    - 📈 Extreme values in 'px_buy_6' (z-score > 5)
    - 📈 Extreme values in 'px_buy_7' (z-score > 5)
    - 📈 Extreme values in 'px_buy_8' (z-score > 5)
    - 📈 Extreme values in 'px_buy_9' (z-score > 5)
    - 📈 Extreme values in 'trade_amt' (z-score > 5)
    - 📉 Zero volume with non-zero price in px_buy_6
    - 📉 Negative volume values in 'amt_buy_1'
    - 📉 Negative volume values in 'amt_buy_10'
    - 📉 Negative volume values in 'amt_buy_2'
    - 📉 Negative volume values in 'amt_buy_3'
    - 📉 Negative volume values in 'amt_buy_4'
    - 📉 Negative volume values in 'amt_buy_5'
    - 📉 Negative volume values in 'amt_buy_6'
    - 📉 Negative volume values in 'amt_buy_7'
    - 📉 Negative volume values in 'amt_buy_8'
    - 📉 Negative volume values in 'amt_buy_9'
    - 📉 Negative volume values in 'amt_sell_8'
    - 📉 Negative volume values in 'trade_amt'
    - 📉 Negative price values in 'px_buy_9'
    - 📉 'px_buy_1' price has >2 decimal places
    - 📉 'px_buy_10' price has >2 decimal places
    - 📉 'px_buy_2' price has >2 decimal places
    - 📉 'px_buy_3' price has >2 decimal places
    - 📉 'px_buy_4' price has >2 decimal places
    - 📉 'px_buy_5' price has >2 decimal places
    - 📉 'px_buy_6' price has >2 decimal places
    - 📉 'px_buy_7' price has >2 decimal places
    - 📉 'px_buy_8' price has >2 decimal places
    - 📉 'px_buy_9' price has >2 decimal places
    - 📊 Higher book level px_buy_2 filled while px_buy_1 empty
    - 📊 Zero volume at level 6 but positive at level 7 for buy side
    - 📊 Unordered or equal prices in book: px_buy_1 vs px_buy_2
    - 📊 Unordered or equal prices in book: px_buy_9 vs px_buy_10
    - 📊 Unordered or equal prices in book: px_sell_1 vs px_sell_2
    - 📊 Unordered or equal prices in book: px_sell_2 vs px_sell_3
    - 📊 Unordered or equal prices in book: px_sell_3 vs px_sell_4
    - 📊 Unordered or equal prices in book: px_sell_4 vs px_sell_5
    - 📊 Unordered or equal prices in book: px_sell_5 vs px_sell_6
    - 📊 Unordered or equal prices in book: px_sell_6 vs px_sell_7
    - 📊 Unordered or equal prices in book: px_sell_7 vs px_sell_8
    - 📎 Type 6 rows (order book updates) with non-zero trade_px or trade_amt
    - 📐 trade_amt doesn't match expected logic for non-zero trades
    - 📛 Column 'px_sell_7' contains non-numeric values (should be float)
    - 🔢 Gaps or duplicates in msgSeqNum for type 4
    - 🔢 Gaps or duplicates in msgSeqNum for type 6
    - 🧩 Duplicate msgSeqNum values for type 4
    - 🧩 Duplicate rows with same msgSeqNum and exchHostTime
    - 🧩 Fully duplicate rows

    ✅ Total unique error types detected: 110 -> can be conditionally grouped into 13 categories.

# 🇷🇺 Русская версия

# Добрый день, будущие коллеги

## Задание оказалось на удивление не скучным, спасибо

### Первичный анализ

- **Что видим:**
  1. 40374 строк, 48 колонок.
  2. `px_sell_7` — тип `object`, хотя должно быть `float64` → ⚠️ явная ошибка.
  3. `moreTradesInBatch` — содержит много NaN: 10218 непустых из 40374 → это подозрительно.
  4. Колонки: `px_buy_N`, `amt_buy_N`, `px_sell_N`, `amt_sell_N` — стакан заявок (L2).
  5. `type`, `msgSeqNum`, `exchHostTime`, `adapterTime` — мета-информация.
  6. `trade_px`, `trade_amt`, `trade_cnt` — сделки.

# Обнаруженные типы ошибок в test.feather

## 1. Типы данных (Data Types)

- **Ошибка:** Колонка `px_sell_7` содержит нечисловые значения (должна быть `float`).
- **Конкретные ошибки в категории:**
  - 📛 Колонка 'px_sell_7' содержит нечисловые значения (должна быть float).
- **Что происходит:** Ценовые колонки, такие как `px_sell_7`, должны содержать числовые значения (цены в лимитном стакане). Нечисловые значения могут быть результатом ошибок при сборе данных, например, строковые артефакты или некорректное форматирование.
- **Почему это ошибка:** Цены должны быть числами для расчётов, таких как спред или рыночная глубина. Нечисловые значения нарушают обработку данных.
- **Последствия:** Это может привести к сбоям в торговых алгоритмах или неверным расчётам рыночных метрик.

## 2. Неверные значения (Incorrect Values)

- **Ошибки:**
  - 📉 Отрицательные значения объема в колонках `amt_buy_1`–`amt_buy_10`, `amt_sell_8`, `trade_amt`.
  - 📉 Отрицательные значения цены в колонке `px_buy_9`.
  - 📉 Цены с более чем двумя знаками после запятой в колонках `px_buy_1`–`px_buy_10`.
- **Что происходит:**
  - Отрицательные объёмы в `amt_` (например, `amt_buy_1`, `amt_sell_8`) недопустимы, так как объёмы в лимитном стакане должны быть положительными. Это может быть вызвано ошибками ввода или обработки.
  - Отрицательные цены в `px_buy_9` указывают на сбой, так как цены активов не могут быть отрицательными.
  - Цены с более чем двумя знаками после запятой (например, 11357.999 вместо 11357.99) нарушают стандартный формат цен для биткойна (шаг цены обычно 0.01).
  - Отрицательные значения в `trade_amt` могут быть допустимы, если обозначают продажи, но требуют проверки контекста.
- **Почему это ошибка:** Отрицательные значения и неверная точность цен нарушают логику рыночных данных, искажая расчёты ликвидности и стоимости.
- **Последствия:** Это может привести к неверным торговым решениям или сбоям в алгоритмах.

## 3. Пропущенные значения (Missing Values)

- **Ошибки:**
  - ❓ NaN значения в обязательных колонках `amt_buy_1`–`amt_buy_10`, `px_buy_1`.
  - ❓ Несогласованный NaN: цена NaN, но объем не NaN в `px_buy_1/amt_buy_1`.
  - ❓ Несогласованный NaN: цена не NaN, но объем NaN в `px_buy_1/amt_buy_1`–`px_buy_10/amt_buy_10`.
- **Что происходит:** Пропущенные значения (NaN) в обязательных колонках, таких как `px_buy_1` или `amt_buy_1`, указывают на неполные данные. Несогласованные NaN (когда цена присутствует, а объём отсутствует, или наоборот) нарушают парную целостность уровней стакана.
- **Почему это ошибка:** Все уровни стакана должны быть полностью заполнены для точного анализа рыночной глубины. Несогласованные NaN указывают на повреждение данных.
- **Последствия:** Это может искажать расчёты спреда и ликвидности, приводя к ошибкам в торговых стратегиях.

## 4. Пустые заявки (Empty Orders)

- **Ошибка:**
  - 📉 Нулевой объем с ненулевой ценой в `px_buy_6`.
- **Что происходит:** В лимитном стакане каждый уровень должен иметь ненулевой объём, если указана цена. Нулевой объём при ненулевой цене (например, в `px_buy_6`) указывает на пустую заявку.
- **Почему это ошибка:** Пустые заявки искажают анализ рыночной глубины и ликвидности, так как предполагается, что каждый уровень содержит активные заявки.
- **Последствия:** Это может привести к неверной оценке доступного объёма на рынке.

## 5. Нарушения порядка в стакане (Order Book Order Violations)

- **Ошибки:**
  - 📊 Цены в стакане неупорядочены или равны: `px_buy_1 vs px_buy_2`, `px_buy_9 vs px_buy_10`, `px_sell_1 vs px_sell_2`–`px_sell_7 vs px_sell_8`.
  - 📊 Более высокий уровень стакана `px_buy_2` заполнен, в то время как `px_buy_1` пуст.
  - 📊 Нулевой объем на уровне 6, но положительный объем на уровне 7 для стороны buy.
- **Что происходит:**
  - Цены покупки должны быть строго убывающими (`px_buy_1 > px_buy_2`), а цены продажи — строго возрастающими (`px_sell_1 < px_sell_2`). Равенство или нарушение порядка указывает на некорректное обновление стакана.
  - Заполненные более глубокие уровни (например, `px_buy_2`) при пустых ближних уровнях (`px_buy_1`) нарушают структуру стакана.
  - Нулевой объём на уровне 6 при ненулевом объёме на уровне 7 также указывает на несогласованность.
- **Почему это ошибка:** Неправильный порядок или пустые ближние уровни искажают лучшие ставки и предложения, влияя на расчёт спреда.
- **Последствия:** Это может привести к неверным торговым сигналам и ошибкам в анализе рынка.

## 6. Сделки вне спреда (Trades Outside the Spread)

- **Ошибка:**
  - 💱 Сделки выполнены вне спреда.
  - 💱 Отрицательный или нулевой спред (`px_sell_1 <= px_buy_1`).
- **Что происходит:** Сделки должны происходить внутри спреда (между `px_buy_1` и `px_sell_1`). Сделки вне этого диапазона или нулевой/отрицательный спред (когда `px_sell_1 <= px_buy_1`) указывают на аномалию, возможно, из-за ошибок данных или экстремальных рыночных событий.
- **Почему это ошибка:** Такие аномалии не соответствуют нормальной рыночной динамике и могут быть вызваны повреждением данных.
- **Последствия:** Это может искажать процесс ценообразования и расчёты волатильности.

## 7. Логические несоответствия в сделках (Logical Inconsistencies in Trades)

- **Ошибки:**
  - 💼 `trade_amt` > 0, но `trade_cnt` == 0.
  - 💼 Отрицательные значения `trade_cnt`.
- **Что происходит:**
  - Положительный объём сделки (`trade_amt > 0`) при нулевом количестве сделок (`trade_cnt == 0`) логически противоречив.
  - Отрицательное количество сделок (`trade_cnt < 0`) недопустимо, так как сделки не могут быть отрицательными.
- **Почему это ошибка:** Эти несоответствия указывают на ошибки в агрегации или записи данных.
- **Последствия:** Это может привести к неверным расчётам торговой активности и объёмов.

## 8. Неправильные значения trade_px при trade_cnt > 0 (Incorrect trade_px when trade_cnt > 0)

- **Ошибка:**
  - 🔁 `trade_cnt` > 0, но `trade_px` == 0.
- **Что происходит:** Если есть сделки (`trade_cnt > 0`), цена сделки (`trade_px`) должна быть положительной. Нулевая цена указывает на ошибку данных.
- **Почему это ошибка:** Сделки должны иметь ненулевую цену для корректного анализа.
- **Последствия:** Это может искажать расчёты средней цены сделок и общей стоимости.

## 9. Временные аномалии (Temporal Anomalies)

- **Ошибки:**
  - 📈 `exchHostTime` не является монотонно возрастающим.
  - 📈 `adapterTime` не является монотонно возрастающим.
  - 📈 `exchHostTime` содержит нулевые или отрицательные временные метки.
  - 📈 `exchHostTime` имеет подозрительно большие временные разрывы.
  - 📈 `adapterTime` имеет подозрительно большие временные разрывы.
  - ♻️ `exchHostTime` повторяется в >90% строк (возможная заморозка фида).
  - ♻️ Значение в `px_buy_1` повторяется в >90% строк (возможная заморозка фида).
  - ♻️ Значение в `px_sell_1` повторяется в >90% строк (возможная заморозка фида).
  - ⏳ `adapterTime` раньше, чем `exchHostTime`.
  - ⏳ Большое отклонение (>5с) между `adapterTime` и `exchHostTime`.
- **Что происходит:**
  - Немонотонные временные метки нарушают хронологию событий, необходимую для анализа.
  - Нулевые или отрицательные метки в `exchHostTime` указывают на сбой синхронизации.
  - Большие временные разрывы (выше среднего + 5σ) могут быть вызваны задержками или потерей данных.
  - Повторяющиеся метки или цены в >90% строк указывают на возможную "заморозку" данных, когда обновления не поступают.
  - `adapterTime` раньше `exchHostTime` или с большим отклонением (>5 секунд) указывает на проблемы синхронизации между биржей и адаптером.
- **Почему это ошибка:** Временные метки должны быть последовательными и точными для анализа временных рядов.
- **Последствия:** Это может нарушить порядок событий, искажая анализ и торговые решения.

## 10. Неверные значения в поле type (Incorrect Values in 'type' Field)

- **Ошибка:**
  - 📎 Неизвестные значения в колонке `type`.
- **Что происходит:** Колонка `type` должна содержать только значения 4 (сделки) или 6 (обновления стакана). Другие значения указывают на повреждение данных или изменение формата.
- **Почему это ошибка:** Неправильные типы сообщений нарушают их обработку.
- **Последствия:** Это может привести к пропускам данных или их неверной интерпретации.

## 11. Дубликаты (Duplicates)

- **Ошибки:**
  - 🧩 Полностью дублирующиеся строки.
  - 🧩 Дублирующиеся значения `msgSeqNum` для типа 4.
  - 🧩 Дублирующиеся строки с одинаковыми `msgSeqNum` и `exchHostTime`.
  - 🔢 Пропуски или дубликаты в `msgSeqNum` для типа 4.
  - 🔢 Пропуски или дубликаты в `msgSeqNum` для типа 6.
- **Что происходит:** Дублирующиеся строки или номера последовательности (`msgSeqNum`) указывают на повторную запись сообщений. Пропуски в `msgSeqNum` могут означать потерю данных.
- **Почему это ошибка:** Каждое сообщение должно быть уникальным, особенно для `msgSeqNum`, чтобы обеспечить целостность данных.
- **Последствия:** Дубликаты завышают торговую активность, а пропуски могут привести к потере важных событий.

## 12. Логические несоответствия в сделках и стакане (Logical Inconsistencies in Trades and Order Book)

- **Ошибки:**
  - 📎 Строки типа 6 (обновление стакана) с ненулевыми `trade_px` или `trade_amt`.
  - 📐 `trade_amt` не соответствует ожидаемой логике для ненулевых сделок.
- **Что происходит:**
  - Сообщения типа 6 (обновления стакана) не должны содержать данных о сделках (`trade_px`, `trade_amt`), так как они предназначены только для обновления лимитного стакана.
  - Несоответствие `trade_amt` логике (например, ненулевой `trade_amt` при отсутствии других условий сделки) указывает на ошибку агрегации.
- **Почему это ошибка:** Это нарушает ожидаемую структуру сообщений и логику данных.
- **Последствия:** Это может привести к неверной интерпретации данных о сделках и обновлениях стакана.

## 13. Дополнительные возможные ошибки

- **Ошибки, связанные с протоколом FIX:**
  - **Отсутствующие теги:** Отсутствие обязательных тегов в сообщениях FIX может привести к неполным данным.
  - **Неправильная контрольная сумма:** Некорректная контрольная сумма (тег 10) указывает на повреждение сообщения при передаче.
  - **Пропуски в номерах последовательности:** Пропуски в `msgSeqNum` могут указывать на потерянные сообщения.
- **Что происходит:** Если данные основаны на протоколе FIX, эти ошибки могут возникать из-за проблем с форматированием или передачей сообщений.
- **Почему это ошибка:** Такие ошибки нарушают целостность данных, необходимую для точной обработки.
- **Последствия:** Это может привести к потере данных или их неверной интерпретации.

- **Проблемы с `moreTradesInBatch`:**
  - **Что происходит:** Колонка `moreTradesInBatch` имеет много NaN значений, что может быть нормальным, если информация недоступна, но может указывать на неполное заполнение данных.
  - **Почему это может быть проблемой:** Пропуски могут повлиять на анализы, зависящие от этой информации, например, на определение пакетов сделок.
  - **Последствия:** Это может ограничить точность анализа торговой активности.

- **Глубина стакана:**
  - **Что происходит:** Набор данных имеет до 10 уровней, что кажется последовательным, но возможны проблемы, если более глубокие уровни заполнены, а ближние пусты.
  - **Почему это может быть ошибкой:** Это может указывать на некорректное обновление стакана.
  - **Последствия:** Это может искажать анализ рыночной глубины.

## Заключение

Я написал небольшой скрипт выявляющий широкий спектр ошибок, охватывающих:

- проблемы с типами данных, значениями, временными метками, логикой сделок и структурой стакана.

Скрипт выявил 110 уникальных типов ошибок, которые были сгруппированы в 13 логических категорий для структурированного анализа. Каждая категория охватывает ошибки, связанные с определёнными аспектами данных, такими как типы данных, значения, временные метки, структура стакана и логика сделок. Этот подход позволяет выявить широкий спектр аномалий, критически важных для обеспечения надежности торговых систем. Дополнительные проверки, такие как анализ целостности сообщений FIX или согласованности глубины стакана, могут быть добавлены для ещё большей полноты, но текущий анализ уже демонстрирует высокую эффективность.

# Чуть более подробно по ошибкам ->

## 📋 Обнаруженные типы ошибок

    - ⏳ adapterTime раньше, чем exchHostTime
    - ⏳ Большое отклонение (>5с) между adapterTime и exchHostTime
    - ♻️ exchHostTime повторяется в >90% строк (возможная заморозка фида)
    - ♻️ Значение в px_buy_1 повторяется в >90% строк (возможная заморозка фида)
    - ♻️ Значение в px_sell_1 повторяется в >90% строк (возможная заморозка фида)
    - ❓ NaN значения в обязательной колонке 'amt_buy_1'
    - ❓ NaN значения в обязательной колонке 'amt_buy_10'
    - ❓ NaN значения в обязательной колонке 'amt_buy_2'
    - ❓ NaN значения в обязательной колонке 'amt_buy_3'
    - ❓ NaN значения в обязательной колонке 'amt_buy_4'
    - ❓ NaN значения в обязательной колонке 'amt_buy_5'
    - ❓ NaN значения в обязательной колонке 'amt_buy_6'
    - ❓ NaN значения в обязательной колонке 'amt_buy_7'
    - ❓ NaN значения в обязательной колонке 'amt_buy_8'
    - ❓ NaN значения в обязательной колонке 'amt_buy_9'
    - ❓ NaN значения в обязательной колонке 'px_buy_1'
    - ❓ Несогласованный NaN: цена NaN, но объем не NaN в px_buy_1/amt_buy_1
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_1/amt_buy_1
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_10/amt_buy_10
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_2/amt_buy_2
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_3/amt_buy_3
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_4/amt_buy_4
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_5/amt_buy_5
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_6/amt_buy_6
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_7/amt_buy_7
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_8/amt_buy_8
    - ❓ Несогласованный NaN: цена не NaN, но объем NaN в px_buy_9/amt_buy_9
    - 💱 Отрицательный или нулевой спред (px_sell_1 <= px_buy_1)
    - 💱 Сделки выполнены вне спреда
    - 💼 trade_amt > 0, но trade_cnt == 0
    - 💼 Отрицательные значения trade_cnt
    - 📈 adapterTime имеет подозрительно большие временные разрывы
    - 📈 adapterTime не является монотонно возрастающим
    - 📈 exchHostTime имеет подозрительно большие временные разрывы
    - 📈 exchHostTime не является монотонно возрастающим
    - 📈 exchHostTime содержит нулевые или отрицательные временные метки
    - 📈 Экстремальные значения в колонке 'amt_buy_1' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_10' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_2' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_3' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_4' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_5' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_6' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_7' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_8' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_buy_9' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_1' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_10' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_2' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_3' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_4' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_5' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_6' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_7' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_8' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'amt_sell_9' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_1' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_10' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_2' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_3' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_4' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_5' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_6' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_7' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_8' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'px_buy_9' (z-score > 5)
    - 📈 Экстремальные значения в колонке 'trade_amt' (z-score > 5)
    - 📉 Нулевой объем с ненулевой ценой в px_buy_6
    - 📉 Отрицательные значения объема в колонке 'amt_buy_1'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_10'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_2'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_3'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_4'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_5'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_6'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_7'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_8'
    - 📉 Отрицательные значения объема в колонке 'amt_buy_9'
    - 📉 Отрицательные значения объема в колонке 'amt_sell_8'
    - 📉 Отрицательные значения объема в колонке 'trade_amt'
    - 📉 Отрицательные значения цены в колонке 'px_buy_9'
    - 📉 Цена в колонке 'px_buy_1' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_10' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_2' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_3' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_4' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_5' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_6' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_7' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_8' имеет более двух знаков после запятой
    - 📉 Цена в колонке 'px_buy_9' имеет более двух знаков после запятой
    - 📊 Более высокий уровень стакана px_buy_2 заполнен, в то время как px_buy_1 пуст
    - 📊 Нулевой объем на уровне 6, но положительный объем на уровне 7 для стороны buy
    - 📊 Цены в стакане неупорядочены или равны: px_buy_1 vs px_buy_2
    - 📊 Цены в стакане неупорядочены или равны: px_buy_9 vs px_buy_10
    - 📊 Цены в стакане неупорядочены или равны: px_sell_1 vs px_sell_2
    - 📊 Цены в стакане неупорядочены или равны: px_sell_2 vs px_sell_3
    - 📊 Цены в стакане неупорядочены или равны: px_sell_3 vs px_sell_4
    - 📊 Цены в стакане неупорядочены или равны: px_sell_4 vs px_sell_5
    - 📊 Цены в стакане неупорядочены или равны: px_sell_5 vs px_sell_6
    - 📊 Цены в стакане неупорядочены или равны: px_sell_6 vs px_sell_7
    - 📊 Цены в стакане неупорядочены или равны: px_sell_7 vs px_sell_8
    - 📎 Строки типа 6 (обновление стакана) с ненулевыми trade_px или trade_amt
    - 📐 trade_amt не соответствует ожидаемой логике для ненулевых сделок
    - 📛 Колонка 'px_sell_7' содержит нечисловые значения (должна быть float)
    - 🔢 Пропуски или дубликаты в msgSeqNum для типа 4
    - 🔢 Пропуски или дубликаты в msgSeqNum для типа 6
    - 🧩 Дублирующиеся значения msgSeqNum для типа 4
    - 🧩 Дублирующиеся строки с одинаковыми msgSeqNum и exchHostTime
    - 🧩 Полностью дублирующиеся строки

    ✅ Всего обнаружено уникальных типов ошибок: 110 -> условно можно разнести на 13 категорий.
