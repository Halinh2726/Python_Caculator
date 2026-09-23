# Python Calculator - PyQt5

Ung dung may tinh ca nhan (calculator) xay dung bang **PyQt5**, lam theo yeu cau
bai tap: **2 ban cai dat doc lap** cho cung 1 de bai.

| Thu muc | Mo ta |
|---|---|
| [`handcoded/`](handcoded/) | Ban **code tay** - tu viet toan bo logic tinh toan (state machine, khong dung `eval()`) |
| [`vibe-coded/`](vibe-coded/) | Ban **vibe code** - lam voi su ho tro cua AI coding assistant (Claude - Anthropic), dung trinh danh gia bieu thuc an toan dua tren `ast` |

Ca 2 ban deu dap ung day du yeu cau de bai:

- [x] Day du 4 phep tinh: `+`, `-`, `*`, `/`
- [x] Bat loi input (nhap sai dinh dang, ky tu la, cu phap sai, ...)
- [x] Bat loi tinh toan (chia cho 0, tran so, ket qua khong xac dinh, ...)

## Cai dat & chay

```bash
git clone https://github.com/Halinh2726/Python_Caculator.git
cd Python_Caculator
pip install -r requirements.txt

# Ban code tay
python3 handcoded/calculator.py

# Ban vibe code
python3 vibe-coded/calculator.py
```

Yeu cau: Python 3.8+, PyQt5.

## So sanh nhanh 2 ban

| | Code tay (`handcoded/`) | Vibe code (`vibe-coded/`) |
|---|---|---|
| Cach nhap | Bam tung so/phep tinh nhu may tinh bo tui | Go/bam ca bieu thuc, VD `12+5*(3-1)` |
| Cach tinh | Tu code state machine (`current_value`, `pending_operator`, ...), if/elif thu cong | Dung `ast` de parse va tu danh gia cay cu phap (khong `eval()` truc tiep) |
| Cong cu | Tu viet 100% | Duoc AI (Claude) ho tro sinh code tu mo ta yeu cau, sau do kiem tra/chinh sua lai |

Chi tiet tinh nang va cach bat loi cu the cua tung ban xem trong README rieng
cua tung thu muc.

## Ghi chu

- Ban `vibe-coded/` duoc tao voi su ho tro cua Claude (Anthropic) trong Claude Code.
- Ca 2 file da duoc chay thu (offscreen + tuong tac) de kiem tra khong crash va
  xu ly dung cac truong hop loi (chia cho 0, nhap sai, bieu thuc sai cu phap).
