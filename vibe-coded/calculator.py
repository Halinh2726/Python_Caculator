"""
May Tinh Ca Nhan - BAN VIBE CODE (AI-assisted version)
=======================================================
Xay dung bang PyQt5.

Duoc tao ra voi su ho tro cua AI coding assistant (Claude - Anthropic),
theo phong cach "vibe coding": mo ta yeu cau bang ngon ngu tu nhien, AI sinh code,
nguoi dung doc lai / chinh sua / chay thu de kiem tra.

Cach tiep can nay KHAC voi ban code tay (handcoded/calculator.py):
- O day, man hinh la mot O NHAP BIEU THUC (giong may tinh tren dien thoai),
  nguoi dung co the go ca chuoi vi du "12+5*(3-1)" roi bam "=".
- Bieu thuc duoc phan tich va tinh bang mot TRINH DANH GIA AN TOAN dua tren
  module `ast` cua Python (KHONG dung eval()/exec() truc tiep tren input cua
  nguoi dung, de tranh nguy co thuc thi ma doc hai / code injection).

Tinh nang:
- Day du 4 phep tinh: +, -, *, / (co ho tro dau ngoac va so am)
- Bat loi input:
    + QRegExpValidator chan ky tu la (chi cho phep so, . + - * / ( ) va khoang trang)
    + Kiem tra bieu thuc "hop le tam thoi" ngay khi go (khong cho 2 toan tu lien tiep,...)
    + Bat SyntaxError / ValueError khi bieu thuc khong dung cu phap luc bam '='
- Bat loi tinh toan:
    + Chia cho 0 -> ZeroDivisionError duoc bat va bao loi ro rang
    + Tran so / ket qua qua lon -> OverflowError
    + Loi khong luong truoc duoc -> Exception chung, khong lam crash ung dung
"""

import ast
import operator
import sys

from PyQt5.QtCore import Qt, QRegExp
from PyQt5.QtGui import QFont, QRegExpValidator
from PyQt5.QtWidgets import (
    QApplication,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QSizePolicy,
    QVBoxLayout,
    QWidget,
)


# --------------------------------------------------------------------------- #
#  Trinh danh gia bieu thuc an toan (an toan hon eval())
# --------------------------------------------------------------------------- #
_ALLOWED_BIN_OPS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
}
_ALLOWED_UNARY_OPS = {
    ast.UAdd: operator.pos,
    ast.USub: operator.neg,
}


class CalculationError(Exception):
    """Loi phat sinh trong qua trinh danh gia bieu thuc (loi tinh toan)."""


def safe_eval(expression: str) -> float:
    """
    Danh gia an toan mot bieu thuc so hoc chi gom +, -, *, /, (), so thap phan
    va dau am/duong. Dung module `ast` de parse va tu duyet cay cu phap thay vi
    goi eval()/exec() truc tiep tren chuoi nguoi dung nhap.
    """
    if not expression or not expression.strip():
        raise ValueError("Bieu thuc rong")

    try:
        tree = ast.parse(expression, mode="eval")
    except SyntaxError as exc:
        raise ValueError(f"Cu phap khong hop le: {exc.msg}") from exc

    return _eval_node(tree.body)


def _eval_node(node):
    if isinstance(node, ast.Constant):
        if isinstance(node.value, (int, float)):
            return float(node.value)
        raise ValueError("Chi cho phep gia tri so")

    if isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_BIN_OPS:
            raise ValueError("Toan tu khong duoc ho tro")

        left = _eval_node(node.left)
        right = _eval_node(node.right)

        if op_type is ast.Div and right == 0:
            raise CalculationError("Khong the chia cho 0")

        try:
            result = _ALLOWED_BIN_OPS[op_type](left, right)
        except OverflowError as exc:
            raise CalculationError("Ket qua qua lon, vuot gioi han tinh toan") from exc

        if abs(result) > 1e18:
            raise CalculationError("Ket qua qua lon, vuot gioi han tinh toan")

        return result

    if isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type not in _ALLOWED_UNARY_OPS:
            raise ValueError("Toan tu khong duoc ho tro")
        return _ALLOWED_UNARY_OPS[op_type](_eval_node(node.operand))

    # Bat tat ca cac dang node khac (goi ham, ten bien, list, ...) -> khong cho phep
    raise ValueError("Bieu thuc chua thanh phan khong duoc phep")


def format_result(value: float) -> str:
    if value != value or value in (float("inf"), float("-inf")):
        raise CalculationError("Ket qua khong xac dinh")
    if value == int(value) and abs(value) < 1e15:
        return str(int(value))
    text = f"{value:.10f}".rstrip("0").rstrip(".")
    return text if text else "0"


# --------------------------------------------------------------------------- #
#  Giao dien
# --------------------------------------------------------------------------- #
class Calculator(QWidget):
    OPERATORS = "+-*/"

    def __init__(self):
        super().__init__()
        self.expression = ""
        self._build_ui()

    def _build_ui(self):
        self.setWindowTitle("May Tinh Ca Nhan - Ban Vibe Code")
        self.setFixedSize(340, 470)

        layout = QVBoxLayout()

        # Nhan nho hien thi lai bieu thuc dang go (ho tro nguoi dung theo doi)
        self.history_label = QLabel("")
        self.history_label.setAlignment(Qt.AlignRight)
        self.history_label.setStyleSheet("color:#888888;")
        self.history_label.setFont(QFont("Consolas", 11))
        layout.addWidget(self.history_label)

        # O nhap bieu thuc - CHO PHEP GO TRUC TIEP tu ban phim, co Validator
        # de chan ky tu la ngay tu buoc nhap (bat loi input som).
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setFont(QFont("Consolas", 22))
        self.display.setFixedHeight(60)
        self.display.setPlaceholderText("0")
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ffffff; border-radius:6px; padding:6px;"
        )
        # Chi chap nhan: chu so, dau cham, 4 phep toan, ngoac don, khoang trang
        validator = QRegExpValidator(QRegExp(r"[0-9.\+\-\*/\(\)\s]*"))
        self.display.setValidator(validator)
        self.display.textChanged.connect(self._on_text_changed)
        self.display.returnPressed.connect(self.evaluate_expression)
        layout.addWidget(self.display)

        self.status_label = QLabel(" ")
        self.status_label.setAlignment(Qt.AlignRight)
        self.status_label.setFixedHeight(18)
        self.status_label.setFont(QFont("Arial", 10))
        layout.addWidget(self.status_label)

        grid = QGridLayout()
        grid.setSpacing(8)

        buttons = [
            ("C", 0, 0), ("(", 0, 1), (")", 0, 2), ("/", 0, 3),
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
            btn.clicked.connect(lambda _checked, t=text: self._on_button(t))
            self._style_button(btn, text)
            grid.addWidget(btn, row, col, row_span, col_span)

        layout.addLayout(grid)
        self.setLayout(layout)

    def _style_button(self, btn, text):
        if text.isdigit() or text == ".":
            btn.setStyleSheet(
                "QPushButton {background-color:#3a3a3a; color:white; border-radius:8px;}"
                "QPushButton:hover {background-color:#4a4a4a;}"
            )
        elif text in self.OPERATORS:
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

    # ------------------------------------------------------------ Su kien ---
    def _on_button(self, text):
        if text == "C":
            self.clear_all()
        elif text == "=":
            self.evaluate_expression()
        else:
            self._append_text(text)

    def _append_text(self, text):
        # Bat loi input: khong cho go 2 toan tu lien tiep (tru dau '-' de nhap so am)
        if text in self.OPERATORS and self.display.text():
            last_char = self.display.text().rstrip()[-1:] if self.display.text().strip() else ""
            if last_char in self.OPERATORS and not (text == "-" and last_char in "+*/("):
                self.status_label.setText("Khong the nhap 2 toan tu lien tiep")
                self.status_label.setStyleSheet("color:#ff8888;")
                return

        self.status_label.setText(" ")
        self.display.setText(self.display.text() + text)
        self.display.setCursorPosition(len(self.display.text()))

    def _on_text_changed(self, text):
        # Cap nhat dong lich su moi khi nguoi dung go tay truc tiep vao o nhap
        self.history_label.setText(text)
        self.status_label.setText(" ")
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ffffff; border-radius:6px; padding:6px;"
        )

    def clear_all(self):
        self.display.clear()
        self.history_label.setText("")
        self.status_label.setText(" ")
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ffffff; border-radius:6px; padding:6px;"
        )

    def evaluate_expression(self):
        raw_expression = self.display.text().strip()

        if not raw_expression:
            return  # Khong co gi de tinh

        try:
            value = safe_eval(raw_expression)
            result_text = format_result(value)
        except CalculationError as exc:
            # Bat loi tinh toan: chia cho 0, tran so, ket qua khong xac dinh...
            self._show_error(str(exc))
            return
        except ZeroDivisionError:
            self._show_error("Khong the chia cho 0")
            return
        except (ValueError, SyntaxError, TypeError) as exc:
            # Bat loi input: bieu thuc nguoi dung go bi sai cu phap / khong hop le
            self._show_error(f"Input khong hop le: {exc}")
            return
        except RecursionError:
            self._show_error("Bieu thuc qua phuc tap")
            return
        except Exception as exc:  # phong ngua moi loi khong luong truoc duoc
            self._show_error(f"Loi khong xac dinh: {exc}")
            return

        self.history_label.setText(raw_expression + " =")
        self.display.setText(result_text)
        self.status_label.setText(" ")

    def _show_error(self, message):
        self.status_label.setText(message)
        self.status_label.setStyleSheet("color:#ff5555;")
        self.display.setStyleSheet(
            "background-color:#1e1e1e; color:#ff5555; border-radius:6px; padding:6px;"
        )

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Escape:
            self.clear_all()
        else:
            super().keyPressEvent(event)


def main():
    app = QApplication(sys.argv)
    window = Calculator()
    window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
