# dung-video — dựng video giải thích kiểu Monk tự động

Đầu vào: file prompt ảnh theo lô (`### H221` + `[m:ss] câu thoại`), thư mục ảnh `H221_*.jpg…`, file giọng MiniMax,
thư mục SFX (`Downloads/All in here/Am_thanh`), nhạc nền (tuỳ chọn). Đầu ra: MP4 1080p đăng thẳng YouTube.

```
scripts/sua_giong.py   cắt lặng >0,3s, nhanh x1.1 giữ cao độ
scripts/canh_moc.py    mốc thật từng câu + từng chữ (căn offline, chia đoạn cho video dài)
scripts/tao_bang.py    khung bảng dựng từ mốc + ảnh
scripts/xem_anh.py     lưới ảnh có số H### + toạ độ để đặt chữ
scripts/kiem_bang.py   tự sửa bảng (chữ ≥1s, trong khung, +2dB đoạn căng) + bảng tóm tắt để duyệt
scripts/lay_sfx.py     chuẩn hoá SFX từ thư viện theo thu_vien_sfx.json
scripts/dung.py        Remotion dựng hình -> FFmpeg trộn giọng + SFX + nhạc tự hạ
scripts/kiem_video.py  kiểm định dạng/tiếng/độ dài + tấm khung hình để xem chữ
remotion/              thành phần Remotion (phông Fredoka)
quy_tac_dung.md        quy tắc chọn chữ/chuyển động/SFX (cập nhật theo góp ý)
```

Cài một lần: `pip install --break-system-packages pocketsphinx` · `cd remotion && npm install`.
Remotion miễn phí cho cá nhân và công ty ≤3 người.
