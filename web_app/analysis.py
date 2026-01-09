import pandas as pd


def calculate_kpi_metrics(df: pd.DataFrame) -> tuple:
    """
    Вычисляет основные метрики KPI на основе данных о продажах.

    Args:
        df: DataFrame с данными о продажах, содержащий колонки 'Дата' и 'Сумма'

    Returns:
        Кортеж из трех значений: (общая сумма продаж, средние ежедневные
        продажи, максимальные ежедневные продажи)
    """
    # Проверяем, что DataFrame не пустой
    if df is None or df.empty:
        return (0, 0, 0)

    # Проверяем наличие необходимых колонок
    required_columns = ["Дата", "Сумма"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"DataFrame должен содержать колонку '{col}'")

    pass  # Больше не нужно проверять все колонки, т.к. это делается в app.py

    # Удаляем строки с пропущенными значениями в нужных колонках
    df_clean = df.dropna(subset=["Дата", "Сумма"])

    if df_clean.empty:
        return (0, 0, 0)

    # Вычисляем общую сумму продаж
    total_sales = df_clean["Сумма"].sum()

    # Вычисляем ежедневные продажи
    daily_sales = df_clean.groupby(df_clean["Дата"].dt.date)["Сумма"].sum()

    # Вычисляем средние ежедневные продажи
    avg_daily_sales = daily_sales.mean() if len(daily_sales) > 0 else 0

    # Вычисляем максимальные ежедневные продажи
    max_daily_sales = daily_sales.max() if len(daily_sales) > 0 else 0

    return (total_sales, avg_daily_sales, max_daily_sales)


# Алиас для функции, чтобы соответствовать описанию в задании
calculate_kpis = calculate_kpi_metrics
