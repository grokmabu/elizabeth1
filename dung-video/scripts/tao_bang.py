#!/usr/bin/env python3
"""Tạo KHUNG bảng dựng từ moc.json + thư mục ảnh. Claude điền phần chữ/SFX/chuyển động đặc biệt sau.

python3 tao_bang.py --moc moc.json --images "thu_muc_anh" --out bang_dung.json [--lead 0.15]

Ảnh được ghép theo số H### trong tên file (H221_xxx.jpg). Ảnh tên có "b_du_phong"/"b_" sau số (H240b) bị bỏ qua.
Kết quả: mỗi hình có bat_dau (giây), chuyen_dong mặc định "kb" (phóng chậm, đổi gốc luân phiên),
"chu": [] và "sfx": [] để Claude điền theo quy_tac_dung.md.
"""
import argparse, glob, json, os, re, sys

p = argparse.ArgumentParser()
p.add_argument("--moc", required=True)
p.add_argument("--images", required=True)
p.add_argument("--out", default="bang_dung.json")
p.add_argument("--lead", type=float, default=0.15, help="đổi hình sớm hơn tiếng bao nhiêu giây")
p.add_argument("--tail", type=float, default=0.4, help="giữ hình cuối thêm bao lâu sau chữ cuối")
a = p.parse_args()

moc = json.load(open(a.moc, encoding="utf-8"))
imgs = {}
for f in glob.glob(os.path.join(a.images, "*")):
    m = re.match(r"^(H\d{3,4})(?![0-9a-zA-Z])", os.path.basename(f), re.I)
    if m and f.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
        imgs.setdefault(m.group(1).upper(), f)

thieu = [m["id"] for m in moc if m["id"] not in imgs]
hinh, goc = [], ["center", "left", "right", "top"]
for i, m in enumerate(moc):
    if m["id"] not in imgs:
        continue
    bd = 0.0 if not hinh else round(max(m["start"] - a.lead, 0), 2)
    hinh.append({"id": m["id"], "anh": os.path.abspath(imgs[m["id"]]), "bat_dau": bd,
                 "chuyen_dong": {"kieu": "kb", "goc": goc[i % 4]}, "cau": m["line"]})
bang = {"fps": 30, "ket_thuc": round(moc[-1]["end"] + a.tail, 2), "hinh": hinh, "chu": [], "sfx": [], "nhac": []}
json.dump(bang, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"{len(hinh)} hình, dài {bang['ket_thuc']}s -> {a.out}")
if thieu:
    print(f"THIẾU ẢNH ({len(thieu)}): {', '.join(thieu)} — câu của các hình này sẽ nằm trên hình trước đó.")
