# Quy tắc dựng video — kiểu "Monk Habits Explained"

Phiên bản 1 (18/11/2026), rút từ phân tích 2 phút đầu của 3 kênh mẫu và bản dựng thử lô 12 (đã duyệt mức "tạm ổn").
Khi user góp ý một hình cụ thể, sửa hình đó **và** ghi quy tắc tổng quát vào file này (mục "Nhật ký điều chỉnh").

## 1. Nguyên tắc chung
- Nền phẳng, nét đen, người que — chữ cũng phải phẳng: phông **Fredoka 600**, không bóng đổ mạnh, không gradient.
- Ảnh luôn chuyển động nhẹ; không có khung tĩnh dài hơn ~2 giây mà không có gì mới (chữ, thẻ, phóng).
- **Không áp máy móc**: chỉ thêm chữ khi nó giúp hiểu hoặc tạo nhịp. Trung bình ~1 lớp chữ cho mỗi 2–3 giây video; hình đã tự nói đủ (có chữ "ON", dấu "$"...) thì không thêm chữ.
- Chữ hiện **đúng chữ được đọc** (mốc từ `moc.json`), tối thiểu 1,0 giây trên màn hình (kiem_bang tự dời).
- Chuyển giữa các hình: mờ 0,3 giây (mặc định). Đầu một phần/chương mới: `truot`.

## 2. Chọn cách thể hiện theo nội dung câu
| Câu thoại có… | Lớp chữ (`kieu`) | Chuyển động hình | SFX gợi ý (thu_vien_sfx.json) |
|---|---|---|---|
| năm, số, đơn vị, phần trăm | `so` (số to + `sub` in hoa ngắn) | kb | ting |
| tên người/tổ chức/nhóm xuất hiện lần đầu | `nhan` đặt sát dưới nhân vật | kb | ting |
| từ khóa, khái niệm, câu hỏi chủ đề | `chu` 1–4 từ, viết lại gọn (không chép nguyên câu) | kb | bung_tay / huh (câu hỏi) |
| liệt kê ≥2 thứ ("when and where", "A, B, C") | mỗi thứ một `nhan`, bật đúng lúc đọc tới | kb | ting cho mỗi thẻ |
| lời trích dẫn | `chu` trong ngoặc kép | kb | swoosh |
| tự nhận "chỉ là đoán", ngượng | `chu` trong ngoặc đơn | kb | de_keu (-16 dB) |
| cú lật, điều tệ nhất, câu hỏi tiêu đề | `chu` có 1 từ VIẾT HOA | `dam` | boom (≤ 1 lần/phút) |
| hành động mạnh, nguy hiểm ập tới (đập, leo, cắn, chảy) | không chữ | `dam` vào điểm hành động | bonk / cang / giot / vut |
| mở phần mới ("So,", "Now,", "Here's the thing") | không chữ | `truot` | swoosh_tram (sớm 0,35s) |
| câu thường, hình đã đủ ý | không chữ | kb | không |

- **Đoạn gay cấn/căng thẳng**: đánh dấu `"cang": true` trên các hình đó → SFX tự +2 dB (quy tắc của user).
- SFX dạng vút/swoosh đặt **sớm** 0,25–0,35s trước lúc đổi hình; SFX va chạm/bật đặt **đúng** chữ được đọc.
- Mức SFX mặc định: bung_tay -12, ting -10 đến -12, ding -13, huh -12, boom -11, bonk -9, giot -8, de_keu -16 (dB).

## 3. Đặt chữ trên khung 1920×1080
- Trước khi đặt, chạy `xem_anh.py` và **nhìn** từng hình: chữ đặt vào vùng trống (trời, tường, nền trắng), không đè mặt nhân vật, chủ thể, chữ có sẵn trong ảnh.
- Hình `dam` phóng to 16% quanh (x%, y%) → chủ thể to ra và lệch; để chữ xa điểm phóng.
- `nen: "anh"` (chữ trắng viền đen) cho ảnh có màu; `nen: "trang"` (chữ đen viền trắng) cho ảnh nền trắng.
- Vị trí hay dùng: trên-trái (480,170), trên-phải (1440,170), dưới-giữa (960,930), cạnh-phải (1440,540).
- Sau khi dựng, mở các tấm `kiem_chu_*.jpg` từ `kiem_video.py` và sửa mọi chữ đè/tràn trước khi giao.

## 4. Cấu trúc bang_dung.json
```json
{
 "fps": 30, "ket_thuc": 38.7,
 "hinh": [{"id": "H221", "anh": "/duong/dan/H221.jpg", "bat_dau": 0.0, "cau": "...",
           "chuyen_dong": {"kieu": "kb", "goc": "center|left|right|top"}, "cang": false}],
 "chu":  [{"h": "H228", "kieu": "so", "text": "~200,000", "sub": "ANTS IN ONE COLONY", "t": 16.58, "x": 960, "y": 150},
          {"h": "H222", "kieu": "chu", "text": "Built for predators", "t": 3.11, "x": 520, "y": 150, "nen": "anh"},
          {"h": "H224", "kieu": "nhan", "text": "USDA researchers", "t": 7.41, "x": 1290, "y": 900}],
 "sfx":  [{"h": "H228", "am": "ting", "t": 16.58, "db": -10}],
 "nhac": [{"file": "/duong/dan/nhac.mp3", "tu": 0, "den": 38.7, "db": -12}]
}
```
`chuyen_dong` khác: `{"kieu": "dam", "x": 43, "y": 42}` (phần trăm khung), `{"kieu": "truot"}`.

## 5. Nhạc nền
- Không lời, nhẹ, tò mò (pizzicato, piano nhẹ, lofi). Đoạn căng dùng bài căng hơn.
- Bài nhạc được chuẩn hoá về -16 LUFS rồi áp `db` (mặc định -12 → khoảng -28 LUFS, nằm dưới giọng ~10 dB), tự hạ thêm khi có giọng (sidechain trong `dung.py`). Đổi bài theo phần, mờ vào/ra 1,5s.
- Chỉ dùng nhạc user cung cấp (YouTube Audio Library / nguồn có giấy phép).

## 5b. Chuyển cảnh, hiệu ứng chữ, điểm nhấn giọng (v2, 19/11/2026)
- `hinh[].vao` = kiểu chuyển cảnh vào hình: `mo` (mặc định, mờ 0,3s), `trai`/`phai` (đẩy ngang), `len` (đẩy lên), `quet`/`quet_trai` (quét lộ), `lat` (lật 3D), `zoom` (phóng chuyển cảnh). Hình trước tự đi ra khớp kiểu. Chỉ dùng kiểu khác `mo` ở chỗ mở phần mới / liệt kê (~10% số hình), đổi kiểu luân phiên, không lặp liền nhau.
- `chu[].hieu`: `go` (đánh máy, mặc định cho chu), `pop` (bật), `mo` (mờ + nổi lên), `truot` (+`tu`: trai/phai/duoi), `lo` (lộ dần trái→phải), `dap` (đập mạnh từ to về, cho cú lật / số quan trọng). `mau`: `vang` (thông tin chính), `do` (nguy hiểm/cảnh báo). `het`: cho chữ ở lại sang hình sau khi hình quá ngắn.
- `nhan[]` = điểm nhấn giọng: `dap` (phóng giật + rung, x/y = điểm phóng), `rung`, `flash`, `bat` (cắt vùng x,y,w,h của ảnh `anh`=id hình thành thẻ bật ra). Chọn chỗ bằng phân tích độ lớn/độ kéo dài/ngắt của từng chữ trong giọng, cộng nội dung câu; ~1 lần / 30–40 giây, không liên tiếp. Luôn đi kèm SFX va chạm (`dap`, `bonk`, `set`, `dun_dun`).
- Chọn vị trí chữ tự động bằng `vung_trong.py` (vùng ít nét nhất, tránh điểm phóng và chữ khác), sau đó vẫn phải xem `kiem_chu_*`.
- `canh_moc.py`: số được đọc như người ("1962" → nineteen sixty two, "300" → three hundred); cửa sổ căn theo tốc độ đọc thật — trước đây đọc số từng chữ số làm mốc trôi dần tới hụt.

## 6. Nhật ký điều chỉnh
- 18/11/2026 — lô 12: chữ tối thiểu 1,0s; chữ đen trên nền trắng thêm viền trắng 14px; giữ chữ trong lề 60px; chữ không đặt gần điểm phóng của hình `dam`.
- 19/11/2026 — kien_lua (H012 "...or YOU?"): chữ **không bao giờ** được ở lại sang hình sau. Câu có từ khóa cuối câu mà hình ngắn → dời chữ sớm lên trong chính hình đó; hình quá ngắn (<1s) thì chữ hiện hết thời gian của hình rồi tắt cùng hình. Không dùng trường `het` để kéo chữ qua ranh giới hình. (User duyệt tổng thể bản dựng v2: chuyển cảnh đa dạng + điểm nhấn giọng.)
- 19/11/2026 — kien_lua bản đầy đủ: (1) ảnh Flow thường đã có chữ/số vẽ sẵn (dòng "The only text in the image is…" trong prompt) → đọc dòng đó trước, KHÔNG thêm chữ trùng nội dung; chỉ thêm chữ mang ý mới. (2) Chữ dài >15 ký tự rất dễ đè chủ thể ở ảnh có cảnh nền → rút gọn hoặc đổi sang thẻ `nhan` nhỏ. (3) Số có `sub` cần chừa ~250px chiều cao, không đặt sát đáy khung.
