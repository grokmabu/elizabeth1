#!/usr/bin/env python3
"""Lấy mốc thật của từng câu H### (và từng chữ) từ file giọng — chạy offline, căn chữ với tiếng.

Dùng:
  python3 canh_moc.py --prompt "lo*.md" --audio giong_da_sua.mp3 --out moc.json [--chunk 25]

- --prompt nhận một hoặc nhiều file (cho phép mẫu *), mỗi file có các khối:
      ### H221
      [8:33] Because outlets are new.
  Câu được gom theo số H tăng dần, trùng số thì giữ bản xuất hiện đầu.
- Video dài được căn theo từng đoạn --chunk câu, cửa sổ âm thanh tự nới khi căn hụt.
"""
import argparse, glob, json, os, re, subprocess, sys
import pocketsphinx
from pocketsphinx import Decoder

SR = 16000
p = argparse.ArgumentParser()
p.add_argument("--prompt", nargs="+", required=True)
p.add_argument("--audio", required=True)
p.add_argument("--out", default="moc.json")
p.add_argument("--chunk", type=int, default=25)
a = p.parse_args()

files = sorted({f for pat in a.prompt for f in glob.glob(pat)})
if not files:
    sys.exit("Không tìm thấy file prompt nào.")
beats, seen = [], set()
for f in files:
    txt = open(f, encoding="utf-8").read()
    for h, line in re.findall(r"^###\s+(H\d{3,4})\b[^\n]*\n+\s*\[≈?\d+:\d{2}\]\s*(.*)$", txt, re.M):
        if h not in seen:
            seen.add(h); beats.append((h, line.strip()))
beats.sort(key=lambda b: int(b[0][1:]))

mdir = os.path.join(os.path.dirname(pocketsphinx.__file__), "model", "en-us")
DICT = set(l.split()[0] for l in open(os.path.join(mdir, "cmudict-en-us.dict"), encoding="utf-8", errors="ignore"))
NUM = {"0": "zero", "1": "one", "2": "two", "3": "three", "4": "four", "5": "five", "6": "six", "7": "seven", "8": "eight", "9": "nine"}

ONES = "zero one two three four five six seven eight nine ten eleven twelve thirteen fourteen fifteen sixteen seventeen eighteen nineteen".split()
TENS = "_ _ twenty thirty forty fifty sixty seventy eighty ninety".split()

def so_chu(n):
    """Đọc số như người đọc tiếng Anh: 300 -> three hundred, 220000 -> two hundred twenty thousand."""
    if n < 20: return [ONES[n]]
    if n < 100: return [TENS[n // 10]] + ([ONES[n % 10]] if n % 10 else [])
    if n < 1000: return [ONES[n // 100], "hundred"] + (so_chu(n % 100) if n % 100 else [])
    for gt, ten in ((10**9, "billion"), (10**6, "million"), (1000, "thousand")):
        if n >= gt:
            return so_chu(n // gt) + [ten] + (so_chu(n % gt) if n % gt else [])

def doc_so(w):
    n = int(w)
    if len(w) == 4 and 1100 <= n <= 2099 and n % 1000 >= 10 and not (2000 <= n <= 2009):   # năm: 1962 -> nineteen sixty two
        hi, lo = divmod(n, 100)
        return so_chu(hi) + (["hundred"] if lo == 0 else (["oh", ONES[lo]] if lo < 10 else so_chu(lo)))
    return so_chu(n)

def to_words(line):
    out = []
    line = re.sub(r"(?<=\d),(?=\d{3})", "", line).replace("&", " and ")
    for w in re.findall(r"[A-Za-z0-9']+", line):
        lw = w.lower()
        if lw in DICT:
            out.append(lw)
        elif lw.endswith("'s") and lw[:-2] in DICT:
            out.append(lw[:-2])
        elif w.isupper() and len(w) <= 6:          # viết tắt: USDA -> u s d a
            out += [c.lower() for c in w if c.lower() in DICT]
        elif w.isdigit():                          # số: đọc như người (năm / số đếm)
            out += [x for x in doc_so(w) if x in DICT]
        # từ lạ khác: bỏ qua, chỉ làm lệch nhẹ mốc của chữ bên cạnh
    return out

bw = [to_words(l) for _, l in beats]
TONG = sum(len(w) for w in bw)
pcm = subprocess.run(["ffmpeg", "-loglevel", "error", "-i", a.audio, "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                     capture_output=True, check=True).stdout
dur = len(pcm) / 2 / SR

def align(t0, t1, words):
    seg = pcm[int(t0 * SR) * 2:int(t1 * SR) * 2]
    d = Decoder(samprate=SR, bestpath=False)
    d.set_align_text(" ".join(words))
    d.start_utt(); d.process_raw(seg, full_utt=True); d.end_utt()
    if d.hyp() is None or d.seg() is None:   # căn hụt: pocketsphinx trả None thay vì danh sách
        return None
    out = [(re.sub(r"\(\d+\)$", "", s.word), t0 + s.start_frame / 100, t0 + (s.end_frame + 1) / 100)
           for s in d.seg() if s.word not in ("<s>", "</s>", "<sil>", "[NOISE]")]
    return out if len(out) == len(words) else None

res, i, cur = [], 0, 0.0
while i < len(beats):
    j = min(i + a.chunk, len(beats))
    ctx = i - 1 if i > 0 else None          # câu trước làm "mồi" để chữ đầu đoạn không nuốt khoảng lặng
    ctx_n = len(bw[ctx]) if ctx is not None else 0
    words = (bw[ctx] if ctx is not None else []) + [w for ws in bw[i:j] for w in ws]
    # cửa sổ theo tốc độ đọc thật của cả file (+15% và 3s dư); cửa sổ quá rộng làm mốc bị kéo giãn và trôi dần
    win = len(words) / (TONG / dur) * 1.15 + 3
    segs = None
    for _ in range(4):
        segs = align(cur, min(cur + win, dur), words)
        if segs or cur + win >= dur:
            break
        win *= 1.5
    if not segs:
        json.dump(res, open(a.out + ".do_dang.json", "w"), ensure_ascii=False, indent=1)
        sys.exit(f"Căn hụt ở đoạn {beats[i][0]}–{beats[j-1][0]}: kiểm tra file giọng có đọc đúng các câu này không.")
    segs = segs[ctx_n:]
    keep_to = j if j == len(beats) else max(i + 1, j - 3)   # bỏ 3 câu cuối, căn lại ở đoạn sau cho chắc
    k = 0
    for n in range(i, keep_to):
        ws = segs[k:k + len(bw[n])]; k += len(bw[n])
        if ws:
            res.append({"id": beats[n][0], "start": round(ws[0][1], 2), "end": round(ws[-1][2], 2), "line": beats[n][1],
                         "words": [[w, round(s, 2), round(e, 2)] for w, s, e in ws]})
        else:
            prev = res[-1]["end"] if res else 0
            res.append({"id": beats[n][0], "start": prev, "end": prev, "line": beats[n][1], "words": []})
    if keep_to < len(beats):   # đoạn sau bắt đầu ở câu mồi (câu keep_to-1)
        cur = max(res[-1]["start"] - 0.3, 0)
    i = keep_to

json.dump(res, open(a.out, "w"), ensure_ascii=False, indent=1)
print(f"{len(res)} câu, {len(files)} file prompt, giọng dài {dur:.1f}s -> {a.out}")
for r in res[:3] + [{"id": "...", "start": 0, "end": 0, "line": ""}] + res[-3:] if len(res) > 6 else res:
    print(f"  {r['id']:>5} {r['start']:7.2f} – {r['end']:7.2f}  {r['line'][:60]}")
