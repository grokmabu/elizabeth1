#!/usr/bin/env python3
"""Ghép ảnh của bảng dựng thành các tấm lưới có ghi số H### và lưới toạ độ, để Claude xem trước khi đặt chữ.

python3 xem_anh.py --bang bang_dung.json --ra xem_anh
Mỗi tấm 4x3 ảnh; trên mỗi ảnh vẽ lưới 3x3 mờ với toạ độ khung 1920x1080 (x=320/960/1600, y=180/540/900).
"""
import argparse, json, os, subprocess

p = argparse.ArgumentParser()
p.add_argument("--bang", required=True)
p.add_argument("--ra", default="xem_anh")
a = p.parse_args()
os.makedirs(a.ra, exist_ok=True)
b = json.load(open(a.bang, encoding="utf-8"))
font = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
H = b["hinh"]
for k in range(0, len(H), 12):
    grp = H[k:k + 12]; cmd = ["ffmpeg", "-y", "-loglevel", "error"]
    fc = []
    for i, h in enumerate(grp):
        cmd += ["-i", h["anh"]]
        fc.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
                  "drawgrid=w=640:h=360:t=3:c=red@0.35,"
                  f"drawtext=fontfile={font}:text='{h['id']}':x=20:y=20:fontsize=90:fontcolor=yellow:box=1:boxcolor=black@0.7,"
                  f"scale=640:360[v{i}]")
    while len(fc) < 12:
        fc.append(f"color=white:s=640x360:d=1[v{len(fc)}]")
    fc.append("".join(f"[v{i}]" for i in range(12)) + "xstack=inputs=12:layout=" +
              "|".join(f"{(i%4)*640}_{(i//4)*360}" for i in range(12)) + "[o]")
    subprocess.run(cmd + ["-filter_complex", ";".join(fc), "-map", "[o]", "-frames:v", "1",
                          os.path.join(a.ra, f"anh_{k//12+1:02d}.jpg")], check=True)
print("Tấm xem ảnh:", ", ".join(sorted(os.listdir(a.ra))))
