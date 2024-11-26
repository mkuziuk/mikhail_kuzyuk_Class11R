def calculate(expression: str) -> float:
    """Calculates the result of a simple arithmetic expression."""
    try:
        tokens = expression.split(" ")

        if len(tokens) != 3:
            raise ValueError("Неверное количество операндов")

        num1 = float(tokens[0])
        operator = tokens[1]
        num2 = float(tokens[2])

        if operator == "+":
            return num1 + num2
        elif operator == "-":
            return num1 - num2
        elif operator == "*":
            return num1 * num2
        elif operator == "/":
            if num2 == 0:
                raise ZeroDivisionError("Деление на 0 недопустимо")
            return num1 / num2
        else:
            raise ValueError("Не валидный оператор. Доступные операторы: +, -, *, /")

    except ValueError as ve:
        print(f"Error: {ve}")
    except ZeroDivisionError as zde:
        print(f"Error: {zde}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
