import tkinter as tk
from tkinter import ttk, messagebox
from calculus_core import MathCalculator

class CalculatorGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Символьный калькулятор на Python")

        # Описание операций и их параметров
        self.operations = {
            "Производная": {
                "func": MathCalculator.derivative,
                "params": ["Выражение", "Переменная"]
            },
            "Интеграл": {
                "func": MathCalculator.integrate,
                "params": ["Выражение", "Переменная", "Нижний предел (опционально)", "Верхний предел (опционально)"]
            },
            "Вычислить выражение": {
                "func": MathCalculator.calculate,
                "params": ["Выражение", "Подстановки (пример: x=2,y=3)"]
            },
            "Упростить": {
                "func": MathCalculator.simplify_expression,
                "params": ["Выражение"]
            },
            "Ряд Тейлора": {
                "func": MathCalculator.series_expansion,
                "params": ["Выражение", "Переменная", "Порядок (число)", "Точка разложения (число, опционально)"]
            }
        }

        self.create_widgets()

    def create_widgets(self):
        # Выпадающий список выбора операции
        tk.Label(self.root, text="Выберите операцию:").grid(row=0, column=0, sticky="w")
        self.op_var = tk.StringVar()
        self.op_combobox = ttk.Combobox(self.root, textvariable=self.op_var, values=list(self.operations.keys()), state="readonly")
        self.op_combobox.grid(row=0, column=1, sticky="ew")
        self.op_combobox.bind("<<ComboboxSelected>>", self.update_params)

        # Контейнер для параметров
        self.params_frame = tk.Frame(self.root)
        self.params_frame.grid(row=1, column=0, columnspan=2, sticky="ew")
        
        self.param_entries = []

        # Кнопка вычислить
        self.calc_button = tk.Button(self.root, text="Вычислить", command=self.calculate)
        self.calc_button.grid(row=2, column=0, columnspan=2, pady=5)

        # Текстовое поле результата
        tk.Label(self.root, text="Результат:").grid(row=3, column=0, sticky="nw")
        self.result_text = tk.Text(self.root, height=6, width=50, wrap="word")
        self.result_text.grid(row=3, column=1, sticky="ew")

        # Описание/справка
        tk.Label(self.root, text="Описание операции:").grid(row=4, column=0, sticky="nw")
        self.desc_text = tk.Text(self.root, height=8, width=50, wrap="word", bg="#f0f0f0")
        self.desc_text.grid(row=4, column=1, sticky="ew")

        self.root.columnconfigure(1, weight=1)
        self.op_combobox.current(0)
        self.update_params()

    def update_params(self, event=None):
        # Очистка параметров
        for widget in self.params_frame.winfo_children():
            widget.destroy()
        self.param_entries.clear()

        op = self.op_var.get()
        params = self.operations[op]["params"]

        for i, p in enumerate(params):
            lbl = tk.Label(self.params_frame, text=p + ":")
            lbl.grid(row=i, column=0, sticky="w")
            ent = tk.Entry(self.params_frame, width=40)
            ent.grid(row=i, column=1, sticky="ew", pady=2)
            self.param_entries.append(ent)

            # Подсказки в описание операции
        self.set_description(op)

    def set_description(self, operation):
        descriptions = {
            "Производная": "Вычисляет производную заданного выражения по переменной.\nПример: Выражение: x**2 + 3*x, Переменная: x",
            "Интеграл": "Вычисляет неопределенный или определенный интеграл.\nПределы интегрирования задаются опционально.",
            "Вычислить выражение": "Вычисляет числовое значение выражения. Подстановки переменных указывайте через запятую, например: x=2,y=3",
            "Упростить": "Упрощает данное математическое выражение.",
            "Ряд Тейлора": "Разлагает выражение в ряд Тейлора около точки с указанным порядком.\nПример: порядок 5, точка разложения 0."
        }
        self.desc_text.delete("1.0", tk.END)
        self.desc_text.insert(tk.END, descriptions.get(operation, ""))

    def calculate(self):
        op = self.op_var.get()
        func = self.operations[op]["func"]
        params = [e.get().strip() for e in self.param_entries]

        try:
            if op == "Производная":
                if len(params) < 2 or not params[0] or not params[1]:
                    raise ValueError("Введите выражение и переменную.")
                result = func(params[0], params[1])

            elif op == "Интеграл":
                if len(params) < 2 or not params[0] or not params[1]:
                    raise ValueError("Введите выражение и переменную.")
                lower = params[2] if len(params) > 2 and params[2] else None
                upper = params[3] if len(params) > 3 and params[3] else None
                result = func(params[0], params[1], lower, upper)

            elif op == "Вычислить выражение":
                expr = params[0]
                substitutions = {}
                if len(params) > 1 and params[1]:
                    # Разбор подстановок переменных вида x=2,y=3
                    try:
                        pairs = [item.strip() for item in params[1].split(",")]
                        for pair in pairs:
                            var, val = pair.split("=")
                            substitutions[var.strip()] = float(val.strip())
                    except Exception:
                        raise ValueError("Неверный формат подстановок (пример: x=2,y=3)")
                result = func(expr, substitutions)

                # result возвращает кортеж (строка, число)
                if isinstance(result, tuple):
                    result = f"Выражение: {result[0]}\nЗначение: {result[1]}"

            elif op == "Упростить":
                if not params[0]:
                    raise ValueError("Введите выражение.")
                result = func(params[0])

            elif op == "Ряд Тейлора":
                if len(params) < 3 or not params[0] or not params[1] or not params[2]:
                    raise ValueError("Введите выражение, переменную и порядок.")
                n = int(params[2])
                x0 = float(params[3]) if len(params) > 3 and params[3] else 0
                result = func(params[0], params[1], n, x0)

            else:
                result = "Неизвестная операция."
        except Exception as e:
            result = f"Ошибка: {str(e)}"

        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, str(result))


if __name__ == "__main__":
    root = tk.Tk()
    app = CalculatorGUI(root)
    root.mainloop()
