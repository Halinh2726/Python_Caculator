# May Tinh Ca Nhan - Ban Vibe Code

Ung dung may tinh bo tui bang PyQt5, duoc xay dung theo phong cach **vibe coding**:
mo ta yeu cau bang ngon ngu tu nhien cho AI coding assistant (Claude - Anthropic),
AI sinh code, sau do doc lai / kiem tra / chinh sua truoc khi chay.

## Chay chuong trinh

```bash
pip install -r ../requirements.txt
python3 calculator.py
```

## Diem khac biet so voi ban code tay

O nay man hinh la **o nhap bieu thuc** (giong may tinh dien thoai): co the go/bam
ca chuoi vi du `12+5*(3-1)` roi bam `=`, thay vi tinh tung buoc mot.

Bieu thuc duoc danh gia bang mot **trinh danh gia an toan tu viet (`safe_eval`)**
dua tren module `ast` cua Python, tu duyet cay cu phap va chi cho phep so +
4 phep toan + dau ngoac + dau am. Khong goi `eval()`/`exec()` truc tiep tren
chuoi nguoi dung nhap, de tranh nguy co thuc thi ma doc hai (vi du nhap
`__import__('os').system(...)` se bi tu choi ngay).

## Tinh nang

- Day du 4 phep tinh: `+`, `-`, `*`, `/`, co ho tro dau ngoac `()` va so am
- Go truc tiep bang ban phim hoac bam nut deu duoc
- Dong "lich su" nho phia tren hien lai bieu thuc vua tinh

## Bat loi input

- `QRegExpValidator` chan ky tu la ngay luc go (chi cho phep so, `. + - * / ( )`, khoang trang)
- Chan nhap 2 toan tu lien tiep (tru truong hop dau `-` cho so am)
- Bat `SyntaxError` / `ValueError` khi bieu thuc sai cu phap luc bam `=`

## Bat loi tinh toan

- Chia cho 0 -> loi rieng `CalculationError("Khong the chia cho 0")`
- Ket qua qua lon / tran so -> bat va bao "vuot gioi han tinh toan"
- Ket qua khong xac dinh (NaN/Infinity) -> thong bao rieng
- Moi loai loi khac deu duoc bat gon trong `try/except`, khong lam crash ung dung

Thong bao loi hien ngay duoi o nhap (dong chu do), khong dung hop thoai chan
luong thao tac cua nguoi dung.
