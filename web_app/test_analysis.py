import pandas as pd
import numpy as np
from analysis import calculate_kpis


def test_calculate_kpis_basic():
    """Тест базовой функциональности calculate_kpis с простыми данными."""
    # Создаем тестовые данные
    test_data = pd.DataFrame({
        'Дата': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02']),
        'Сумма': [100, 200, 300],
        'Город': ['Москва', 'СПб', 'Москва']  # Дополнительная колонка
    })
    
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(test_data)
    
    # Проверяем результаты
    assert total_sales == 600  # 100 + 200 + 300
    assert avg_daily_sales == 300  # (300 + 300) / 2 дней
    assert max_daily_sales == 300  # Максимальные ежедневные продажи


def test_calculate_kpis_empty_dataframe():
    """Тест функции calculate_kpis с пустым DataFrame."""
    empty_df = pd.DataFrame(columns=['Дата', 'Сумма'])
    
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(empty_df)
    
    # Все значения должны быть равны 0
    assert total_sales == 0
    assert avg_daily_sales == 0
    assert max_daily_sales == 0


def test_calculate_kpis_none_dataframe():
    """Тест функции calculate_kpis с None в качестве аргумента."""
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(None)
    
    # Все значения должны быть равны 0
    assert total_sales == 0
    assert avg_daily_sales == 0
    assert max_daily_sales == 0


def test_calculate_kpis_with_missing_values():
    """Тест функции calculate_kpis с пропущенными значениями."""
    # Создаем тестовые данные с пропущенными значениями
    test_data = pd.DataFrame({
        'Дата': pd.to_datetime(['2023-01-01', '2023-01-01', '2023-01-02', pd.NaT]),
        'Сумма': [100, 200, 300, np.nan],
        'Город': ['Москва', 'СПб', 'Москва', 'Екат']  # Дополнительная колонка
    })
    
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(test_data)
    
    # Пропущенные значения должны быть исключены из расчетов
    assert total_sales == 600  # Только 100 + 200 + 300 (np.nan и NaT исключены)
    assert avg_daily_sales == 300  # (300 + 300) / 2 дней
    assert max_daily_sales == 300  # Максимальные ежедневные продажи


def test_calculate_kpis_single_day():
    """Тест функции calculate_kpis с данными за один день."""
    test_data = pd.DataFrame({
        'Дата': pd.to_datetime(['2023-01-01', '2023-01-01']),
        'Сумма': [100, 200]
    })
    
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(test_data)
    
    assert total_sales == 300  # 100 + 200
    assert avg_daily_sales == 300  # 300 / 1 день
    assert max_daily_sales == 300  # Максимальные ежедневные продажи


def test_calculate_kpis_missing_required_columns():
    """Тест функции calculate_kpis с отсутствующими обязательными колонками."""
    # DataFrame без колонки 'Сумма'
    test_data_no_amount = pd.DataFrame({
        'Дата': pd.to_datetime(['2023-01-01']),
        'Город': ['Москва']
    })
    
    # Проверяем, что выбрасывается исключение
    try:
        calculate_kpis(test_data_no_amount)
        assert False, "Ожидалось исключение ValueError для отсутствующей колонки 'Сумма'"
    except ValueError as e:
        assert "DataFrame должен содержать колонку 'Сумма'" in str(e)
    
    # DataFrame без колонки 'Дата'
    test_data_no_date = pd.DataFrame({
        'Сумма': [100],
        'Город': ['Москва']
    })
    
    # Проверяем, что выбрасывается исключение
    try:
        calculate_kpis(test_data_no_date)
        assert False, "Ожидалось исключение ValueError для отсутствующей колонки 'Дата'"
    except ValueError as e:
        assert "DataFrame должен содержать колонку 'Дата'" in str(e)


def test_calculate_kpis_only_missing_values():
    """Тест функции calculate_kpis когда все значения в обязательных колонках пропущены."""
    # DataFrame с только пропущенными значениями в обязательных колонках
    test_data = pd.DataFrame({
        'Дата': [pd.NaT, pd.NaT],
        'Сумма': [np.nan, np.nan]
    })
    
    total_sales, avg_daily_sales, max_daily_sales = calculate_kpis(test_data)
    
    # После удаления строк с пропущенными значениями DataFrame становится пустым
    assert total_sales == 0
    assert avg_daily_sales == 0
    assert max_daily_sales == 0