#!/usr/bin/env python3
"""Kiểm tra video trước khi giao + cắt khung hình để Claude xem bằng mắt.

python3 kiem_video.py --video video.mp4 --bang bang_dung.json --ra thu_muc_kiem

Kiểm: chuẩn hình yuv420p/High (phát được trên điện thoại), có tiếng, độ dài khớp bảng, âm lượng.
Xuất: kiem_chu_XX.jpg — mỗi chữ trên hình chụp lúc đã hiện đầy đủ (15 ô/tấm);
      kiem_nhip_XX.jpg — cứ 4 giây một khung (30 ô/tấm) để xem nhịp chung.
Claude PHẢI mở các tấm kiem_chu_* để xem chữ có đè lên chủ thể, tràn mép, khó đọc không.
"""
import argparse, json, os, subprocess, sys

p = argparse.ArgumentParser()
p.add_argument("--video", required=True)
p.add_argument("--bang", required=True)
p.add_argument("--ra", default="kiem")
a = p.parse_args()
os.makedirs(a.ra, exist_ok=True)
b = json.load(open(a.bang, encoding="utf-8"))

def probe(entries):
    return subprocess.run(["ffprobe", "-v", "error", "-show_entries", entries, "-of", "json", a.video],
                          capture_output=True, text=True).stdout
info = json.loads(probe("stream=codec_type,profile,pix_fmt:format=duration"))
loi = []
v = [s for s in info["streams"] if s["codec_type"] == "video"]
au = [s for s in info["streams"] if s["codec_type"] == "audio"]
if not v or v[0].get("pix_fmt") != "yuv420p": loi.append("hình không phải yuv420p (điện thoại có thể không phát)")
if not au: loi.append("KHÔNG CÓ TIẾNG")
dur = float(info["format"]["duration"])
if abs(dur - b["ket_thuc"]) > 0.2: loi.append(f"độ dài {dur:.1f}s lệch bảng {b['ket_thuc']}s")
vol = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.video, "-af", "volumedetect", "-vn", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
mx = [l for l in vol.splitlines() if "max_volume" in l]
print("Âm lượng:", mx[0].split("]")[-1].strip() if mx else "?")

ids = [h["id"] for h in b["hinh"]]; st = {h["id"]: h["bat_dau"] for h in b["hinh"]}
het = lambda hid: st[ids[ids.index(hid) + 1]] if ids.index(hid) + 1 < len(ids) else b["ket_thuc"]
fr = []
for c in b["chu"]:
    t_full = c["t"] + min(len(c["text"]) * 0.035, 0.6) + 0.15
    fr.append(int(min(t_full, het(c["h"]) - 0.2) * 30))
def sheets(frames, ten, cols, rows, w):
    frames = sorted(set(frames)); k = cols * rows
    for i in range(0, len(frames), k):
        sel = "+".join(f"eq(n\\,{f})" for f in frames[i:i + k])
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", a.video, "-vf",
                        f"select='{sel}',scale={w}:-2,tile={cols}x{rows}", "-frames:v", "1", "-vsync", "0",
                        os.path.join(a.ra, f"{ten}_{i//k+1:02d}.jpg")], check=True)
if fr: sheets(fr, "kiem_chu", 5, 3, 480)
sheets(list(range(0, int(dur * 30), 120)), "kiem_nhip", 6, 5, 320)
print("Tấm kiểm tra:", ", ".join(sorted(os.listdir(a.ra))))
if loi:
    print("LỖI:", *loi, sep="\n  - "); sys.exit(1)
print("Định dạng, tiếng, độ dài: đạt.")
