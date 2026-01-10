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
    # print(f"DEBUG create_sales_over_time_plot: Результат агрегации - строки: {len(daily_sales_sorted)}, пример значений:")
    # print(daily_sales_sorted.head())
    # print(f"Типы данных: {daily_sales_sorted.dtypes}")
    # print(f"Колонки: {daily_sales_sorted.columns.tolist()}")
    
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
    
    # Используем plotly.graph_objects для построения графика
    try:
        import plotly.graph_objects as go
        
        fig = go.Figure()
        # Преобразуем значения в числовой тип для уверенности
        y_values = pd.to_numeric(daily_sales_sorted['Сумма'], errors='coerce')
        fig.add_trace(go.Scatter(
            x=daily_sales_sorted['Дата'],
            y=y_values,
            mode='lines+markers',
            name='Продажи'
        ))
        
        fig.update_layout(
            title=selected_lang['title'],
            xaxis_title=selected_lang['x_axis'],
            yaxis_title=selected_lang['y_axis'],
            hovermode='x unified'
        )
        
        return fig
    except Exception as e:
        print(f"ERROR: Ошибка при создании графика: {e}")
        # Возвращаем график с использованием px.line с правильными данными в случае ошибки
        fig = px.line(
            daily_sales_sorted,
            x='Дата',
            y='Сумма',
            title=f"{selected_lang['title']} - ОШИБКА ОТЛАДКИ"
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
    dow_sales_grouped = df_copy.groupby('ДеньНеделиЛок')['Сумма'].sum().reset_index()
    
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
    
    # Сортируем по порядку дней недели, заполняя отсутствующие дни нулями
    dow_sales_grouped = dow_sales_grouped.set_index('ДеньНеделиЛок').reindex(ordered_days, fill_value=0).reset_index()
    dow_sales_grouped.columns = ['ДеньНеделиЛок', 'Сумма']
    dow_sales_clean = dow_sales_grouped  # Убираем dropna, так как теперь все дни присутствуют
    
    # print(f"DEBUG create_day_of_week_plot: Результат агрегации - строки: {len(dow_sales_clean)}, пример значений:")
    # print(dow_sales_clean.head())
    # print(f"Типы данных: {dow_sales_clean.dtypes}")
    # print(f"Колонки: {dow_sales_clean.columns.tolist()}")
    
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
        
    try:
        # Преобразуем значения в числовой тип для уверенности
        dow_sales_clean_for_plot = dow_sales_clean.copy()
        dow_sales_clean_for_plot['Сумма'] = pd.to_numeric(dow_sales_clean_for_plot['Сумма'], errors='coerce')
        fig = px.bar(
            dow_sales_clean_for_plot,
            x='ДеньНеделиЛок',
            y='Сумма',
            title=selected_lang['title'],
            labels={'ДеньНеделиЛок': selected_lang['x_axis'], 'Сумма': selected_lang['y_axis']}
        )
    except Exception as e:
        print(f"ERROR: Ошибка при создании графика по дням недели: {e}")
        # Возвращаем график с использованием px.bar с правильными данными в случае ошибки
        # Преобразуем значения в числовой тип для уверенности в обработке ошибок
        dow_sales_clean_error = dow_sales_clean.copy()
        dow_sales_clean_error['Сумма'] = pd.to_numeric(dow_sales_clean_error['Сумма'], errors='coerce')
        fig = px.bar(
            dow_sales_clean_error,
            x='ДеньНеделиЛок',
            y='Сумма',
            title=f"{selected_lang['title']} - ОШИБКА ОТЛАДКИ"
        )
        return fig
    
    # Настройка внешнего вида графика
    fig.update_xaxes(title_text=selected_lang['x_axis'])
    fig.update_yaxes(title_text=selected_lang['y_axis'])
    
    return fig