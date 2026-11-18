#!/usr/bin/env python3
"""Kiểm tra và TỰ SỬA bảng dựng trước khi dựng, rồi in bảng tóm tắt để user duyệt.

python3 kiem_bang.py bang_dung.json --sfx-dir sfx [--markdown bang_duyet.md]

Tự sửa (ghi đè file):
  - chữ hiện ít nhất 1,0 giây (dời sớm lại nếu từ khóa rơi cuối câu; không sớm hơn đầu hình + 0,1s)
  - giữ chữ trong khung (lề 60px), ước bề rộng theo số ký tự
  - SFX đi kèm chữ (bung_tay/ting/ding/huh/pop) dời theo chữ nếu chữ bị dời
  - hình đánh dấu "cang": true -> SFX của hình đó +2 dB (đúng một lần, ghi cờ "da_cong")
Báo lỗi (không tự sửa): ảnh không tồn tại, SFX thiếu file, hai chữ chồng nhau cùng lúc trên một hình.
"""
import argparse, json, os, sys

p = argparse.ArgumentParser()
p.add_argument("bang")
p.add_argument("--sfx-dir", default="sfx")
p.add_argument("--markdown")
a = p.parse_args()
b = json.load(open(a.bang, encoding="utf-8"))

H = b["hinh"]; ids = [h["id"] for h in H]; st = {h["id"]: h["bat_dau"] for h in H}
het = lambda hid: st[ids[ids.index(hid) + 1]] if ids.index(hid) + 1 < len(ids) else b["ket_thuc"]
loi, sua = [], []
cang = {h["id"] for h in H if h.get("cang")}

for h in H:
    if not os.path.exists(h["anh"]):
        loi.append(f"{h['id']}: không thấy ảnh {h['anh']}")

FS = {"chu": 112, "nhan": 62, "so": 150}
for c in b["chu"]:
    if c["h"] not in st:
        loi.append(f"chữ '{c['text']}' gắn vào hình không có: {c['h']}"); continue
    old = c["t"]
    c["t"] = round(max(min(c["t"], het(c["h"]) - 1.0), st[c["h"]] + 0.1), 2)
    if abs(c["t"] - old) > 0.01:
        sua.append(f"{c['h']} '{c['text']}': {old}s -> {c['t']}s (hiện {het(c['h']) - c['t']:.2f}s)")
        for s in b["sfx"]:
            if s.get("h") == c["h"] and s["am"] in ("bung_tay", "ting", "ding", "huh", "pop") and abs(s["t"] - old) < 0.05:
                s["t"] = c["t"]
    w = len(c["text"]) * FS.get(c["kieu"], 112) * 0.52 / 2
    x = int(min(max(c["x"], 60 + w), 1920 - 60 - w))
    if x != c["x"]:
        sua.append(f"{c['h']} '{c['text']}': x {c['x']} -> {x} (giữ trong khung)"); c["x"] = x

for hid in ids:   # chữ chồng nhau
    cs = sorted([c for c in b["chu"] if c["h"] == hid], key=lambda c: c["t"])
    for i in range(len(cs)):
        for j in range(i + 1, len(cs)):
            if abs(cs[i]["x"] - cs[j]["x"]) < 300 and abs(cs[i]["y"] - cs[j]["y"]) < 120:
                loi.append(f"{hid}: '{cs[i]['text']}' và '{cs[j]['text']}' chồng chỗ nhau")

for s in b["sfx"]:
    if not os.path.exists(os.path.join(a.sfx_dir, s["am"] + ".wav")):
        loi.append(f"thiếu SFX {s['am']}.wav trong {a.sfx_dir}")
    if s.get("h") in cang and not s.get("da_cong"):
        s["db"] += 2; s["da_cong"] = True

json.dump(b, open(a.bang, "w"), ensure_ascii=False, indent=1)

# Bảng tóm tắt cho user duyệt
ten = {"kb": "phóng chậm", "dam": "phóng nhanh", "truot": "trượt vào"}
dong = ["| Hình | Bắt đầu | Chuyển động | Chữ trên hình | Âm thanh |", "|---|---|---|---|---|"]
for h in H:
    chu = "; ".join((f"**{c['text']}**" + (f" / {c['sub']}" if c.get("sub") else "")) for c in b["chu"] if c["h"] == h["id"]) or "—"
    am = ", ".join(s["am"] for s in b["sfx"] if s.get("h") == h["id"]) or "—"
    dong.append(f"| {h['id']}{' ⚡' if h['id'] in cang else ''} | {h['bat_dau']:.1f}s | {ten.get(h['chuyen_dong']['kieu'], '?')} | {chu} | {am} |")
md = "\n".join(dong)
if a.markdown:
    open(a.markdown, "w", encoding="utf-8").write(md + "\n")
print(md)
print(f"\nĐã tự sửa {len(sua)} chỗ:" if sua else "\nKhông cần tự sửa.")
for s in sua: print("  -", s)
if loi:
    print(f"\nLỖI cần xử lý ({len(loi)}):"); [print("  -", l) for l in loi]; sys.exit(1)
