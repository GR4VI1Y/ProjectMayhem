import streamlit as st
import pandas as pd


def validate_and_normalize_columns(df):
    """
    Проверяет и нормализует названия колонок в DataFrame
    """
    # Нормализация названий колонок (удаление пробелов)
    df.columns = df.columns.str.strip()

    # Проверка на наличие минимально необходимых колонок для расчета KPI
    required_kpi_columns = ["Дата", "Сумма"]
    if not all(col in df.columns for col in required_kpi_columns):
        st.error(
            f"Файл данных должен содержать следующие колонки: "
            f"{required_kpi_columns}"
        )
        return df, False

    # Проверяем наличие всех необходимых колонок для полноценной работы
    # приложения, учитывая возможные варианты названий
    required_columns = ["Дата", "Город", "Имя", "Фамилия", "Сумма", "Валюта"]
    # Альтернативные названия колонок (например, английские названия)
    alt_column_names = {
        "Валюта": ["Currency"],
        "Дата": ["Date"],
        "Город": ["City"],
        "Имя": ["Name"],
        "Фамилия": ["Surname", "Last Name", "LastName"],
        "Сумма": ["Amount", "Sum", "Total"]
    }

    # Создаем словарь соответствий для поиска колонок (с учетом регистра)
    col_lower_map = {col.lower(): col for col in df.columns}

    # Проверяем наличие колонок, учитывая возможные альтернативные названия
    missing_cols = []
    for req_col in required_columns:
        found = False
        # Проверяем основное название
        if req_col in df.columns:
            found = True
        else:
            # Проверяем альтернативные названия
            if req_col in alt_column_names:
                for alt_name in alt_column_names[req_col]:
                    if alt_name in df.columns:
                        # Переименовываем альтернативное название в стандартное
                        df.rename(columns={alt_name: req_col}, inplace=True)
                        found = True
                        break

            # Если не найдено точное совпадение, проверим по нижнему регистру
            if not found:
                req_lower = req_col.lower()
                if req_lower in col_lower_map:
                    # Совпадение найдено, переименовываем колонку
                    actual_col_name = col_lower_map[req_lower]
                    if actual_col_name != req_col:
                        df.rename(columns={actual_col_name: req_col}, inplace=True)
                    found = True
                else:
                    # Проверяем альтернативные названия в нижнем регистре
                    if req_col in alt_column_names:
                        for alt_name in alt_column_names[req_col]:
                            alt_lower = alt_name.lower()
                            if alt_lower in col_lower_map:
                                actual_col_name = col_lower_map[alt_lower]
                                df.rename(columns={actual_col_name: req_col}, inplace=True)
                                found = True
                                break

        # Если всё ещё не найдено, проверим на частичное совпадение
        if not found:
            for col_name in df.columns:
                if req_col.lower() in col_name.lower() or (req_col == "Валюта" and "currency" in col_name.lower()) or (req_col == "Валюта" and "валют" in col_name.lower()):
                    # Совпадение найдено, переименовываем колонку
                    df.rename(columns={col_name: req_col}, inplace=True)
                    found = True
                    break

        if not found:
            missing_cols.append(req_col)

    if missing_cols:
        # Вместо остановки приложения, показываем предупреждение
        st.warning(
            f"Предупреждение: "
            f"Отсутствуют колонки: {missing_cols}. "
            "Некоторые функции могут "
            "работать некорректно."
        )

    return df, True


@st.cache_data
def load_data(file_path: str = "../app/dataset_1.xlsx") -> pd.DataFrame:
    """
    Загружает и кэширует данные из Excel файла.

    Args:
        file_path: Путь к файлу данных

    Returns:
        DataFrame с загруженными данными
    """
    try:
        # Загрузка данных из Excel файла
        df = pd.read_excel(file_path)

        # Преобразование колонки 'Дата' в формат datetime
        df["Дата"] = pd.to_datetime(df["Дата"])

        # Проверяем и нормализуем колонки
        df, is_valid = validate_and_normalize_columns(df)
        if not is_valid:
            return None

        return df
    except FileNotFoundError:
        error_msg = (
            "Файл {file_path} не найден. " "Пожалуйста, проверьте наличие файла."
        )
        st.error(error_msg)
        return None
    except Exception as e:
        st.error(f"Ошибка при загрузке данных: {str(e)}")
        return None


def load_uploaded_data(uploaded_file) -> pd.DataFrame:
    """
    Загружает данные из загруженного пользователем файла.

    Args:
        uploaded_file: Загруженный пользователем файл (CSV или Excel)

    Returns:
        DataFrame с загруженными данными
    """
    try:
        # Определение типа файла по расширению
        if uploaded_file.name.endswith(".csv"):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith((".xlsx", ".xls")):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Поддерживаются только файлы CSV и Excel (.xlsx, .xls)")
            return None

        # Преобразование колонки 'Дата' в формат datetime
        df["Дата"] = pd.to_datetime(df["Дата"])

        # Проверяем и нормализуем колонки
        df, is_valid = validate_and_normalize_columns(df)
        if not is_valid:
            return None

        return df

    except Exception as e:
        st.error(f"Ошибка при загрузке загруженного файла: {str(e)}")
        return None
