import streamlit as st
import pandas as pd
from data_loader import load_data, load_uploaded_data
from plotting import create_sales_over_time_plot, create_city_sales_plot, create_day_of_week_plot
from analysis import calculate_kpi_metrics

# Функции перевода текста
def get_text(lang, key):
    translations = {
        'русский': {
            'title': 'Анализатор продаж интернет-магазинов',
            'sidebar_header': 'Параметры анализа',
            'upload_label': 'Загрузите свой файл данных (CSV или Excel)',
            'upload_success': 'Данные успешно загружены из файла',
            'date_start': 'Начальная дата',
            'date_end': 'Конечная дата',
            'select_language': 'Выберите язык',
            'total_sales': 'Общая сумма продаж',
            'avg_daily_sales': 'Средние ежедневные продажи',
            'max_daily_sales': 'Максимальные ежедневные продажи',
            'sales_over_time': 'Продажи по дням',
            'city_sales': 'Продажи по городам',
            'day_of_week_sales': 'Продажи по дням недели',
            'selected_period_data': 'Данные за выбранный период',
            'data_table_title': 'Таблица данных за выбранный период',
            'period_data_header': 'Данные по всему периоду',
            'selected_period_sales': 'Данные по выбранному периоду',
            'all_period_sales': 'Данные по всему периоду',
            'note_faq': 'Часто задаваемые вопросы находятся на отдельной странице \'FAQ\', доступной через боковое меню.',
            'error_file_not_found': 'Не удалось загрузить данные. Пожалуйста, проверьте наличие файла dataset_1.xlsx в папке app или загрузите свой файл.',
            'error_missing_columns': 'Файл данных должен содержать следующие колонки: {}',
            'error_invalid_file': 'Поддерживаются только файлы CSV и Excel (.xlsx, .xls)',
            'select_city': 'Выберите город',
            'all_cities': 'Все города',
            'cities': {
                'Москва': 'Moscow',
                'Санкт-Петербург': 'St. Petersburg',
                'Казань': 'Kazan',
                'Новосибирск': 'Novosibirsk',
                'Екатеринбург': 'Yekaterinburg',
                'Нижний Новгород': 'Nizhny Novgorod',
                'Краснодар': 'Krasnodar',
                'Самара': 'Samara',
                'Челябинск': 'Chelyabinsk',
                'Ростов-на-Дону': 'Rostov-on-Don',
                'Уфа': 'Ufa',
                'Волгоград': 'Volgograd',
                'Пермь': 'Perm',
                'Воронеж': 'Voronezh',
                'Саратов': 'Saratov',
                'Тюмень': 'Tyumen',
                'Тольятти': 'Tolyatti',
                'Ижевск': 'Izhevsk',
                'Барнаул': 'Barnaul',
                'Иркутск': 'Irkutsk'
            },
            'faq_q1': 'Какие данные можно анализировать?',
            'faq_a1': 'Приложение позволяет анализировать данные о продажах интернет-магазина, включая дату, город, имя клиента, фамилию и сумму покупки.',
            'faq_q2': 'Как интерпретировать графики?',
            'faq_a2': 'График продаж по времени показывает динамику продаж в течение выбранного периода. График по городам показывает сравнение продаж по различным городам.',
            'faq_q3': 'Как интерпретировать графики?',
            'faq_a3': 'График продаж по времени показывает динамику продаж в течение выбранного периода. График по городам показывает сравнение продаж по различным городам.',
            'faq_q4': 'Какие метрики отображаются?',
            'faq_a4': 'Приложение отображает общую сумму продаж, средние ежедневные продажи и максимальные ежедневные продажи за выбранный период.',
            'faq_q5': 'Как выбрать язык интерфейса?',
            'faq_a5': 'Вы можете выбрать язык интерфейса из выпадающего списка в боковой панели. В настоящее время поддерживаются русский, английский и китайский языки.',
            'faq_q6': 'Как фильтровать данные по дате?',
            'faq_a6': 'Используйте виджеты выбора даты в боковой панели, чтобы установить начальную и конечную дату для анализа.',
            'faq_q7': 'Какие форматы файлов поддерживаются для загрузки?',
            'faq_a7': 'Приложение поддерживает загрузку файлов в формате CSV и Excel (.xlsx, .xls). Файл должен содержать колонки: \'Дата\', \'Город\', \'Имя\', \'Фамилия\', \'Сумма\', \'Валюта\'.',
            'nav_analysis': 'Анализ данных',
            'nav_faq': 'FAQ',
            'date_col': 'Дата',
            'city_col': 'Город',
            'name_col': 'Имя',
            'surname_col': 'Фамилия',
            'amount_col': 'Сумма',
            'currency_col': 'Валюта'
        },
        'английский': {
            'title': 'E-commerce Sales Analyzer',
            'sidebar_header': 'Analysis Parameters',
            'upload_label': 'Upload your data file (CSV or Excel)',
            'upload_success': 'Data successfully loaded from file',
            'date_start': 'Start Date',
            'date_end': 'End Date',
            'select_language': 'Select Language',
            'total_sales': 'Total Sales Amount',
            'avg_daily_sales': 'Average Daily Sales',
            'max_daily_sales': 'Maximum Daily Sales',
            'sales_over_time': 'Sales Over Time',
            'city_sales': 'Sales by City',
            'day_of_week_sales': 'Sales by Day of Week',
            'selected_period_data': 'Data for Selected Period',
            'data_table_title': 'Selected Period Data Table',
            'period_data_header': 'Data for Entire Period',
            'selected_period_sales': 'Data for Selected Period',
            'all_period_sales': 'Data for Entire Period',
            'note_faq': 'Frequently asked questions are on a separate \'FAQ\' page accessible through the sidebar menu.',
            'error_file_not_found': 'Failed to load data. Please check if dataset_1.xlsx file exists in the app folder or upload your own file.',
            'error_missing_columns': 'Data file must contain the following columns: {}',
            'error_invalid_file': 'Only CSV and Excel (.xlsx, .xls) files are supported',
            'select_city': 'Select City',
            'all_cities': 'All Cities',
            'cities': {
                'Москва': 'Moscow',
                'Санкт-Петербург': 'St. Petersburg',
                'Казань': 'Kazan',
                'Новосибирск': 'Novosibirsk',
                'Екатеринбург': 'Yekaterinburg',
                'Нижний Новгород': 'Nizhny Novgorod',
                'Краснодар': 'Krasnodar',
                'Самара': 'Samara',
                'Челябинск': 'Chelyabinsk',
                'Ростов-на-Дону': 'Rostov-on-Don',
                'Уфа': 'Ufa',
                'Волгоград': 'Volgograd',
                'Пермь': 'Perm',
                'Воронеж': 'Voronezh',
                'Саратов': 'Saratov',
                'Тюмень': 'Tyumen',
                'Тольятти': 'Tolyatti',
                'Ижевск': 'Izhevsk',
                'Барнаул': 'Barnaul',
                'Иркутск': 'Irkutsk'
            },
            'faq_q1': 'What data can be analyzed?',
            'faq_a1': 'The application allows analyzing e-commerce sales data, including date, city, customer name, surname, and purchase amount.',
            'faq_q2': 'How to interpret the graphs?',
            'faq_a2': 'The sales over time chart shows sales dynamics over the selected period. The city chart shows sales comparison across different cities.',
            'faq_q3': 'How to interpret the graphs?',
            'faq_a3': 'The sales over time chart shows sales dynamics over the selected period. The city chart shows sales comparison across different cities.',
            'faq_q4': 'What metrics are displayed?',
            'faq_a4': 'The application displays total sales amount, average daily sales, and maximum daily sales for the selected period.',
            'faq_q5': 'How to select the interface language?',
            'faq_a5': 'You can select the interface language from the dropdown list in the sidebar. Currently, Russian, English, and Chinese are supported.',
            'faq_q6': 'How to filter data by date?',
            'faq_a6': 'Use the date selection widgets in the sidebar to set the start and end date for analysis.',
            'faq_q7': 'What file formats are supported for upload?',
            'faq_a7': 'The application supports uploading CSV and Excel (.xlsx, .xls) files. The file must contain columns: \'Date\', \'City\', \'Name\', \'Surname\', \'Amount\', \'Currency\'.',
            'nav_analysis': 'Data Analysis',
            'nav_faq': 'FAQ',
            'date_col': 'Date',
            'city_col': 'City',
            'name_col': 'Name',
            'surname_col': 'Surname',
            'amount_col': 'Amount',
            'currency_col': 'Currency'
        },
        'китайский': {
            'title': '电商销售分析器',
            'sidebar_header': '分析参数',
            'upload_label': '上传您的数据文件（CSV或Excel）',
            'upload_success': '数据已成功从文件加载',
            'date_start': '开始日期',
            'date_end': '结束日期',
            'select_language': '选择语言',
            'total_sales': '总销售额',
            'avg_daily_sales': '平均每日销售额',
            'max_daily_sales': '最大单日销售额',
            'sales_over_time': '销售趋势',
            'city_sales': '按城市划分的销售额',
            'day_of_week_sales': '按星期划分的销售额',
            'selected_period_data': '选定期间的数据',
            'data_table_title': '选定期间数据表',
            'period_data_header': '整个期间的数据',
            'selected_period_sales': '选定期间的数据',
            'all_period_sales': '整个期间的数据',
            'note_faq': '常见问题在单独的"FAQ"页面上，可通过侧边栏菜单访问。',
            'error_file_not_found': '无法加载数据。请检查app文件夹中是否存在dataset_1.xlsx文件或上传自己的文件。',
            'error_missing_columns': '数据文件必须包含以下列：{}',
            'error_invalid_file': '仅支持CSV和Excel（.xlsx，.xls）文件',
            'select_city': '选择城市',
            'all_cities': '所有城市',
            'cities': {
                'Москва': '北京',
                'Санкт-Петербург': '上海',
                'Казань': '广州',
                'Новосибирск': '深圳',
                'Екатеринбург': '天津',
                'Нижний Новгород': '成都',
                'Краснодар': '武汉',
                'Самара': '重庆',
                'Челябинск': '杭州',
                'Ростов-на-Дону': '南京',
                'Уфа': '西安',
                'Волгоград': '苏州',
                'Пермь': '郑州',
                'Воронеж': '青岛',
                'Саратов': '长沙',
                'Тюмень': '宁波',
                'Тольятти': '东莞',
                'Ижевск': '无锡',
                'Барнаул': '大连',
                'Иркутск': '厦门'
            },
            'faq_q1': '可以分析哪些数据？',
            'faq_a1': '该应用程序允许分析电子商务销售数据，包括日期、城市、客户姓名、姓氏和购买金额。',
            'faq_q2': '如何解释图表？',
            'faq_a2': '销售时间图显示所选期间的销售动态。城市图显示不同城市的销售比较。',
            'faq_q3': '如何解释图表？',
            'faq_a3': '销售时间图显示所选期间的销售动态。城市图显示不同城市的销售比较。',
            'faq_q4': '显示哪些指标？',
            'faq_a4': '该应用程序显示所选期间的总销售额、平均每日销售额和最大单日销售额。',
            'faq_q5': '如何选择界面语言？',
            'faq_a5': '您可以从侧边栏中的下拉列表中选择界面语言。目前支持俄语、英语和中文。',
            'faq_q6': '如何按日期筛选数据？',
            'faq_a6': '使用侧边栏中的日期选择小部件设置分析的开始和结束日期。',
            'faq_q7': '支持哪些文件格式上传？',
            'faq_a7': '该应用程序支持上传CSV和Excel（.xlsx，.xls）文件。文件必须包含以下列：\'日期\'、\'城市\'、\'名字\'、\'姓氏\'、\'金额\'、\'货币\'。',
            'nav_analysis': '数据分析',
            'nav_faq': '常见问题',
            'date_col': '日期',
            'city_col': '城市',
            'name_col': '名字',
            'surname_col': '姓氏',
            'amount_col': '金额',
            'currency_col': '货币'
        }
    }
    return translations.get(lang, translations['русский']).get(key, key)

# Выбор языка
language = st.sidebar.selectbox(get_text('русский', 'select_language'), ["русский", "английский", "китайский"])

# Боковая панель с элементами управления
st.sidebar.header(get_text(language, 'sidebar_header'))

# Обновляем заголовок в соответствии с выбранным языком
try:
    st.set_page_config(page_title=get_text(language, 'title'), layout="wide")
except:
    try:
        st.set_page_config(page_title=get_text(language, 'title'))
    except:
        try:
            st.set_page_config(page_title="E-commerce Sales Analyzer")
        except:
            # Если все попытки установить конфигурацию страницы неудачны, просто продолжаем
            pass

st.title(get_text(language, 'title'))

# Возможность загрузки пользовательских данных
uploaded_file = st.sidebar.file_uploader(get_text(language, 'upload_label'), type=['csv', 'xlsx', 'xls'])

# Загрузка данных
if uploaded_file is not None:
    df = load_uploaded_data(uploaded_file)
    if df is not None:
        st.sidebar.success(get_text(language, 'upload_success'))
else:
    df = load_data("app/dataset_1.xlsx")
    
# Проверка структуры данных
if df is not None and not df.empty:
    # Проверяем наличие минимально необходимых колонок для расчета KPI
    required_kpi_columns = ['Дата', 'Сумма']
    missing_kpi_cols = [col for col in required_kpi_columns if col not in df.columns]
    if missing_kpi_cols:
        st.error(get_text(language, 'error_missing_columns').format(missing_kpi_cols))
        st.stop()

if df is not None:
    # Выбор диапазона дат
    min_date = df['Дата'].min().date()
    max_date = df['Дата'].max().date()
    start_date = st.sidebar.date_input(get_text(language, 'date_start'), value=min_date, min_value=min_date, max_value=max_date, key='start_date')
    end_date = st.sidebar.date_input(get_text(language, 'date_end'), value=max_date, min_value=min_date, max_value=max_date, key='end_date')

    # Фильтрация данных по дате
    mask = (df['Дата'].dt.date >= start_date) & (df['Дата'].dt.date <= end_date)
    filtered_df = df.loc[mask]
    
    # Проверка наличия всех необходимых колонок для полноценной работы приложения
    # Проверка уже выполнена в data_loader с переименованием альтернативных названий
    # Здесь просто убедимся, что основные колонки для KPI присутствуют
    required_kpi_columns = ['Дата', 'Сумма']
    missing_cols = [col for col in required_kpi_columns if col not in df.columns]
    if missing_cols:
        # Вместо остановки приложения, показываем предупреждение
        st.warning(f"Предупреждение: Отсутствуют колонки: {missing_cols}. Приложение не может работать без этих колонок.")

    # Получение уникальных городов для выбора
    unique_cities = sorted(filtered_df['Город'].unique())
    
    # Используем session_state для сохранения выбора города
    if 'selected_city' not in st.session_state:
        st.session_state.selected_city = "Все"

    # Создаем отображаемый список городов с переводом
    display_cities = [get_text(language, 'all_cities')]
    for city in unique_cities:
        if language == 'русский':
            display_cities.append(city)
        elif language == 'английский':
            # Используем перевод города на английский
            translated_city = get_text('английский', 'cities').get(city, city)
            display_cities.append(translated_city)
        elif language == 'китайский':
            # Используем перевод города на китайский
            translated_city = get_text('китайский', 'cities').get(city, city)
            display_cities.append(translated_city)
    
    # Находим индекс ранее выбранного города в текущем списке
    if st.session_state.selected_city == "Все":
        default_index = 0
    else:
        # Найдем отображаемое название для сохраненного города
        display_selected_city = st.session_state.selected_city
        if language == 'английский':
            display_selected_city = get_text('английский', 'cities').get(st.session_state.selected_city, st.session_state.selected_city)
        elif language == 'китайский':
            display_selected_city = get_text('китайский', 'cities').get(st.session_state.selected_city, st.session_state.selected_city)
        
        try:
            default_index = display_cities.index(display_selected_city)
        except ValueError:
            default_index = 0
    
    # Создаем виджет выбора города
    selected_display_city = st.sidebar.selectbox(
        get_text(language, 'select_city'),
        display_cities,
        key='selected_city_widget',
        index=default_index
    )
    
    # Сохраняем выбранный город (в оригинальном названии)
    if selected_display_city == get_text(language, 'all_cities'):
        selected_city = "Все"
        st.session_state.selected_city = "Все"
    else:
        # Найдем оригинальное русское название города
        if language == 'русский':
            selected_city = selected_display_city
            st.session_state.selected_city = selected_display_city
        elif language == 'английский':
            # Найдем русское название по английскому переводу
            reverse_city_map = {v: k for k, v in get_text('английский', 'cities').items()}
            original_city = reverse_city_map.get(selected_display_city, selected_display_city)
            selected_city = original_city
            st.session_state.selected_city = original_city
        elif language == 'китайский':
            # Найдем русское название по китайскому переводу
            reverse_city_map = {v: k for k, v in get_text('китайский', 'cities').items()}
            original_city = reverse_city_map.get(selected_display_city, selected_display_city)
            selected_city = original_city
            st.session_state.selected_city = original_city

    # Фильтрация данных по городу
    if selected_city != "Все":
        city_mask = filtered_df['Город'] == selected_city
        filtered_df = filtered_df.loc[city_mask]

    # Фильтрация данных по городу для всего периода (независимо от даты)
    all_period_filtered = df.copy()
    if selected_city != "Все":
        all_period_filtered = all_period_filtered[all_period_filtered['Город'] == selected_city]

    # Вычисление KPI метрик для выбранного периода
    kpi_results = calculate_kpi_metrics(filtered_df)
    if kpi_results is not None and len(kpi_results) == 3:
        total_sales, avg_daily_sales, max_daily_sales = kpi_results
    else:
        # Если данных нет, устанавливаем значения по умолчанию
        total_sales, avg_daily_sales, max_daily_sales = 0, 0, 0

    # Вычисление KPI метрик для всего выгруженного периода (с учетом выбранного города)
    kpi_all_results = calculate_kpi_metrics(all_period_filtered)
    if kpi_all_results is not None and len(kpi_all_results) == 3:
        total_all_period, avg_all_period, max_all_period = kpi_all_results
    else:
        # Если данных нет, устанавливаем значения по умолчанию
        total_all_period, avg_all_period, max_all_period = 0, 0, 0

    # Добавляем заголовок для первой группы метрик
    st.markdown(f'<h3 style="margin-top: 1rem; margin-bottom: 0.5rem;">{get_text(language, "selected_period_sales")}</h3>', unsafe_allow_html=True)
    
    # Отображение KPI метрик для выбранного периода с использованием CSS Grid для выравнивания
    # Получаем валюту из данных (предполагаем, что все записи в выбранном периоде имеют одинаковую валюту)
    # Проверяем, существует ли колонка 'Валюта' перед обращением к ней
    if 'Валюта' in filtered_df.columns and not filtered_df.empty:
        currency = filtered_df['Валюта'].iloc[0]
    else:
        currency = 'RUB'  # Устанавливаем значение по умолчанию
    
    # Создаем контейнер с CSS Grid для выравнивания метрик
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; margin-bottom: 1px;">
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'total_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{total_sales:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency}</div>
        </div>
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'avg_daily_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{avg_daily_sales:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency}</div>
        </div>
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'max_daily_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{max_daily_sales:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency}</div>
        </div>
    """, unsafe_allow_html=True)

    # Фильтрация данных по городу для всего периода (независимо от даты)
    all_period_filtered = df.copy()
    if selected_city != "Все":
        all_period_filtered = all_period_filtered[all_period_filtered['Город'] == selected_city]

    # Вычисление KPI метрик для всего выгруженного периода (с учетом выбранного города)
    total_all_period, avg_all_period, max_all_period = calculate_kpi_metrics(all_period_filtered)

    # Закрываем предыдущий div
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Отображение KPI метрик для всего периода (с учетом выбранного города)
    # Используем тот же стиль, что и для заголовка "Данные по выбранному периоду"
    st.markdown(f'<h3 style="margin-top: 2rem; margin-bottom: 1rem;">{get_text(language, "all_period_sales")}</h3>', unsafe_allow_html=True)
    
    # Проверяем, существует ли колонка 'Валюта' перед обращением к ней
    if 'Валюта' in all_period_filtered.columns and not all_period_filtered.empty:
        currency_all = all_period_filtered['Валюта'].iloc[0]
    else:
        currency_all = 'RUB'  # Устанавливаем значение по умолчанию
    
    # Создаем контейнер с CSS Grid для выравнивания метрик
    st.markdown(f"""
    <div style="display: grid; grid-template-columns: 1fr 1fr 1fr; gap: 5px; margin-bottom: 1px;">
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'total_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{total_all_period:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency_all}</div>
        </div>
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'avg_daily_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{avg_all_period:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency_all}</div>
        </div>
        <div style="text-align: center; padding: 3px;">
            <div style="font-weight: bold; font-size: 12px; margin-bottom: 1px; height: 1.8em; display: flex; align-items: center; justify-content: center; color: white;">{get_text(language, 'max_daily_sales')}</div>
            <div style="font-size: 20px; font-weight: bold; margin: 8px 0 3px 0; color: white;">{f'{max_all_period:,.2f}'.replace(',', ' ')}</div>
            <div style="color: green; font-size: 12px; margin-top: 1px;">{currency_all}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Визуализация данных
    if filtered_df.empty:
        st.warning("Нет данных для отображения за выбранный период.")
    else:
        st.plotly_chart(create_sales_over_time_plot(filtered_df, language), width='stretch')
        st.plotly_chart(create_day_of_week_plot(filtered_df, language), width='stretch')

    # Отображение таблицы с данными
    st.subheader(get_text(language, 'data_table_title'))
    
    # Создаем копию данных для отображения с переводом заголовков колонок
    display_df = filtered_df.copy()
    
    # Определяем, какие колонки нужно переименовать, проверяя их существование
    column_mapping = {}
    if 'Дата' in display_df.columns:
        column_mapping['Дата'] = get_text(language, 'date_col')
    if 'Город' in display_df.columns:
        column_mapping['Город'] = get_text(language, 'city_col')
    if 'Имя' in display_df.columns:
        column_mapping['Имя'] = get_text(language, 'name_col')
    if 'Фамилия' in display_df.columns:
        column_mapping['Фамилия'] = get_text(language, 'surname_col')
    if 'Сумма' in display_df.columns:
        column_mapping['Сумма'] = get_text(language, 'amount_col')
    if 'Валюта' in display_df.columns:
        column_mapping['Валюта'] = get_text(language, 'currency_col')
    
    # Переименовываем колонки
    display_df.rename(columns=column_mapping, inplace=True)
    
    st.dataframe(display_df)

    # Отображение сообщения о том, что FAQ находится на отдельной странице
    st.markdown(f"**Note:** {get_text(language, 'note_faq')}")
else:
    st.error(get_text(language, 'error_file_not_found'))