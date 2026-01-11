@echo off
REM Скрипт для создания и активации виртуального окружения на Windows

echo Создание виртуального окружения...
python -m venv venv

if %ERRORLEVEL% NEQ 0 (
    echo Ошибка при создании виртуального окружения
    exit /b %ERRORLEVEL%
)

echo Установка зависимостей...
call venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo Ошибка при установке зависимостей
    exit /b %ERRORLEVEL%
)

echo.
echo Виртуальное окружение создано и зависимости установлены.
echo Для активации окружения выполните: venv\Scripts\activate
echo.
pause