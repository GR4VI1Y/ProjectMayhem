import streamlit as st
try:
    import plotly.express as px
except ImportError:
    px = None
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
    # Явно преобразуем дату в тип date и создаем копию DataFrame для безопасности
    df_copy = df.copy()
    df_copy['Дата_только'] = df_copy['Дата'].dt.date
    
    # Группируем по дате и суммируем продажи, убедившись, что используем только 'Сумма'
    daily_sales_grouped = df_copy.groupby('Дата_только')['Сумма'].sum().reset_index()
    daily_sales_grouped.columns = ['Дата', 'Сумма']
    
    # Сортируем по дате
    daily_sales_sorted = daily_sales_grouped.sort_values('Дата').reset_index(drop=True)
    
    # Проверяем результат агрегации
    print(f"DEBUG: Результат агрегации - строки: {len(daily_sales_sorted)}, пример значений: {daily_sales_sorted.head()}")
    
    # Переводы для графика
    titles = {
        'русский': {'title': 'Продажи по дням', 'x_axis': 'Дата', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales Over Time', 'x_axis': 'Date', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '销售趋势', 'x_axis': '日期', 'y_axis': '销售额'}
    }
    
    selected_lang = titles.get(lang, titles['русский'])
    
    # Создание линейного графика с использованием явных данных
    if px is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
        
    fig = px.line(
        x=daily_sales_sorted['Дата'],
        y=daily_sales_sorted['Сумма'],
        title=selected_lang['title'],
        labels={'x': selected_lang['x_axis'], 'y': selected_lang['y_axis']},
        markers=True
    )
    
    # Настройка осей и меток
    fig.update_xaxes(title_text=selected_lang['x_axis'])
    fig.update_yaxes(title_text=selected_lang['y_axis'])
    
    return fig
    
    # Настройка внешнего вида графика
    fig.update_layout(
        xaxis_title=selected_lang['x_axis'],
        yaxis_title=selected_lang['y_axis'],
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
    city_sales = df.groupby('Город')['Сумма'].sum().reset_index()
    city_sales = city_sales.sort_values('Сумма', ascending=False)
    
    # Переводы для графика
    titles = {
        'русский': {'title': 'Продажи по городам', 'x_axis': 'Город', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales by City', 'x_axis': 'City', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '按城市划分的销售额', 'x_axis': '城市', 'y_axis': '销售额'}
    }
    
    selected_lang = titles.get(lang, titles['русский'])
    
    # Создание столбчатого графика
    if px is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
        
    fig = px.bar(
        city_sales,
        x='Город',
        y='Сумма',
        title=selected_lang['title'],
        labels={'Город': selected_lang['x_axis'], 'Сумма': selected_lang['y_axis']}
    )
    
    # Настройка внешнего вида графика
    fig.update_layout(
        xaxis_title=selected_lang['x_axis'],
        yaxis_title=selected_lang['y_axis'],
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
    
    # Добавляем колонку с днями недели
    df_copy['ДеньНедели'] = df_copy['Дата'].dt.day_name()
    
    # Соответствие дней недели на разных языках
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
    df_copy['ДеньНеделиЛок'] = df_copy['ДеньНедели'].map(selected_mapping)
    
    # Явно группируем по дням недели и суммируем продажи
    dow_sales_grouped = df_copy.groupby('ДеньНеделиЛок')['Сумма'].sum().reindex([
        selected_mapping['Monday'],
        selected_mapping['Tuesday'],
        selected_mapping['Wednesday'],
        selected_mapping['Thursday'],
        selected_mapping['Friday'],
        selected_mapping['Saturday'],
        selected_mapping['Sunday']
    ]).reset_index()
    
    # Переименовываем колонки
    dow_sales_grouped.columns = ['ДеньНеделиЛок', 'Сумма']
    dow_sales_clean = dow_sales_grouped.dropna()  # Удаление NaN значений
    
    # Переводы для графика
    titles = {
        'русский': {'title': 'Продажи по дням недели', 'x_axis': 'День недели', 'y_axis': 'Сумма продаж'},
        'английский': {'title': 'Sales by Day of Week', 'x_axis': 'Day of Week', 'y_axis': 'Sales Amount'},
        'китайский': {'title': '按星期划分的销售额', 'x_axis': '星期', 'y_axis': '销售额'}
    }
    
    selected_lang = titles.get(lang, titles['русский'])
    
    # Создание столбчатого графика с использованием явных данных
    if px is None:
        st.error("Plotly не установлен. Пожалуйста, установите plotly для использования этой функции.")
        return None
        
    fig = px.bar(
        x=dow_sales_clean['ДеньНеделиЛок'],
        y=dow_sales_clean['Сумма'],
        title=selected_lang['title'],
        labels={'x': selected_lang['x_axis'], 'y': selected_lang['y_axis']}
    )
    
    # Настройка внешнего вида графика
    fig.update_xaxes(title_text=selected_lang['x_axis'])
    fig.update_yaxes(title_text=selected_lang['y_axis'])
    
    return fig