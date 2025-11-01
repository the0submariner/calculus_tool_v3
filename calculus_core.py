"""
calculus_core.py

Модуль для символьных математических вычислений:
- вычисление производных,
- базовых арифметических операций,
- вычисление первообразных (неопределенных и определенных интегралов),
- упрощение выражений,
- разложение в ряд Тейлора (series).

Использует библиотеку SymPy. Обрабатывает типовые ошибки и возвращает текстовые сообщения.
"""

import sympy
from sympy import Symbol, sympify, diff, integrate, simplify, series
from sympy.core.sympify import SympifyError

class MathCalculator:
    """
    Класс для символьных математических вычислений.
    Методы:
    - derivative(expression, variable)
    - calculate(expression, substitutions=None)
    - integrate(expression, variable, lower=None, upper=None)
    - simplify_expression(expression)
    - series_expansion(expression, variable, n=5, x0=0)
    """

    @staticmethod
    def _safe_sympify(value):
        """Вспомогательный метод для безопасного преобразования строки в символьный объект."""
        try:
            return sympify(value), None
        except SympifyError:
            return None, "Ошибка: некорректный синтаксис выражения"
        except Exception as e:
            return None, f"Ошибка: {str(e)}"

    @staticmethod
    def derivative(expression: str, variable: str) -> str:
        """Вычисляет производную выражения по переменной."""
        var, error = MathCalculator._safe_sympify(variable)
        if error:
            return error
        expr, error = MathCalculator._safe_sympify(expression)
        if error:
            return error
        try:
            derivative_expr = diff(expr, var)
            return str(derivative_expr)
        except Exception as e:
            return f"Ошибка: невозможно вычислить производную ({str(e)})"

    @staticmethod
    def calculate(expression: str, substitutions: dict = None):
        """
        Вычисляет числовое значение выражения с возможной подстановкой переменных.
        Возвращает кортеж (строка выражения, численный результат) или (ошибка, None).
        """
        expr, error = MathCalculator._safe_sympify(expression)
        if error:
            return error, None
        if substitutions:
            try:
                expr = expr.subs(substitutions)
            except Exception as e:
                return f"Ошибка в подстановке переменных: {str(e)}", None
        try:
            result = expr.evalf()
            return str(expr), result
        except Exception as e:
            return f"Ошибка при вычислении: {str(e)}", None

    @staticmethod
    def integrate(expression: str, variable: str, lower: str = None, upper: str = None) -> str:
        """
        Вычисляет первообразную выражения (неопределенный или определенный интеграл).
        Возвращает строку результата или сообщение об ошибке.
        """
        var, error = MathCalculator._safe_sympify(variable)
        if error:
            return error
        expr, error = MathCalculator._safe_sympify(expression)
        if error:
            return error

        if (lower is not None and upper is None) or (lower is None and upper is not None):
            return "Ошибка: должны быть заданы оба предела интегрирования или ни один."

        if lower is not None and upper is not None:
            a, err_a = MathCalculator._safe_sympify(lower)
            b, err_b = MathCalculator._safe_sympify(upper)
            if err_a or err_b:
                return "Ошибка: некорректные пределы интегрирования"
            try:
                integral = integrate(expr, (var, a, b))
                return str(integral)
            except Exception as e:
                return f"Ошибка при вычислении определенного интеграла: {str(e)}"
        else:
            try:
                integral = integrate(expr, var)
                return str(integral)
            except Exception as e:
                return f"Ошибка при вычислении неопределенного интеграла: {str(e)}"

    @staticmethod
    def simplify_expression(expression: str) -> str:
        """Упрощает математическое выражение."""
        expr, error = MathCalculator._safe_sympify(expression)
        if error:
            return error
        try:
            simplified = simplify(expr)
            return str(simplified)
        except Exception as e:
            return f"Ошибка при упрощении: {str(e)}"

    @staticmethod
    def series_expansion(expression: str, variable: str, n: int = 5, x0=0) -> str:
        """
        Выполняет разложение выражения в ряд Тейлора около точки x0 (по умолчанию 0) до порядка n.
        """
        var, error = MathCalculator._safe_sympify(variable)
        if error:
            return error
        expr, error = MathCalculator._safe_sympify(expression)
        if error:
            return error
        try:
            ser = series(expr, var, x0, n).removeO()
            return str(ser)
        except Exception as e:
            return f"Ошибка при разложении в ряд: {str(e)}"


if __name__ == "__main__":
    print("=== Проверка производной ===")
    test_cases = [("x**2 + 2*x + 1", "x"), ("sin(x)", "x"), ("invalid expr", "x"), ("x**2", "y")]
    for expression, variable in test_cases:
        print(f"Производная {expression} по {variable}: {MathCalculator.derivative(expression, variable)}")

    print("\n=== Проверка calculate ===")
    calc_tests = [("2 + 3*4", None), ("sqrt(16)", None), ("x + 1", {"x": 3}), ("invalid + expr", None)]
    for expression, subs in calc_tests:
        res_str, res_val = MathCalculator.calculate(expression, subs)
        print(f"Вычисление '{expression}' с подстановками {subs}: выражение = '{res_str}', значение = {res_val}")

    print("\n=== Проверка интеграла ===")
    print(MathCalculator.integrate("x**2", "x"))                  # неопределенный
    print(MathCalculator.integrate("x**2", "x", "0", "1"))        # определенный
    print(MathCalculator.integrate("x**2", "x", "0"))             # ошибка
    print(MathCalculator.integrate("invalid", "x"))               # ошибка

    print("\n=== Проверка упрощения ===")
    print(MathCalculator.simplify_expression("sin(x)**2 + cos(x)**2"))

    print("\n=== Проверка ряда Тейлора ===")
    print(MathCalculator.series_expansion("exp(x)", "x", 6))
    print(MathCalculator.series_expansion("log(1+x)", "x", 6, 1))
