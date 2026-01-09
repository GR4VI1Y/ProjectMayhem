import pandas as pd


def validate_data_frame(df: pd.DataFrame) -> bool:
    """
    Проверяет, что DataFrame не пустой и содержит необходимые колонки.

    Args:
        df: DataFrame для проверки

    Returns:
        bool: True если DataFrame валиден, иначе False
    """
    if df is None or df.empty:
        return False

    required_columns = ["Дата", "Сумма"]
    for col in required_columns:
        if col not in df.columns:
            raise ValueError(f"DataFrame должен содержать колонку '{col}'")

    return True


def clean_sales_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Удаляет строки с пропущенными значениями в нужных колонках.

    Args:
        df: Исходный DataFrame

    Returns:
        pd.DataFrame: Очищенный DataFrame
    """
    return df.dropna(subset=["Дата", "Сумма"])


def calculate_total_sales(sales_data: pd.DataFrame) -> float:
    """
    Вычисляет общую сумму продаж.

    Args:
        sales_data: DataFrame с данными о продажах

    Returns:
        float: Общая сумма продаж
    """
    return sales_data["Сумма"].sum()


def calculate_daily_sales(sales_data: pd.DataFrame) -> pd.Series:
    """
    Группирует продажи по дате и вычисляет сумму продаж за каждый день.

    Args:
        sales_data: DataFrame с данными о продажах

    Returns:
        pd.Series: Продажи по дням
    """
    return sales_data.groupby(sales_data["Дата"].dt.date)["Сумма"].sum()


def calculate_average_daily_sales(daily_sales: pd.Series) -> float:
    """
    Вычисляет средние ежедневные продажи.

    Args:
        daily_sales: Series с ежедневными продажами

    Returns:
        float: Средние ежедневные продажи
    """
    return daily_sales.mean() if len(daily_sales) > 0 else 0


def calculate_maximum_daily_sales(daily_sales: pd.Series) -> float:
    """
    Вычисляет максимальные ежедневные продажи.

    Args:
        daily_sales: Series с ежедневными продажами

    Returns:
        float: Максимальные ежедневные продажи
    """
    return daily_sales.max() if len(daily_sales) > 0 else 0


def calculate_kpi_metrics(df: pd.DataFrame) -> tuple:
    """
    Вычисляет основные метрики KPI на основе данных о продажах.

    Args:
        df: DataFrame с данными о продажах, содержащий колонки 'Дата' и 'Сумма'

    Returns:
        tuple: Кортеж из трех значений: (общая сумма продаж, средние ежедневные
               продажи, максимальные ежедневные продажи)
    """
    # Проверяем, что DataFrame валиден
    if not validate_data_frame(df):
        return (0, 0, 0)

    # Очищаем данные
    cleaned_data = clean_sales_data(df)

    if cleaned_data.empty:
        return (0, 0, 0)

    # Вычисляем общую сумму продаж
    total_sales = calculate_total_sales(cleaned_data)

    # Вычисляем ежедневные продажи
    daily_sales = calculate_daily_sales(cleaned_data)

    # Вычисляем средние и максимальные ежедневные продажи
    avg_daily_sales = calculate_average_daily_sales(daily_sales)
    max_daily_sales = calculate_maximum_daily_sales(daily_sales)

    return (total_sales, avg_daily_sales, max_daily_sales)


# Алиас для функции, чтобы соответствовать описанию в задании
calculate_kpis = calculate_kpi_metrics
