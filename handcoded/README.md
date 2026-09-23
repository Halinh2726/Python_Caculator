# May Tinh Ca Nhan - Ban Code Tay

Ung dung may tinh bo tui bang PyQt5, code thu cong theo mo hinh **state machine**
(giong logic may tinh Windows/Casio) - **khong dung `eval()`**.

## Chay chuong trinh

```bash
pip install -r ../requirements.txt
python3 calculator.py
```

## Tinh nang

- Day du 4 phep tinh: `+`, `-`, `*`, `/`
- Cac nut phu: xoa toan bo (`C`), xoa 1 ky tu (`<-`), doi dau (`+/-`), dau cham thap phan
- Ho tro nhap tu ban phim (so, `+ - * /`, `Enter`, `Backspace`, `Esc`)

## Bat loi input

- Khong cho phep nhap 2 dau `.` trong cung 1 so
- Gioi han so chu so toi da (15 chu so) de tranh nhap qua dai / tran hien thi
- Bat `ValueError` khi chuoi dang nhap khong the chuyen thanh so (`float`)

## Bat loi tinh toan

- Chia cho 0 -> bat `ZeroDivisionError`, hien "Error" + thong bao ro rang
- Nhan/tinh ra ket qua qua lon -> tu bat `OverflowError`
- Ket qua khong xac dinh (NaN / Infinity) -> hien thong bao rieng

Loi duoc hien ngay tren giao dien (dong chu do phia duoi man hinh so),
khong dung hop thoai (`QMessageBox`) de khong lam gian doan thao tac cua nguoi dung.
