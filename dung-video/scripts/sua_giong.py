#!/usr/bin/env python3
"""Rút ngắn khoảng lặng dài và tăng tốc nhẹ (giữ nguyên cao độ giọng).

python3 sua_giong.py vao.mp3 ra.mp3 --pause 0.3 --speed 1.1
  --pause : khoảng lặng dài nhất được giữ lại (giây); lặng dài hơn sẽ bị cắt bớt phần giữa
  --speed : hệ số tăng tốc (1.0 = giữ nguyên)
"""
import argparse, re, subprocess

p = argparse.ArgumentParser()
p.add_argument("inp"); p.add_argument("out")
p.add_argument("--pause", type=float, default=0.3)
p.add_argument("--speed", type=float, default=1.1)
p.add_argument("--noise", default="-35dB")
p.add_argument("--min", type=float, default=0.25)
a = p.parse_args()

log = subprocess.run(["ffmpeg", "-hide_banner", "-i", a.inp, "-af",
                      f"silencedetect=noise={a.noise}:d={a.min}", "-f", "null", "-"],
                     capture_output=True, text=True).stderr
dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", a.inp], capture_output=True, text=True).stdout)
starts = [float(x) for x in re.findall(r"silence_start: ([\d.]+)", log)]
ends = [float(x) for x in re.findall(r"silence_end: ([\d.]+)", log)]

# Các đoạn giữ lại: mỗi khoảng lặng chỉ giữ 'pause' giây (chia đôi ở hai mép).
keep, cur = [], 0.0
for s, e in zip(starts, ends):
    if e - s > a.pause:
        half = a.pause / 2
        keep.append((cur, s + half))
        cur = e - half
keep.append((cur, dur))

parts = "+".join(f"between(t,{x:.3f},{y:.3f})" for x, y in keep)
af = f"aselect='{parts}',asetpts=N/SR/TB,atempo={a.speed}"
subprocess.run(["ffmpeg", "-y", "-hide_banner", "-loglevel", "error", "-i", a.inp,
                "-af", af, "-c:a", "libmp3lame", "-b:a", "192k", a.out], check=True)
new = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration",
                            "-of", "csv=p=0", a.out], capture_output=True, text=True).stdout)
print(f"{dur:.1f}s -> {new:.1f}s  (đã cắt bớt {len(keep)-1} khoảng lặng, tăng tốc x{a.speed})")
