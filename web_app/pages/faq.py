import streamlit as st
import pandas as pd

# Функции перевода текста
def get_text(lang, key):
    translations = {
        'русский': {
            'title': 'Часто задаваемые вопросы (FAQ)',
            'select_language': 'Выберите язык',
            'upload_section_title': 'Формат входящих данных',
            'upload_info': 'Приложение позволяет анализировать данные о продажах интернет-магазинов. Поддерживаемые форматы файлов: CSV и Excel (.xlsx, .xls).',
            'upload_columns': [
                "'Дата': дата продажи (в формате YYYY-MM-DD)",
                "'Город': город покупателя", 
                "'Имя': имя покупателя",
                "'Фамилия': фамилия покупателя",
                "'Сумма': сумма покупки (числовое значение)",
                "'Валюта': валюта, в которой совершена покупка (например, RUB, USD, EUR)"
            ],
            'can_upload_data': 'Можно ли загрузить свои данные?',
            'upload_data_info': 'Да, вы можете загрузить свой CSV или Excel файл со следующими обязательными столбцами:',
            'required_columns_header': 'Файл данных должен содержать следующие колонки:',
            'required_columns': [
                "'Дата': дата продажи (в формате YYYY-MM-DD)",
                "'Город': город покупателя",
                "'Имя': имя покупателя",
                "'Фамилия': фамилия покупателя",
                "'Сумма': сумма покупки (числовое значение)",
                "'Валюта': валюта, в которой совершена покупка (например, RUB, USD, EUR)"
            ],
            'supported_formats': 'Поддерживаемые форматы файлов: CSV и Excel (.xlsx, .xls)',
            'data_structure_example': 'Пример структуры данных:',
            'date_col': 'Дата',
            'city_col': 'Город',
            'name_col': 'Имя',
            'surname_col': 'Фамилия',
            'amount_col': 'Сумма',
            'currency_col': 'Валюта',
            'faq_q1': 'Какие данные можно анализировать?',
            'faq_a1': 'Приложение позволяет анализировать данные о продажах интернет-магазинов, включая дату, город, имя клиента, фамилию и сумму покупки.',
            'faq_q2': 'Как интерпретировать графики?',
            'faq_a2': 'График продаж по времени показывает динамику продаж в течение выбранного периода. График по городам показывает сравнение продаж по различным городам.',
            'faq_q3': 'Какие метрики отображаются?',
            'faq_a3': 'Приложение отображает общую сумму продаж, средние ежедневные продажи и максимальные ежедневные продажи за выбранный период.',
            'faq_q4': 'Как выбрать язык интерфейса?',
            'faq_a4': 'Вы можете выбрать язык интерфейса из выпадающего списка в боковой панели. В настоящее время поддерживаются русский, английский и китайский языки.',
            'faq_q5': 'Как фильтровать данные по дате?',
            'faq_a5': 'Используйте виджеты выбора даты в боковой панели, чтобы установить начальную и конечную дату для анализа.',
            'faq_q6': 'Какие форматы файлов поддерживаются для загрузки?',
            'faq_a6': 'Приложение поддерживает загрузку файлов в формате CSV и Excel (.xlsx, .xls). Файл должен содержать колонки: \'Дата\', \'Город\', \'Имя\', \'Фамилия\', \'Сумма\', \'Валюта\'.'
        },
        'английский': {
            'title': 'Frequently Asked Questions (FAQ)',
            'select_language': 'Select Language',
            'upload_section_title': 'Data Upload Format',
            'upload_info': 'The application allows analyzing e-commerce sales data. Supported file formats: CSV and Excel (.xlsx, .xls).',
            'upload_columns': [
                "'Date': sale date (in YYYY-MM-DD format)",
                "'City': customer city",
                "'Name': customer name",
                "'Surname': customer surname",
                "'Amount': purchase amount (numeric value)",
                "'Currency': currency in which the purchase was made (e.g., RUB, USD, EUR)"
            ],
            'can_upload_data': 'Can I upload my own data?',
            'upload_data_info': 'Yes, you can upload your own CSV or Excel file with the following required columns:',
            'required_columns_header': 'Data file must contain the following columns:',
            'required_columns': [
                "'Date': sale date (in YYYY-MM-DD format)",
                "'City': customer city",
                "'Name': customer name",
                "'Surname': customer surname",
                "'Amount': purchase amount (numeric value)",
                "'Currency': currency in which the purchase was made (e.g., RUB, USD, EUR)"
            ],
            'supported_formats': 'Supported file formats: CSV and Excel (.xlsx, .xls)',
            'data_structure_example': 'Example of data structure:',
            'date_col': 'Date',
            'city_col': 'City',
            'name_col': 'Name',
            'surname_col': 'Surname',
            'amount_col': 'Amount',
            'currency_col': 'Currency',
            'faq_q1': 'What data can be analyzed?',
            'faq_a1': 'The application allows analyzing e-commerce sales data, including date, city, customer name, surname, and purchase amount.',
            'faq_q2': 'How to interpret the graphs?',
            'faq_a2': 'The sales over time chart shows sales dynamics over the selected period. The city chart shows sales comparison across different cities.',
            'faq_q3': 'What metrics are displayed?',
            'faq_a3': 'The application displays total sales amount, average daily sales, and maximum daily sales for the selected period.',
            'faq_q4': 'How to select the interface language?',
            'faq_a4': 'You can select the interface language from the dropdown list in the sidebar. Currently, Russian, English, and Chinese are supported.',
            'faq_q5': 'How to filter data by date?',
            'faq_a5': 'Use the date selection widgets in the sidebar to set the start and end date for analysis.',
            'faq_q6': 'What file formats are supported for upload?',
            'faq_a6': 'The application supports uploading CSV and Excel (.xlsx, .xls) files. The file must contain columns: \'Date\', \'City\', \'Name\', \'Surname\', \'Amount\', \'Currency\'.'
        },
        'китайский': {
            'title': '常见问题解答 (FAQ)',
            'select_language': '选择语言',
            'upload_section_title': '数据上传格式',
            'upload_info': '该应用程序允许分析电子商务销售数据。支持的文件格式：CSV和Excel (.xlsx, .xls).',
            'upload_columns': [
                "'日期': 销售日期（YYYY-MM-DD格式）",
                "'城市': 客户城市",
                "'名字': 客户名字",
                "'姓氏': 客户姓氏",
                "'金额': 购买金额（数值）",
                "'货币': 购买时使用的货币（例如，RUB、USD、EUR）"
            ],
            'can_upload_data': '我可以上传自己的数据吗？',
            'upload_data_info': '是的，您可以上传包含以下必要列的CSV或Excel文件：',
            'required_columns_header': '数据文件必须包含以下列：',
            'required_columns': [
                "'日期': 销售日期（YYYY-MM-DD格式）",
                "'城市': 客户城市",
                "'名字': 客户名字",
                "'姓氏': 客户姓氏",
                "'金额': 购买金额（数值）",
                "'货币': 购买时使用的货币（例如，RUB、USD、EUR）"
            ],
            'supported_formats': '支持的文件格式：CSV和Excel (.xlsx, .xls)',
            'data_structure_example': '数据结构示例：',
            'date_col': '日期',
            'city_col': '城市',
            'name_col': '名字',
            'surname_col': '姓氏',
            'amount_col': '金额',
            'currency_col': '货币',
            'faq_q1': '可以分析哪些数据？',
            'faq_a1': '该应用程序允许分析电子商务销售数据，包括日期、城市、客户姓名、姓氏和购买金额。',
            'faq_q2': '如何解释图表？',
            'faq_a2': '销售时间图显示所选期间的销售动态。城市图显示不同城市的销售比较。',
            'faq_q3': '显示哪些指标？',
            'faq_a3': '该应用程序显示所选期间的总销售额、平均每日销售额和最大单日销售额。',
            'faq_q4': '如何选择界面语言？',
            'faq_a4': '您可以从侧边栏中的下拉列表中选择界面语言。目前支持俄语、英语和中文。',
            'faq_q5': '如何按日期筛选数据？',
            'faq_a5': '使用侧边栏中的日期选择小部件设置分析的开始和结束日期。',
            'faq_q6': '支持哪些文件格式上传？',
            'faq_a6': '该应用程序支持上传CSV和Excel（.xlsx，.xls）文件。文件必须包含以下列：\'日期\'、\'城市\'、\'名字\'、\'姓氏\'、\'金额\'、\'货币\'。'
        }
    }
    return translations.get(lang, translations['русский']).get(key, key)

# Выбор языка
language = st.sidebar.selectbox(get_text('русский', 'select_language'), ["русский", "английский", "китайский"])

# Установка заголовка страницы
st.title(get_text(language, 'title'))

# Раздел о загрузке собственных данных - теперь отображается как постоянная информация вверху страницы
st.header(get_text(language, 'upload_section_title'))
st.write(get_text(language, 'upload_info'))
columns = get_text(language, 'upload_columns')
if isinstance(columns, list):
    for col in columns:
        st.write(f"- {col}")
else:
    st.write(columns)

st.write(" ")
st.write(get_text(language, 'data_structure_example'))
example_data = pd.DataFrame({
    get_text(language, 'date_col'): ['2025-10-01', '2025-10-02'],
    get_text(language, 'city_col'): ['Москва', 'Санкт-Петербург'],
    get_text(language, 'name_col'): ['Иван', 'Мария'],
    get_text(language, 'surname_col'): ['Иванов', 'Петрова'],
    get_text(language, 'amount_col'): [5000.00, 7500.50],
    get_text(language, 'currency_col'): ['RUB', 'RUB']
})
st.dataframe(example_data)

# Выводим информацию о возможности загрузки данных как постоянный элемент вверху страницы
st.header(get_text(language, 'can_upload_data'))
st.write(get_text(language, 'upload_data_info'))

# Подробная информация о формате данных
st.write(get_text(language, 'required_columns_header'))
required_cols = get_text(language, 'required_columns')
if isinstance(required_cols, list):
    for col in required_cols:
        st.write(f"- {col}")
else:
    st.write(required_cols)

st.write(get_text(language, 'supported_formats'))

# Пример структуры данных
st.write(" ")
st.write(get_text(language, 'data_structure_example'))
example_data = pd.DataFrame({
    get_text(language, 'date_col'): ['2025-10-01', '2025-10-02'],
    get_text(language, 'city_col'): ['Москва', 'Санкт-Петербург'],
    get_text(language, 'name_col'): ['Иван', 'Мария'],
    get_text(language, 'surname_col'): ['Иванов', 'Петрова'],
    get_text(language, 'amount_col'): [5000.00, 7500.50],
    get_text(language, 'currency_col'): ['RUB', 'RUB']
})
st.dataframe(example_data)

# Добавляем пустую строку для разделения
st.write(" ")

# Остальные вопросы в выпадающем списке (вопрос №2 убираем, так как он теперь отображается постоянно)
with st.expander(get_text(language, 'faq_q1')):
    st.write(get_text(language, 'faq_a1'))

with st.expander(get_text(language, 'faq_q3')):
    st.write(get_text(language, 'faq_a3'))

with st.expander(get_text(language, 'faq_q4')):
    st.write(get_text(language, 'faq_a4'))

with st.expander(get_text(language, 'faq_q5')):
    st.write(get_text(language, 'faq_a5'))

with st.expander(get_text(language, 'faq_q6')):
    st.write(get_text(language, 'faq_a6'))