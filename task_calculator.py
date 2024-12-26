import tkinter as tk
from tkinter import messagebox
import re
from datetime import datetime
import unittest
import io


def calculate_expression(expression):
    try:
        result = eval(expression)
        return result
    except ZeroDivisionError:
        return "Division by zero error"
    except Exception as e:
        return str(e)


class TaskCalculatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Task Calculator")

        self.tasks = []

        self.input_frame = tk.Frame(root)
        self.input_frame.pack(pady=10)

        tk.Label(self.input_frame, text="Task Name:").grid(row=0, column=0, padx=5, pady=5)
        self.task_name_entry = tk.Entry(self.input_frame, width=20)
        self.task_name_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(self.input_frame, text="Expression:").grid(row=1, column=0, padx=5, pady=5)
        self.expression_entry = tk.Entry(self.input_frame, width=20)
        self.expression_entry.grid(row=1, column=1, padx=5, pady=5)

        self.save_button = tk.Button(self.input_frame, text="Save", command=self.save_task)
        self.save_button.grid(row=2, column=0, columnspan=2, pady=10)

        self.tasks_frame = tk.Frame(root)
        self.tasks_frame.pack(pady=10)

    def save_task(self):
        task_name = self.task_name_entry.get().strip()
        expression = self.expression_entry.get().strip()

        if not task_name:
            messagebox.showerror("Error", "Task name cannot be empty.")
            return

        if not expression:
            messagebox.showerror("Error", "Expression cannot be empty.")
            return

        for task in self.tasks:
            if task["name"] == task_name:
                messagebox.showerror("Error", "Task name must be unique.")
                return

        test_result = self.run_validation_tests(expression)
        if not test_result.wasSuccessful():
            errors = "\n".join([self.extract_error_message(failure) for failure in test_result.failures])
            messagebox.showerror("Error", errors)
            return

        task_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        task = {"name": task_name, "expression": expression, "time": task_time}
        self.tasks.append(task)

        self.display_task(task)

        self.task_name_entry.delete(0, tk.END)
        self.expression_entry.delete(0, tk.END)

    def display_task(self, task):
        task_frame = tk.Frame(self.tasks_frame, borderwidth=1, relief="solid", pady=5, padx=5)
        task_frame.pack(fill="x", pady=5)

        tk.Label(task_frame, text=f"Task: {task['name']}", font=("Arial", 12, "bold")).pack(anchor="w")

        tk.Label(task_frame, text=f"Expression: {task['expression']}", font=("Arial", 10)).pack(anchor="w")
        tk.Label(task_frame, text=f"Created at: {task['time']}", font=("Arial", 8, "italic")).pack(anchor="w")

        buttons_frame = tk.Frame(task_frame)
        buttons_frame.pack(anchor="e", pady=5)

        load_button = tk.Button(buttons_frame, text="Load", command=lambda: self.load_task(task))
        load_button.pack(side="left", padx=5)

        run_button = tk.Button(buttons_frame, text="Run", command=lambda: self.run_task(task))
        run_button.pack(side="left", padx=5)

        delete_button = tk.Button(buttons_frame, text="Delete", command=lambda: self.delete_task(task_frame, task))
        delete_button.pack(side="left", padx=5)

    def load_task(self, task):
        self.task_name_entry.delete(0, tk.END)
        self.task_name_entry.insert(0, task["name"])

        self.expression_entry.delete(0, tk.END)
        self.expression_entry.insert(0, task["expression"])

    def run_task(self, task):
        result = calculate_expression(task["expression"])
        messagebox.showinfo("Result", f"Result: {result}")

    def delete_task(self, task_frame, task):
        task_frame.destroy()
        self.tasks.remove(task)

    def run_validation_tests(self, expression):
        class TestValidateExpression(unittest.TestCase):
            def test_valid_expression(self):
                if not re.match(r'^[\d+\-*/().\s]+$', expression):
                    self.fail("Expression contains invalid characters.")
                if re.search(r'[\+\-\*/]{2,}', expression):
                    self.fail("Expression contains consecutive operators.")
                stack = []
                for char in expression:
                    if char == '(':
                        stack.append(char)
                    elif char == ')':
                        if not stack:
                            self.fail("Mismatched parentheses.")
                        stack.pop()
                if stack:
                    self.fail("Mismatched parentheses.")

            def test_zero_division(self):
                try:
                    eval(expression)
                except ZeroDivisionError:
                    self.fail("Division by zero error")
                except:
                    pass

        suite = unittest.TestLoader().loadTestsFromTestCase(TestValidateExpression)
        runner = unittest.TextTestRunner(stream=io.StringIO())
        result = runner.run(suite)
        return result

    def extract_error_message(self, failure):
        return failure[1].split("\n")[-2]


if __name__ == "__main__":
    root = tk.Tk()
    app = TaskCalculatorApp(root)
    root.mainloop()