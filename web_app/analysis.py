import streamlit as st
import pandas as pd
import numpy as np

def calculate_kpi_metrics(df: pd.DataFrame) -> tuple:
    """
    Рассчитывает основные метрики KPI для отображения.
    
    Args:
        df: DataFrame с данными о продажах
        
    Returns:
        tuple: (Общая сумма продаж, Средние ежедневные продажи, Максимальные ежедневные продажи)
    """
    if df.empty:
        return 0, 0
    
    # Общая сумма продаж
    total_sales = df['Сумма'].sum()
    
    # Средние ежедневные продажи
    daily_sales = df.groupby(df['Дата'].dt.date)['Сумма'].sum()
    avg_daily_sales = daily_sales.mean() if not daily_sales.empty else 0
    
    # Максимальные ежедневные продажи
    max_daily_sales = daily_sales.max() if not daily_sales.empty else 0
    
    return total_sales, avg_daily_sales, max_daily_sales

def calculate_sales_by_city(df: pd.DataFrame) -> pd.DataFrame:
    """
    Рассчитывает продажи по городам.
    
    Args:
        df: DataFrame с данными о продажах
        
    Returns:
        DataFrame с продажами по городам
    """
    city_sales = df.groupby('Город').agg({
        'Сумма': ['sum', 'mean', 'count']
    }).round(2)
    
    # Плоская структура колонок
    city_sales.columns = ['Общая_сумма', 'Средняя_сумма', 'Количество_транзакций']
    
    return city_sales.sort_values(by='Общая_сумма', ascending=False)

def calculate_sales_by_customer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Рассчитывает продажи по клиентам.
    
    Args:
        df: DataFrame с данными о продажах
        
    Returns:
        DataFrame с продажами по клиентам
    """
    # Создание полного имени клиента
    df['ПолноеИмя'] = df['Имя'] + ' ' + df['Фамилия']
    
    customer_sales = df.groupby('ПолноеИмя').agg({
        'Сумма': ['sum', 'mean', 'count']
    }).round(2)
    
    # Плоская структура колонок
    customer_sales.columns = ['Общая_сумма', 'Средняя_сумма', 'Количество_транзакций']
    
    return customer_sales.sort_values(by='Общая_сумма', ascending=False)

def find_sales_anomalies(df: pd.DataFrame, threshold: float = 2.0) -> pd.DataFrame:
    """
    Находит аномалии в продажах на основе отклонения от среднего.
    
    Args:
        df: DataFrame с данными о продажах
        threshold: Порог отклонения в стандартных отклонениях
        
    Returns:
        DataFrame с аномальными записями
    """
    if df.empty:
        return pd.DataFrame()
    
    # Расчет среднего и стандартного отклонения
    mean_amount = df['Сумма'].mean()
    std_amount = df['Сумма'].std()
    
    if std_amount == 0:
        return pd.DataFrame()
    
    # Определение аномалий
    df['Z_оценка'] = (df['Сумма'] - mean_amount) / std_amount
    anomalies = df[abs(df['Z_оценка']) > threshold]
    
    return anomalies[['Дата', 'Город', 'Имя', 'Фамилия', 'Сумма', 'Z_оценка']].copy()

def calculate_monthly_sales(df: pd.DataFrame) -> pd.DataFrame:
    """
    Рассчитывает ежемесячные продажи.
    
    Args:
        df: DataFrame с данными о продажах
        
    Returns:
        DataFrame с ежемесячными продажами
    """
    df['Месяц'] = df['Дата'].dt.to_period('M')
    monthly_sales = df.groupby('Месяц').agg({
        'Сумма': ['sum', 'mean', 'count']
    }).round(2)
    
    # Плоская структура колонок
    monthly_sales.columns = ['Общая_сумма', 'Средняя_сумма', 'Количество_транзакций']
    
    return monthly_sales