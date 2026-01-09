import streamlit as st

# Выбор языка
language = st.sidebar.selectbox("Язык / Language", ["Русский", "English"])

if language == "Русский":
    st.title("Калькулятор")
    
    # Ввод чисел
    num1 = st.number_input("Введите первое число", value=0.0)
    operation = st.selectbox("Выберите операцию", ["+", "-", "*", "/"])
    num2 = st.number_input("Введите второе число", value=0.0)
    button_text = "Вычислить"
    error_text = "Ошибка: деление на ноль!"
    result_text = f"Результат: {num1} {operation} {num2} = "
else:
    st.title("Calculator")
    
    # Ввод чисел
    num1 = st.number_input("Enter first number", value=0.0)
    operation = st.selectbox("Select operation", ["+", "-", "*", "/"])
    num2 = st.number_input("Enter second number", value=0.0)
    button_text = "Calculate"
    error_text = "Error: division by zero!"
    result_text = f"Result: {num1} {operation} {num2} = "

# Вычисление результата
if st.button(button_text):
    if operation == "+":
        result = num1 + num2
    elif operation == "-":
        result = num1 - num2
    elif operation == "*":
        result = num1 * num2
    elif operation == "/":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error(error_text)
            result = None
    
    if result is not None:
        st.success(f"{result_text}{result}")