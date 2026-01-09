import streamlit as st
import pandas as pd
from datetime import datetime
import os

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
        df['Дата'] = pd.to_datetime(df['Дата'])
        
        # Проверка наличие необходимых колонок
        required_columns = ['Дата', 'Город', 'Имя', 'Фамилия', 'Сумма', 'Валюта']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Файл данных должен содержать следующие колонки: {required_columns}")
            return None
            
        return df
    except FileNotFoundError:
        st.error(f"Файл {file_path} не найден. Пожалуйста, проверьте наличие файла.")
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
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        elif uploaded_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(uploaded_file)
        else:
            st.error("Поддерживаются только файлы CSV и Excel (.xlsx, .xls)")
            return None
        
        # Преобразование колонки 'Дата' в формат datetime
        df['Дата'] = pd.to_datetime(df['Дата'])
        
        # Проверка на наличие необходимых колонок
        required_columns = ['Дата', 'Город', 'Имя', 'Фамилия', 'Сумма', 'Валюта']
        if not all(col in df.columns for col in required_columns):
            st.error(f"Файл данных должен содержать следующие колонки: {required_columns}")
            return None
            
        return df
    except Exception as e:
        st.error(f"Ошибка при загрузке загруженного файла: {str(e)}")
        return None