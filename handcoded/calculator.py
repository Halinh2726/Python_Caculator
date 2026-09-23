import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QGridLayout, QLineEdit, QPushButton, QWidget


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.first_number = None
        self.operator = None
        self.new_number = True
        self.create_ui()

    def create_ui(self):
        self.setWindowTitle("Calculator")
        self.setFixedSize(300, 400)

        layout = QGridLayout(self)

        self.display = QLineEdit("0")
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("font-size: 24px; padding: 10px;")
        layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ("C", 1, 0), ("<-", 1, 1), ("+/-", 1, 2), ("/", 1, 3),
            ("7", 2, 0), ("8", 2, 1), ("9", 2, 2), ("*", 2, 3),
            ("4", 3, 0), ("5", 3, 1), ("6", 3, 2), ("-", 3, 3),
            ("1", 4, 0), ("2", 4, 1), ("3", 4, 2), ("+", 4, 3),
            ("0", 5, 0), (".", 5, 1), ("=", 5, 2),
        ]

        for text, row, column in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 18px;")
            button.clicked.connect(lambda checked, value=text: self.click(value))
            if text == "0":
                layout.addWidget(button, row, column, 1, 2)
            elif text in (".", "="):
                layout.addWidget(button, row, column + 1)
            else:
                layout.addWidget(button, row, column)

    def click(self, value):
        if value.isdigit():
            self.input_number(value)
        elif value == ".":
            self.input_decimal()
        elif value in "+-*/":
            self.set_operator(value)
        elif value == "=":
            self.calculate()
        elif value == "C":
            self.clear()
        elif value == "<-":
            self.backspace()
        elif value == "+/-":
            self.change_sign()

    def input_number(self, number):
        if self.new_number or self.display.text() == "Error":
            self.display.setText(number)
            self.new_number = False
        elif self.display.text() == "0":
            self.display.setText(number)
        else:
            self.display.setText(self.display.text() + number)

    def input_decimal(self):
        if self.new_number or self.display.text() == "Error":
            self.display.setText("0.")
            self.new_number = False
        elif "." not in self.display.text():
            self.display.setText(self.display.text() + ".")

    def set_operator(self, operator):
        if self.display.text() == "Error":
            return

        if self.operator and not self.new_number:
            self.calculate()

        if self.display.text() != "Error":
            self.first_number = float(self.display.text())
            self.operator = operator
            self.new_number = True

    def calculate(self):
        if self.first_number is None or self.operator is None or self.new_number:
            return

        second_number = float(self.display.text())

        try:
            if self.operator == "+":
                result = self.first_number + second_number
            elif self.operator == "-":
                result = self.first_number - second_number
            elif self.operator == "*":
                result = self.first_number * second_number
            else:
                result = self.first_number / second_number

            if result.is_integer():
                result = int(result)
            self.display.setText(str(result))
        except ZeroDivisionError:
            self.display.setText("Error")

        self.first_number = None
        self.operator = None
        self.new_number = True

    def clear(self):
        self.display.setText("0")
        self.first_number = None
        self.operator = None
        self.new_number = True

    def backspace(self):
        if self.new_number or self.display.text() == "Error":
            return

        text = self.display.text()[:-1]
        self.display.setText(text if text and text != "-" else "0")

    def change_sign(self):
        if self.display.text() not in ("0", "Error"):
            if self.display.text().startswith("-"):
                self.display.setText(self.display.text()[1:])
            else:
                self.display.setText("-" + self.display.text())

    def keyPressEvent(self, event):
        text = event.text()

        if text.isdigit() or text in ".+-*/=":
            self.click(text)
        elif event.key() in (Qt.Key_Return, Qt.Key_Enter):
            self.calculate()
        elif event.key() == Qt.Key_Backspace:
            self.backspace()
        elif event.key() == Qt.Key_Escape:
            self.clear()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    calculator = Calculator()
    calculator.show()
    sys.exit(app.exec_())
