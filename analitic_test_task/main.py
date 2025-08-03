from pathlib import Path

import pandas as pd

BASE_DIR = Path(__file__).resolve().parent
path = BASE_DIR / "test.feather"

df = pd.read_feather(path)

# Общая информация по DataFrame
print("📌 Общая информация:")
print(df.info())

# Статистика по числовым колонкам (описательная статистика)
print("\n📊 Описательная статистика по числовым колонкам:")
print(df.describe())

# Статистика по объектным колонкам — уникальные значения, топ и частота
print("\n📋 Статистика по объектным колонкам:")
obj_cols = df.select_dtypes(include=["object"]).columns
for col in obj_cols:
    print(f"\n- Колонка: {col}")
    print(df[col].value_counts(dropna=False).head(10))

# Проверка уникальных значений в categorical-like колонках (int, float с небольшим числом уникальных)
print("\n🔍 Колонки с небольшим числом уникальных значений (<= 30 уникальных):")
for col in df.columns:
    nunique = df[col].nunique(dropna=False)
    if nunique <= 30:
        print(f"  {col} (уникальных значений: {nunique}) -> {df[col].unique()}")

# Вывод верхних и нижних 10 строк для быстрой проверки трендов и аномалий
print("\n⬆️ Верхние 50 строк:")
print(df.head(50))

print("\n⬇️ Нижние 50 строк:")
print(df.tail(50))

# Пример выборки строк с NaN для оценки их распределения
print("\n❓ Несколько строк с NaN (если есть):")
nan_rows = df[df.isnull().any(axis=1)]
print(nan_rows.head(20) if not nan_rows.empty else "Нет строк с NaN")

# Вывод частоты значений для колонки 'type' (часто важна для логики)
if "type" in df.columns:
    print("\n📦 Распределение значений колонки 'type':")
    print(df["type"].value_counts(dropna=False))

# Временные метки: минимумы, максимумы, диапазон
if {"exchHostTime", "adapterTime"}.issubset(df.columns):
    print("\n⏰ Временные метки:")
    for col in ["exchHostTime", "adapterTime"]:
        print(
            f"  {col}: min={df[col].min()}, max={df[col].max()}, count={df[col].count()}"
        )
