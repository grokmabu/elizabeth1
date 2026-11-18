#!/usr/bin/env python3
"""Dựng video từ bang_dung.json: Remotion xuất hình -> FFmpeg trộn giọng + SFX + nhạc nền tự hạ.

python3 dung.py --bang bang_dung.json --giong giong_da_sua.mp3 --sfx-dir sfx --out video.mp4
  [--remotion ../remotion] [--chi-tron]   (--chi-tron: bỏ qua bước dựng hình, dùng lại hinh.mp4 cũ)

Nhạc nền khai báo trong bang["nhac"]: [{"file": "...mp3", "tu": 0, "den": 120.5, "db": -12}]
  - mỗi bài được chuẩn hoá về -16 LUFS rồi mới áp "db"; lặp lại nếu ngắn hơn đoạn, mờ vào/ra 1,5s, tự hạ thêm khi có giọng đọc.
Tiến độ dựng ghi vào <out>.log (video dài chạy nền, xem file log để biết đã tới đâu).
"""
import argparse, json, os, shutil, subprocess, sys

here = os.path.dirname(os.path.abspath(__file__))
p = argparse.ArgumentParser()
p.add_argument("--bang", required=True)
p.add_argument("--giong", required=True)
p.add_argument("--sfx-dir", default="sfx")
p.add_argument("--out", default="video.mp4")
p.add_argument("--remotion", default=os.path.join(here, "..", "remotion"))
p.add_argument("--chi-tron", action="store_true")
a = p.parse_args()

b = json.load(open(a.bang, encoding="utf-8"))
END = b["ket_thuc"]
out_dir = os.path.dirname(os.path.abspath(a.out))
hinh_mp4 = os.path.join(out_dir, "hinh_" + os.path.basename(a.out))
log = open(a.out + ".log", "a")

# ---------- 1. Dựng hình bằng Remotion ----------
if not a.chi_tron:
    rm = os.path.abspath(a.remotion)
    pub = os.path.join(rm, "public", "_anh"); shutil.rmtree(pub, ignore_errors=True); os.makedirs(pub)
    props = json.loads(json.dumps(b))
    for h in props["hinh"]:
        dst = f"{h['id']}{os.path.splitext(h['anh'])[1]}"
        shutil.copy(h["anh"], os.path.join(pub, dst)); h["anh"] = "_anh/" + dst
    pf = os.path.join(rm, "props_dung.json"); json.dump({"bang": props}, open(pf, "w"), ensure_ascii=False)
    cmd = ["npx", "remotion", "render", "src/index.ts", "Video", hinh_mp4, f"--props={pf}",
           f"--concurrency={os.cpu_count() or 2}", "--log=info"]
    for chrome in ("/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser"):
        if os.path.exists(chrome):
            cmd.append(f"--browser-executable={chrome}"); break
    print("Đang dựng hình:", " ".join(cmd), file=log, flush=True)
    r = subprocess.run(cmd, cwd=rm, stdout=log, stderr=log)
    if r.returncode:
        sys.exit(f"Remotion lỗi, xem {a.out}.log")

# ---------- 2. Trộn âm ----------
cmd = ["ffmpeg", "-y", "-loglevel", "error", "-i", hinh_mp4, "-i", a.giong]
fc = [f"[1:a]atrim=0:{END},afade=t=out:st={max(END-0.3,0)}:d=0.3,asplit=2[g][gk]"]
mix = ["[g]"]; n = 2
for i, s in enumerate(b["sfx"]):
    cmd += ["-i", os.path.join(a.sfx_dir, s["am"] + ".wav")]
    d = max(int(s["t"] * 1000), 0)
    fc.append(f"[{n}:a]volume={s['db']}dB,adelay={d}|{d}[s{i}]"); mix.append(f"[s{i}]"); n += 1
nhac = b.get("nhac") or []
if nhac:
    parts = []
    for i, m in enumerate(nhac):
        dai = m["den"] - m["tu"]; d = int(m["tu"] * 1000)
        cmd += ["-stream_loop", "-1", "-i", m["file"]]
        fc.append(f"[{n}:a]atrim=0:{dai},loudnorm=I=-16:TP=-1.5,afade=t=in:d=1.5,afade=t=out:st={max(dai-1.5,0)}:d=1.5,"
                  f"volume={m.get('db', -12)}dB,aresample=44100,aformat=channel_layouts=stereo,adelay={d}|{d}[m{i}]")
        parts.append(f"[m{i}]"); n += 1
    fc.append("".join(parts) + f"amix=inputs={len(parts)}:normalize=0[mm]")
    fc.append("[mm][gk]sidechaincompress=threshold=0.03:ratio=6:attack=20:release=400[md]")
    mix.append("[md]")
else:
    fc.append("[gk]anullsink")
fc.append("".join(mix) + f"amix=inputs={len(mix)}:normalize=0:duration=first,alimiter=limit=0.95[a]")
cmd += ["-filter_complex", ";".join(fc), "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "veryfast",
        "-crf", "20", "-pix_fmt", "yuv420p", "-profile:v", "high", "-c:a", "aac", "-b:a", "192k",
        "-movflags", "+faststart", "-t", str(END), a.out]
subprocess.run(cmd, check=True)
print(f"Xong: {a.out}")
