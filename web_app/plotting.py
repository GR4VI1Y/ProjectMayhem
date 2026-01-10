import streamlit as st
try:
    import plotly.express as px
    import plotly.graph_objects as go
except ImportError:
    px = None
    go = None
import pandas as pd


def create_sales_over_time_plot(df: pd.DataFrame, lang: str = 'русский') -> object:
    """
    Создает интерактивный график продаж по дням.
    
    Args:
        df: DataFrame с данными о продажах
        lang: Язык для отображения (по умолчанию 'русский')
        
    Returns:
        Объект Plotly с графиком
    """
    print(f"DEBUG create_sales_over_time_plot: входящий DataFrame - {len(df)} строк, колонки: {list(df.columns)}")
    print(f"Пример входных данных: {df[['Дата', 'Сумма']].head()}")
    
    # Создаем копию DataFrame для безопасности
    df_copy = df.copy()
    
    # Преобразуем дату к формату date
    df_copy['date_only'] = df_copy['Дата'].dt.date
    print(f"DEBUG: после добавления 'date_only' - пример: {df_copy[['Дата', 'date_only', 'Сумма']].head()}")
    
    # Группируем по дате и суммируем продажи
    grouped_data = df_copy.groupby('date_only')['Сумма'].agg('sum').reset_index()
    print(f"DEBUG: после groupby и agg - {len(grouped_data)} строк, пример: {grouped_data.head()}")
    
    # Переименовываем колонки с уникальными именами, чтобы избежать конфликта
    grouped_data = grouped_data.rename(columns={'date_only': 'plot_date', 'Сумма': 'plot_amount'})
    grouped_data = grouped_data.sort_values('plot_date').reset_index(drop=True)
    print(f"DEBUG: после сортировки - пример: {grouped_data[['plot_date', 'plot_amount']].head()}")
    print(f"DEBUG: типы данных - {grouped_data.dtypes}")
    
    # Определяем заголовки в зависимости от языка
    titles = {
        'русский': {'title': 'Продажи по дням', 'x_axis': 'Дата', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales Over Time', 'x_axis': 'Date', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '销售趋势', 'x_axis': '日期', 'y_axis': '销售额'}
    }
    selected_title = titles.get(lang, titles['русский'])
    
    # Создаем график с явным указанием данных для осей
    if go is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=grouped_data['plot_date'],
        y=grouped_data['plot_amount'],
        mode='lines+markers',
        name='Продажи'
    ))
    
    fig.update_layout(
        title=selected_title['title'],
        xaxis_title=selected_title['x_axis'],
        yaxis_title=selected_title['y_axis'],
        hovermode='x unified'
    )
    
    return fig


def create_city_sales_plot(df: pd.DataFrame, lang: str = 'русский') -> object:
    """
    Создает график продаж по городам.
    
    Args:
        df: DataFrame с данными о продажах
        lang: Язык для отображения (по умолчанию 'русский')
        
    Returns:
        Объект Plotly с графиком
    """
    # Агрегирование данных по городам
    city_sales = df.groupby('Город')['Сумма'].agg('sum').reset_index()
    city_sales = city_sales.sort_values('Сумма', ascending=False)
    
    # Переводы для графика
    titles = {
        'русский': {'title': 'Продажи по городам', 'x_axis': 'Город', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales by City', 'x_axis': 'City', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '按城市划分的销售额', 'x_axis': '城市', 'y_axis': '销售额'}
    }
    
    selected_title = titles.get(lang, titles['русский'])
    
    # Создание столбчатого графика
    if px is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
        
    fig = px.bar(
        city_sales,
        x='Город',
        y='Сумма',
        title=selected_title['title']
    )
    
    # Настройка внешнего вида графика
    fig.update_layout(
        xaxis_title=selected_title['x_axis'],
        yaxis_title=selected_title['y_axis'],
        xaxis_tickangle=-45
    )
    
    return fig


def create_day_of_week_plot(df: pd.DataFrame, lang: str = 'русский') -> object:
    """
    Создает график продаж по дням недели.
    
    Args:
        df: DataFrame с данными о продажах
        lang: Язык для отображения (по умолчанию 'русский')
        
    Returns:
        Объект Plotly с графиком
    """
    print(f"DEBUG create_day_of_week_plot: входящий DataFrame - {len(df)} строк, колонки: {list(df.columns)}")
    print(f"Пример входных данных: {df[['Дата', 'Сумма']].head()}")
    
    # Создаем копию DataFrame для безопасности
    df_copy = df.copy()
    
    # Определяем дни недели
    day_mapping = {
        'русский': {
            'Monday': 'Понедельник',
            'Tuesday': 'Вторник', 
            'Wednesday': 'Среда',
            'Thursday': 'Четверг',
            'Friday': 'Пятница',
            'Saturday': 'Суббота',
            'Sunday': 'Воскресенье'
        },
        'английский': {
            'Monday': 'Monday',
            'Tuesday': 'Tuesday',
            'Wednesday': 'Wednesday',
            'Thursday': 'Thursday',
            'Friday': 'Friday',
            'Saturday': 'Saturday',
            'Sunday': 'Sunday'
        },
        'китайский': {
            'Monday': '星期一',
            'Tuesday': '星期二',
            'Wednesday': '星期三',
            'Thursday': '星期四',
            'Friday': '星期五',
            'Saturday': '星期六',
            'Sunday': '星期日'
        }
    }
    
    selected_mapping = day_mapping.get(lang, day_mapping['русский'])
    
    # Добавляем колонку с днями недели
    df_copy['day_of_week_eng'] = df_copy['Дата'].dt.day_name()
    df_copy['day_of_week_local'] = df_copy['day_of_week_eng'].map(selected_mapping)
    print(f"DEBUG: пример сопоставления дней недели: {df_copy[['Дата', 'day_of_week_eng', 'day_of_week_local', 'Сумма']].head()}")
    
    # Создаем полный список дней недели в правильном порядке
    ordered_days = [
        selected_mapping['Monday'],
        selected_mapping['Tuesday'],
        selected_mapping['Wednesday'],
        selected_mapping['Thursday'],
        selected_mapping['Friday'],
        selected_mapping['Saturday'],
        selected_mapping['Sunday']
    ]
    
    # Группируем по дням недели и суммируем продажи
    grouped_by_day = df_copy.groupby('day_of_week_local')['Сумма'].agg('sum')
    print(f"DEBUG: результат groupby до reindex - {len(grouped_by_day)} строк: {grouped_by_day}")
    
    # Используем reindex для правильного порядка дней недели
    dow_sales = grouped_by_day.reindex(ordered_days, fill_value=0).reset_index()
    dow_sales = dow_sales.rename(columns={'day_of_week_local': 'plot_day', 'Сумма': 'plot_amount'})
    print(f"DEBUG: результат после reindex - {len(dow_sales)} строк, пример: {dow_sales}")
    
    # Переводы для графика
    titles = {
        'русский': {'title': 'Продажи по дням недели', 'x_axis': 'День недели', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales by Day of Week', 'x_axis': 'Day of Week', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '按星期划分的销售额', 'x_axis': '星期', 'y_axis': '销售额'}
    }
    
    selected_title = titles.get(lang, titles['русский'])
    
    # Создаем график с явным указанием данных для осей
    if go is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=dow_sales['plot_day'],
        y=dow_sales['plot_amount'],
        name='Продажи'
    ))
    
    fig.update_layout(
        title=selected_title['title'],
        xaxis_title=selected_title['x_axis'],
        yaxis_title=selected_title['y_axis']
    )
    
    return fig