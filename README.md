# Python Calculator - PyQt5

Du an gom hai ung dung may tinh duoc viet bang Python va PyQt5.

| Thu muc | Mo ta |
|---|---|
| [`handcoded/`](handcoded/) | Ban co ban, bam tung so va phep tinh nhu may tinh bo tui |
| [`vibe-coded/`](vibe-coded/) | Ban nhap bieu thuc, dung `ast` de tinh toan an toan |

## Tinh nang chung

- Cong, tru, nhan va chia
- Ho tro so thap phan va so am
- Xu ly loi chia cho 0
- Giao dien bang PyQt5

## Cai dat

```bash
git clone https://github.com/Halinh2726/Python_Caculator.git
cd Python_Caculator
pip install -r requirements.txt
```

## Chay ban co ban

```bash
python3 handcoded/calculator.py
```

Ban co ban su dung cac bien `first_number`, `operator` va `new_number`
de luu trang thai. Cac phep tinh duoc xu ly bang `if/elif`, khong dung
`eval()`.

## Chay ban nhap bieu thuc

```bash
python3 vibe-coded/calculator.py
```

Ban nay cho phep nhap bieu thuc nhu `12 + 5 * (3 - 1)` va dung module
`ast` de phan tich bieu thuc.

## Yeu cau

- Python 3.8 tro len
- PyQt5 5.15 tro len
