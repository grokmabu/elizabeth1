#!/usr/bin/env python3
"""Chuẩn hoá SFX từ thư viện của user thành wav ngắn, cùng mức âm lượng.

python3 lay_sfx.py --lib "/mnt/user-data/uploads/Am_thanh" --out sfx [--map thu_vien_sfx.json] [--chi ten1,ten2]

thu_vien_sfx.json: {"ten_ngan": {"file": "đường dẫn tương đối trong thư viện", "dai": giây_tối_đa}}
Mỗi âm: cắt lặng đầu, giữ tối đa 'dai' giây, mờ cuối 0,25s, chuẩn hoá mức, 44.1kHz stereo.
"""
import argparse, json, os, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
p = argparse.ArgumentParser()
p.add_argument("--lib", required=True)
p.add_argument("--out", default="sfx")
p.add_argument("--map", default=os.path.join(here, "..", "thu_vien_sfx.json"))
p.add_argument("--chi", help="chỉ lấy các tên này (phẩy ngăn cách)")
a = p.parse_args()
m = json.load(open(a.map, encoding="utf-8"))
chi = set(a.chi.split(",")) if a.chi else None
os.makedirs(a.out, exist_ok=True)
thieu = []
for ten, v in m.items():
    if ten.startswith("_") or (chi and ten not in chi):
        continue
    src = os.path.join(a.lib, v["file"])
    if not os.path.exists(src):
        thieu.append(f"{ten}: {v['file']}"); continue
    d = float(v.get("dai", 1.2))
    af = (f"silenceremove=start_periods=1:start_threshold=-45dB,atrim=0:{d},"
          f"afade=t=out:st={max(d-0.25,0)}:d=0.25,dynaudnorm=p=0.9:m=10,aresample=44100")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src, "-af", af, "-ac", "2",
                    os.path.join(a.out, ten + ".wav")], check=True)
    print("ok", ten)
if thieu:
    print("Không thấy file:", *thieu, sep="\n  "); sys.exit(1)
