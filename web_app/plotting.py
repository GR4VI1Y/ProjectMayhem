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
    # Создаем копию DataFrame для безопасности
    df_copy = df.copy()
    
    # Преобразуем дату к формату date
    df_copy['Дата_только'] = df_copy['Дата'].dt.date
    
    # Группируем по дате и суммируем продажи
    grouped_data = df_copy.groupby('Дата_только')['Сумма'].agg('sum').reset_index()
    grouped_data = grouped_data.rename(columns={'Дата_только': 'Дата'})
    grouped_data = grouped_data.sort_values('Дата').reset_index(drop=True)
    
    print(f"DEBUG create_sales_over_time_plot: данные для графика - {len(grouped_data)} строк")
    print(f"Пример значений: {grouped_data[['Дата', 'Сумма']].head()}")
    
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
        x=grouped_data['Дата'],
        y=grouped_data['Сумма'],
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
    df_copy['ДеньНедели'] = df_copy['Дата'].dt.day_name()
    df_copy['ДеньНеделиЛок'] = df_copy['ДеньНедели'].map(selected_mapping)
    
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
    dow_sales = df_copy.groupby('ДеньНеделиЛок')['Сумма'].agg('sum').reindex(ordered_days, fill_value=0).reset_index()
    
    print(f"DEBUG create_day_of_week_plot: данные для графика - {len(dow_sales)} строк")
    print(f"Пример значений: {dow_sales[['ДеньНеделиЛок', 'Сумма']].head()}")
    
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
        x=dow_sales['ДеньНеделиЛок'],
        y=dow_sales['Сумма'],
        name='Продажи'
    ))
    
    fig.update_layout(
        title=selected_title['title'],
        xaxis_title=selected_title['x_axis'],
        yaxis_title=selected_title['y_axis']
    )
    
    return fig