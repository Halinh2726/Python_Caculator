import sys
import re

from PyQt5.QtWidgets import (
    QApplication,
    QWidget,
    QLineEdit,
    QPushButton,
    QGridLayout,
    QVBoxLayout,
    QMessageBox
)
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Máy tính cá nhân - PyQt5")
        self.setFixedSize(360, 500)

        self.create_interface()

    def create_interface(self):
        # =========================
        # Ô hiển thị
        # =========================
        self.display = QLineEdit()

        self.display.setPlaceholderText("Nhập biểu thức...")
        self.display.setAlignment(Qt.AlignRight)
        self.display.setMinimumHeight(60)

        self.display.setStyleSheet("""
            QLineEdit {
                font-size: 25px;
                padding: 10px;
                border: 2px solid #555;
                border-radius: 8px;
            }
        """)

        # =========================
        # Layout chính
        # =========================
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.display)

        # =========================
        # Layout các nút
        # =========================
        grid = QGridLayout()
        grid.setSpacing(8)

        buttons = [
            ("(", 0, 0),
            (")", 0, 1),
            ("⌫", 0, 2),
            ("C", 0, 3),

            ("7", 1, 0),
            ("8", 1, 1),
            ("9", 1, 2),
            ("/", 1, 3),

            ("4", 2, 0),
            ("5", 2, 1),
            ("6", 2, 2),
            ("*", 2, 3),

            ("1", 3, 0),
            ("2", 3, 1),
            ("3", 3, 2),
            ("-", 3, 3),

            ("0", 4, 0),
            (".", 4, 1),
            ("=", 4, 2),
            ("+", 4, 3)
        ]

        for text, row, column in buttons:

            button = QPushButton(text)
            button.setMinimumHeight(65)

            button.setStyleSheet("""
                QPushButton {
                    font-size: 20px;
                    border: 1px solid #777;
                    border-radius: 8px;
                    background-color: #eeeeee;
                }

                QPushButton:hover {
                    background-color: #dddddd;
                }

                QPushButton:pressed {
                    background-color: #cccccc;
                }
            """)

            # Xử lý từng loại nút
            if text == "=":
                button.clicked.connect(self.calculate)

            elif text == "C":
                button.clicked.connect(self.clear_display)

            elif text == "⌫":
                button.clicked.connect(self.backspace)

            else:
                button.clicked.connect(
                    lambda checked=False, value=text:
                    self.add_character(value)
                )

            
            grid.addWidget(button, row, column)

        main_layout.addLayout(grid)

        self.setLayout(main_layout)

    # ==========================================================
    # Thêm ký tự vào ô nhập
    # ==========================================================
    def add_character(self, character):
        self.display.insert(character)

    # ==========================================================
    # Xóa toàn bộ
    # ==========================================================
    def clear_display(self):
        self.display.clear()

    # ==========================================================
    # Xóa một ký tự
    # ==========================================================
    def backspace(self):
        text = self.display.text()

        if text:
            self.display.setText(text[:-1])

    # ==========================================================
    # Kiểm tra input
    # ==========================================================
    def validate_input(self, expression):

        # Input rỗng
        if not expression:
            QMessageBox.warning(
                self,
                "Lỗi input",
                "Bạn chưa nhập biểu thức!"
            )
            return False

        # Chỉ cho phép các ký tự này
        allowed_pattern = r"^[0-9+\-*/().\s]+$"

        if not re.fullmatch(allowed_pattern, expression):
            QMessageBox.warning(
                self,
                "Lỗi input",
                "Biểu thức chứa ký tự không hợp lệ!\n"
                "Chỉ được sử dụng số và các phép toán + - * /."
            )
            return False

        # Phải có ít nhất một số
        if not re.search(r"\d", expression):
            QMessageBox.warning(
                self,
                "Lỗi input",
                "Biểu thức phải chứa ít nhất một số!"
            )
            return False

        # Kiểm tra ngoặc
        balance = 0

        for char in expression:

            if char == "(":
                balance += 1

            elif char == ")":
                balance -= 1

                if balance < 0:
                    QMessageBox.warning(
                        self,
                        "Lỗi input",
                        "Dấu ngoặc không hợp lệ!"
                    )
                    return False

        if balance != 0:
            QMessageBox.warning(
                self,
                "Lỗi input",
                "Số lượng dấu ngoặc không cân bằng!"
            )
            return False

        return True

    # ==========================================================
    # Tính toán
    # ==========================================================
    def calculate(self):

        expression = self.display.text().strip()

        # Kiểm tra input
        if not self.validate_input(expression):
            return

        try:
            # Không cho phép truy cập Python builtins
            result = eval(
                expression,
                {"__builtins__": None},
                {}
            )

            # Kiểm tra kết quả
            if result is None:
                raise ValueError("Không có kết quả.")

            if not isinstance(result, (int, float)):
                raise ValueError("Kết quả không hợp lệ.")

            # Tránh kết quả vô hạn
            if result == float("inf") or result == float("-inf"):
                raise ValueError("Kết quả quá lớn.")

            # Nếu là số nguyên thì hiển thị đẹp hơn
            if isinstance(result, float) and result.is_integer():
                result = int(result)

            self.display.setText(str(result))

        # =========================
        # Chia cho 0
        # =========================
        except ZeroDivisionError:
            QMessageBox.critical(
                self,
                "Lỗi tính toán",
                "Không thể chia cho 0!"
            )

        # =========================
        # Sai cú pháp
        # =========================
        except SyntaxError:
            QMessageBox.critical(
                self,
                "Lỗi tính toán",
                "Biểu thức sai cú pháp!\n"
                "Vui lòng kiểm tra lại."
            )

        # =========================
        # Giá trị không hợp lệ
        # =========================
        except ValueError as error:
            QMessageBox.critical(
                self,
                "Lỗi tính toán",
                f"Không thể thực hiện phép tính!\n{error}"
            )

        # =========================
        # Các lỗi khác
        # =========================
        except Exception as error:
            QMessageBox.critical(
                self,
                "Lỗi tính toán",
                f"Đã xảy ra lỗi:\n{error}"
            )


# ==============================================================
# Chương trình chính
# ==============================================================
if __name__ == "__main__":

    app = QApplication(sys.argv)

    calculator = Calculator()
    calculator.show()

    sys.exit(app.exec_())
