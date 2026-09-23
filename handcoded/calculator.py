"""
May Tinh Ca Nhan - BAN CODE TAY (Hand-coded version)
=====================================================
Xay dung bang PyQt5.

Cach tiep can: mo hinh "state machine" co dien (giong may tinh Windows/Casio),
KHONG dung eval()/exec(). Tat ca logic +, -, *, / duoc code thu cong bang if/elif.

Tinh nang:
- Day du 4 phep tinh: cong, tru, nhan, chia
- Bat loi input:
    + Khong cho nhap 2 dau '.' trong 1 so
    + Gioi han so chu so toi da (tranh tran bo nho / hien thi qua dai)
    + Bat ValueError khi chuoi hien tai khong the chuyen thanh so (float)
- Bat loi tinh toan:
    + Chia cho 0 (ZeroDivisionError)
    + Ket qua qua lon (OverflowError tu dinh nghia)
    + Ket qua khong xac dinh (NaN / Infinity)
"""

import sys
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QGridLayout,
    QLineEdit, QPushButton, QLabel, QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont


class Calculator(QWidget):
    MAX_DIGITS = 15  # gioi han so chu so hien thi, tranh tran so

    def __init__(self):
        super().__init__()
        self.current_input = "0"          # chuoi dang hien thi / dang nhap
        self.stored_value = None          # gia tri da luu truoc do
        self.pending_operator = None      # toan tu dang cho ('+', '-', '*', '/')
        self.waiting_for_operand = False  # True: nut so tiep theo se bat dau so moi
        self.error_state = False          # True khi dang hien thi loi

        self.init_ui()

    # ---------------------------------------------------------------- UI ---
    def init_ui(self):
        self.setWindowTitle("May Tinh Ca Nhan - Ban Code Tay")
        self.setFixedSize(320, 430)

        main_layout = QVBoxLayout()

        self.display = QLineEdit(self.current_input)
        self.display.setReadOnly(True)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Consolas", 22))
        self.display.setFixedHeight(60)
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ffffff; border-radius:6px; padding:6px;"
        )
        main_layout.addWidget(self.display)

        # Nhan hien thi thong bao loi ngay tren giao dien (khong dung QMessageBox
        # de tranh hop thoai modal chan nguoi dung sau moi lan bam sai)
        self.status_label = QLabel(" ")
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setFixedHeight(18)
        self.status_label.setFont(QFont("Arial", 10))
        self.status_label.setStyleSheet("color:#ff5555;")
        main_layout.addWidget(self.status_label)

        grid = QGridLayout()
        grid.setSpacing(8)

        # (label, row, col, [row_span, col_span])
        buttons = [
            ("C", 0, 0), ("<-", 0, 1), ("+/-", 0, 2), ("/", 0, 3),
            ("7", 1, 0), ("8", 1, 1), ("9", 1, 2), ("*", 1, 3),
            ("4", 2, 0), ("5", 2, 1), ("6", 2, 2), ("-", 2, 3),
            ("1", 3, 0), ("2", 3, 1), ("3", 3, 2), ("+", 3, 3),
            ("0", 4, 0, 1, 2), (".", 4, 2), ("=", 4, 3),
        ]

        for spec in buttons:
            text = spec[0]
            row, col = spec[1], spec[2]
            row_span = spec[3] if len(spec) > 3 else 1
            col_span = spec[4] if len(spec) > 4 else 1

            btn = QPushButton(text)
            btn.setFont(QFont("Arial", 15))
            btn.setFixedHeight(55)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            btn.clicked.connect(self._make_handler(text))
            self._style_button(btn, text)
            grid.addWidget(btn, row, col, row_span, col_span)

        main_layout.addLayout(grid)
        self.setLayout(main_layout)

    def _style_button(self, btn, text):
        if text in "0123456789.":
            btn.setStyleSheet(
                "QPushButton {background-color:#3a3a3a; color:white; border-radius:8px;}"
                "QPushButton:hover {background-color:#4a4a4a;}"
            )
        elif text in "+-*/":
            btn.setStyleSheet(
                "QPushButton {background-color:#ff9500; color:white; border-radius:8px;}"
                "QPushButton:hover {background-color:#ffaa33;}"
            )
        elif text == "=":
            btn.setStyleSheet(
                "QPushButton {background-color:#2e8b57; color:white; border-radius:8px;}"
                "QPushButton:hover {background-color:#379e64;}"
            )
        else:
            btn.setStyleSheet(
                "QPushButton {background-color:#a5a5a5; color:black; border-radius:8px;}"
                "QPushButton:hover {background-color:#bcbcbc;}"
            )

    def _make_handler(self, text):
        def handler():
            self.on_button(text)
        return handler

    # ------------------------------------------------------- Dieu phoi nut ---
    def on_button(self, text):
        if text.isdigit():
            self.input_digit(text)
        elif text == ".":
            self.input_decimal()
        elif text in ("+", "-", "*", "/"):
            self.input_operator(text)
        elif text == "=":
            self.calculate_result()
        elif text == "C":
            self.clear_all()
        elif text == "<-":
            self.backspace()
        elif text == "+/-":
            self.toggle_sign()

    # ------------------------------------------------------------- Nhap so ---
    def input_digit(self, digit):
        if self.error_state:
            self.clear_all()

        if self.waiting_for_operand:
            self.current_input = digit
            self.waiting_for_operand = False
        else:
            if self.current_input == "0":
                self.current_input = digit
            else:
                # Bat loi input: gioi han so chu so, tranh nhap qua dai
                digits_only = self.current_input.replace("-", "").replace(".", "")
                if len(digits_only) >= self.MAX_DIGITS:
                    return
                self.current_input += digit

        self.update_display()

    def input_decimal(self):
        if self.error_state:
            self.clear_all()

        if self.waiting_for_operand:
            self.current_input = "0."
            self.waiting_for_operand = False
        elif "." not in self.current_input:
            # Bat loi input: khong cho phep 2 dau '.' trong 1 so
            self.current_input += "."

        self.update_display()

    # -------------------------------------------------------- Toan tu / '=' ---
    def input_operator(self, op):
        if self.error_state:
            return

        try:
            value = float(self.current_input)
        except ValueError:
            # Bat loi input: chuoi hien tai khong phai la so hop le
            self.show_error("Input khong hop le")
            return

        if self.pending_operator and not self.waiting_for_operand:
            # Da co toan tu cho -> tinh truoc ket qua trung gian
            # (cho phep bam lien tiep, vi du: 5 + 3 + 2 =)
            if not self.apply_pending_operator(value):
                return
        else:
            self.stored_value = value

        self.pending_operator = op
        self.waiting_for_operand = True

    def apply_pending_operator(self, second_value):
        """Tra ve True neu tinh thanh cong, False neu co loi (da hien thong bao)."""
        try:
            result = self.compute(self.stored_value, second_value, self.pending_operator)
        except ZeroDivisionError:
            # Bat loi tinh toan: chia cho 0
            self.show_error("Khong the chia cho 0")
            return False
        except OverflowError:
            # Bat loi tinh toan: ket qua qua lon
            self.show_error("Ket qua qua lon, vuot gioi han")
            return False
        except Exception as exc:  # bat moi loi tinh toan phat sinh khac
            self.show_error(f"Loi tinh toan: {exc}")
            return False

        if result != result or result in (float("inf"), float("-inf")):
            # NaN hoac vo cuc
            self.show_error("Ket qua khong xac dinh")
            return False

        self.stored_value = result
        self.current_input = self.format_number(result)
        return True

    def compute(self, a, b, op):
        """Thuc hien 1 trong 4 phep tinh co ban. Khong dung eval()."""
        if op == "+":
            return a + b
        elif op == "-":
            return a - b
        elif op == "*":
            result = a * b
            if abs(result) > 1e15:
                raise OverflowError
            return result
        elif op == "/":
            if b == 0:
                raise ZeroDivisionError
            return a / b
        else:
            raise ValueError(f"Toan tu khong xac dinh: {op}")

    def calculate_result(self):
        if self.error_state:
            return
        if self.pending_operator is None:
            return  # Chua co phep tinh nao de thuc hien

        try:
            second_value = float(self.current_input)
        except ValueError:
            self.show_error("Input khong hop le")
            return

        if self.apply_pending_operator(second_value):
            self.pending_operator = None
            self.waiting_for_operand = True
            self.update_display()

    # ---------------------------------------------------------- Tien ich ---
    def clear_all(self):
        self.current_input = "0"
        self.stored_value = None
        self.pending_operator = None
        self.waiting_for_operand = False
        self.error_state = False
        self.status_label.setText(" ")
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ffffff; border-radius:6px; padding:6px;"
        )
        self.update_display()

    def backspace(self):
        if self.error_state or self.waiting_for_operand:
            return
        if len(self.current_input) <= 1 or (
            len(self.current_input) == 2 and self.current_input[0] == "-"
        ):
            self.current_input = "0"
        else:
            self.current_input = self.current_input[:-1]
        self.update_display()

    def toggle_sign(self):
        if self.error_state:
            return
        try:
            value = float(self.current_input)
        except ValueError:
            self.show_error("Input khong hop le")
            return
        self.current_input = self.format_number(-value)
        self.update_display()

    def show_error(self, message):
        self.error_state = True
        self.current_input = "0"
        self.stored_value = None
        self.pending_operator = None
        self.waiting_for_operand = False
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ff5555; border-radius:6px; padding:6px;"
        )
        self.display.setText("Error")
        self.status_label.setText(message)

    @staticmethod
    def format_number(value):
        if value == int(value) and abs(value) < 1e15:
            return str(int(value))
        text = f"{value:.10f}".rstrip("0").rstrip(".")
        return text if text else "0"

    def update_display(self):
        self.display.setText(self.current_input)

    # ------------------------------------------------------ Ban phim that ---
    def keyPressEvent(self, event):
        key = event.key()
        text = event.text()
        if text.isdigit():
            self.input_digit(text)
        elif text == ".":
            self.input_decimal()
        elif text in ("+", "-", "*", "/"):
            self.input_operator(text)
        elif key in (Qt.Key_Enter, Qt.Key_Return, Qt.Key_Equal):
            self.calculate_result()
        elif key == Qt.Key_Backspace:
            self.backspace()
        elif key == Qt.Key_Escape:
            self.clear_all()


def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
