# Используем официальный образ Python 3.11 как базовый
FROM python:3.11-slim

# Устанавливаем рабочую директорию в контейнере
WORKDIR /app

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копируем файл зависимостей
COPY requirements.txt .

# Устанавливаем зависимости
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Копируем остальные файлы приложения
COPY web_app/ ./web_app/
COPY app/ ./app/

# Открываем порт 8501, который использует Streamlit
EXPOSE 8501

# Команда для запуска приложения
CMD ["streamlit", "run", "web_app/app.py", "--server.port", "8501", "--server.address", "0.0.0.0"]