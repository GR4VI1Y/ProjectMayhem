#!/bin/bash
# Скрипт для создания и активации виртуального окружения на Unix-системах

echo "Создание виртуального окружения..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Ошибка при создании виртуального окружения"
    exit 1
fi

echo "Установка зависимостей..."
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt

if [ $? -ne 0 ]; then
    echo "Ошибка при установке зависимостей"
    exit 1
fi

echo ""
echo "Виртуальное окружение создано и зависимости установлены."
echo "Для активации окружения выполните: source venv/bin/activate"
echo ""