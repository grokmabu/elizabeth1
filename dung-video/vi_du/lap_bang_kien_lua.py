#!/usr/bin/env python3
"""Điền bảng dựng kien_lua_bi_dap: chuyển cảnh, chữ, SFX, điểm nhấn giọng."""
import json, sys
sys.path.insert(0, "/home/claude/elizabeth1/dung-video/scripts")
from vung_trong import Anh

moc = {m["id"]: m for m in json.load(open("moc.json"))}
b = json.load(open("bang_dung.json"))
H = {h["id"]: h for h in b["hinh"]}

# ---- kịch bản dựng: n: dict(v=vào, d=(x,y) phóng, c=căng, chu=[...], s=[...], nh=[...]) ----
# chu: (kieu, text, moc_chu, hieu, {sub, mau, uu})   s: (am, moc_chu | "<" = sớm trước khi đổi hình, db)
# nh: (kieu, moc_chu, {manh, x, y, w, h})
S = {
5: dict(d=(34, 80), chu=[("chu", "SLAP!", "slap", "dap", {"mau": "do"})], s=[("bonk", "slap", -9)], nh=[("dap", "slap", {})]),
6: dict(chu=[("chu", "Problem solved.", "problem", "go", {})], s=[("ding", "solved", -13)]),
8: dict(c=1, chu=[("so", "20 sec", "twenty", "pop", {"sub": "LATER"})], s=[("ting", "twenty", -11)]),
9: dict(c=1, d=(62, 62), chu=[("so", "11", "eleven", "dap", {"sub": "BURNING SPOTS", "mau": "do"})], s=[("dap", "eleven", -9)], nh=[("dap", "eleven", {})]),
10: dict(c=1, chu=[("chu", "Backup?", "backup", "pop", {})], s=[("huh", "backup", -12)]),
12: dict(chu=[("chu", "...or YOU?", "yourself", "dap", {})], s=[("boom", "yourself", -11)]),
13: dict(v="trai", s=[("swoosh_tram", "<", -12)]),
14: dict(chu=[("chu", "Can't see. Can't smell.", "nothing", "mo", {})], s=[("bung_tay", "nothing", -12)]),
17: dict(chu=[("nhan", "Alarm gland", "gland", "pop", {"uu": "duoi"})], s=[("ting", "gland", -11)]),
18: dict(chu=[("so", "2010", "twenty", "pop", {})], s=[("ting", "twenty", -11)]),
19: dict(chu=[("nhan", "USDA lab", "department", "truot", {"uu": "duoi"})], s=[("ting", "department", -11)]),
20: dict(chu=[("nhan", "Gainesville, Florida", "florida", "pop", {"uu": "duoi"})]),
21: dict(chu=[("chu", "Pyrazine", "called+", "lo", {"mau": "vang"})], s=[("bung_tay", "called+", -12)]),
22: dict(chu=[("so", "300", "three", "pop", {"sub": "PICOGRAMS PER ANT"})], s=[("ting", "three", -11)]),
23: dict(chu=[("so", "60 mcg", "sixty", "pop", {"sub": "ONE GRAIN OF SALT"})], s=[("ting", "sixty", -11)]),
24: dict(chu=[("so", "1/200,000", "two", "dap", {"sub": "OF A GRAIN OF SALT", "mau": "vang"})], s=[("dap", "two", -11)]),
26: dict(chu=[("so", "1962", "nineteen", "pop", {})], s=[("ting", "nineteen", -11)]),
27: dict(chu=[("so", "40+ years", "forty", "pop", {"sub": "TO NAME IT"})], s=[("ting", "forty", -11)]),
29: dict(v="quet", s=[("swoosh", "<", -14)]),
30: dict(chu=[("chu", "barely any", "barely", "go", {})], s=[("bung_tay", "barely", -12)]),
33: dict(chu=[("chu", "Missing pieces?", "other", "mo", {})], s=[("huh", "other", -13)]),
35: dict(d=(52, 57), s=[("rac", "cracked", -11)]),
36: dict(v="phai", s=[("swoosh_tram", "<", -12)]),
38: dict(chu=[("chu", "ABSOLUTELY", "absolutely", "pop", {"mau": "vang"})], s=[("ding", "absolutely", -13)]),
39: dict(chu=[("so", "1962", "nineteen", "pop", {})], s=[("ting", "nineteen", -11)]),
40: dict(chu=[("nhan", "E. O. Wilson", "wilson", "truot", {"uu": "duoi"})], s=[("ting", "wilson", -11)]),
41: dict(d=(50, 55), s=[("vut", "running", -13)]),
42: dict(chu=[("chu", "FRENZY", "frenzy", "pop", {"mau": "vang"})], s=[("bung_tay", "frenzy", -12)]),
43: dict(v="lat", chu=[("chu", "But wait.", "but", "go", {})], s=[("xuoc_dia", "wait", -12)]),
44: dict(chu=[("nhan", "Lab dish", "lab", "pop", {"uu": "duoi"})], s=[("ting", "lab", -12)]),
45: dict(chu=[("chu", "Whole colony?", "colony", "mo", {})], s=[("huh", "colony", -12)]),
46: dict(chu=[("chu", "NOBODY measured", "nobody", "dap", {})], s=[("dap", "nobody", -9)], nh=[("dap", "nobody", {})]),
48: dict(chu=[("chu", "Close range only", "close", "lo", {})]),
49: dict(chu=[("chu", "NO.", "no", "pop", {})], s=[("bung_tay", "no", -12)]),
52: dict(v="len", s=[("swoosh_tram", "<", -12)]),
53: dict(d=(55, 50)),
55: dict(chu=[("chu", "On their trail", "trail", "go", {})], s=[("bung_tay", "trail", -12)]),
56: dict(chu=[("chu", "...or ON their home", "home", "go", {})]),
57: dict(chu=[("chu", "Changes EVERYTHING", "everything", "dap", {})], s=[("boom", "everything", -11)]),
59: dict(v="zoom", chu=[("chu", "How many?", "many", "pop", {})], s=[("swoosh_tram", "<", -12), ("huh", "many", -12)]),
61: dict(d=(55, 25), s=[("ding", "roof", -13)]),
63: dict(chu=[("chu", "No hole on top", "hole", "mo", {})]),
66: dict(chu=[("chu", "A CITY", "city", "pop", {"mau": "vang"})], s=[("bung_tay", "city", -12)]),
67: dict(chu=[("nhan", "Walter Tschinkel", "walter", "truot", {"uu": "duoi"})], s=[("ting", "walter", -11)]),
68: dict(chu=[("so", "4-6 years", "four", "pop", {"sub": "OF GROWING"})], s=[("ting", "four", -11)]),
69: dict(chu=[("so", "220,000", "two", "dap", {"sub": "WORKERS", "mau": "vang"})], s=[("dap", "two", -10)]),
70: dict(chu=[("nhan", "Michigan Stadium", "michigan", "pop", {"uu": "duoi"})], s=[("ting", "michigan", -11)]),
72: dict(chu=[("so", "x2", "two", "pop", {})], s=[("ting", "two", -11)]),
73: dict(d=(30, 70), chu=[("chu", "ALL of them", "all", "dap", {})], s=[("dap", "all", -9)], nh=[("dap", "all", {})]),
76: dict(chu=[("nhan", "1 queen + a few workers", "queen", "pop", {"uu": "duoi"})], s=[("ting", "queen", -12)]),
77: dict(chu=[("chu", "Probably a BIG one", "big", "go", {})]),
80: dict(d=(60, 40), s=[("bonk", "rattling", -9)]),
81: dict(v="trai", s=[("swoosh_tram", "<", -12)]),
82: dict(chu=[("chu", "Why not instantly?", "instantly", "mo", {})], s=[("huh", "instantly", -12)]),
83: dict(chu=[("chu", "In steps", "steps", "lo", {})], s=[("bung_tay", "steps", -12)]),
84: dict(v="quet", s=[("swoosh", "<", -14)]),
85: dict(c=1, chu=[("nhan", "1  CLIMB", "climb", "pop", {})], s=[("ting", "climb", -11)]),
86: dict(c=1, chu=[("nhan", "Texas A&M", "texas", "truot", {"uu": "duoi"})], s=[("ting", "texas", -12)]),
87: dict(c=1), 88: dict(c=1, d=(60, 50), chu=[("chu", "Hundreds", "hundreds", "pop", {})], s=[("vut", "rush", -12)]),
89: dict(c=1, chu=[("chu", "including YOU", "you", "go", {})]),
90: dict(c=1, v="quet", s=[("swoosh", "<", -14)]),
91: dict(c=1, d=(45, 55), chu=[("nhan", "2  GRAB", "grabs", "pop", {})], s=[("rac", "grabs", -12), ("ting", "hold", -12)]),
92: dict(c=1, d=(60, 63), chu=[("nhan", "3  STING", "stinger", "pop", {})], s=[("dap", "only", -10), ("ting", "stinger", -11)], nh=[("dap", "only", {"manh": 0.8})]),
93: dict(c=1), 94: dict(c=1),
95: dict(c=1, d=(56, 68), chu=[("chu", "Again!", "again", "pop", {})], s=[("bonk", "again", -10)]),
96: dict(c=1), 97: dict(chu=[("chu", "Takes time", "time", "go", {})]),
98: dict(chu=[("so", "10-20 sec", "ten", "pop", {"sub": "BEFORE THE FIRST STING"})], s=[("ting", "ten", -11)]),
100: dict(chu=[("chu", "Really dead?", "dead", "mo", {})], s=[("huh", "dead", -13)]),
101: dict(v="quet", chu=[("chu", "The clever part", "clever", "lo", {})], s=[("swoosh", "<", -14), ("bung_tay", "clever", -12)]),
102: dict(chu=[("chu", "Sizing you up", "sizes", "go", {})]),
103: dict(chu=[("so", "2010", "twenty", "pop", {})], s=[("ting", "twenty", -11)]),
104: dict(chu=[("nhan", "Kevin Haight", "kevin", "truot", {"uu": "duoi"})], s=[("ting", "kevin", -11)]),
105: dict(chu=[("nhan", "Light touch", "light", "pop", {})], s=[("ting", "light", -12)]),
107: dict(chu=[("nhan", "Heavy shake", "heavy", "pop", {})], s=[("ting", "heavy", -12)]),
109: dict(chu=[("chu", "BIGGER workers", "bigger", "pop", {"mau": "vang"})], s=[("bung_tay", "bigger", -12)]),
110: dict(chu=[("chu", "Longer stingers", "longer", "go", {})]),
111: dict(chu=[("chu", "Not blind rage", "blind", "mo", {})]),
113: dict(d=(18, 75), chu=[("chu", "How BIG you are", "big", "go", {})], nh=[("rung", "your", {"manh": 0.7})]),
114: dict(c=1, v="phai", s=[("swoosh", "<", -14), ("cang", "first", -10)]),
115: dict(c=1, d=(40, 55), s=[("bonk", "slap", -9)]),
116: dict(c=1),
117: dict(c=1, d=(50, 55), chu=[("so", "x12", "dozen", "dap", {"sub": "LIGHTERS AT ONCE", "mau": "do", "uu": "tren"})],
         s=[("set", "lighters", -10)], nh=[("flash", "lighters", {}), ("dap", "lighters", {})]),
118: dict(v="lat", chu=[("chu", "All at once?", "exact", "mo", {})], s=[("swoosh_tram", "<", -12), ("huh", "exact", -12)]),
119: dict(chu=[("chu", "\"Sting now!\"", "sting", "pop", {})], s=[("swoosh", "sting", -15)]),
120: dict(chu=[("chu", "A chemical countdown", "chemical", "lo", {})]),
122: dict(chu=[("chu", "Probably NOT", "not", "dap", {})], s=[("xuoc_dia", "not", -12)]),
123: dict(chu=[("nhan", "NIEHS", "national", "truot", {"uu": "duoi"})], s=[("ting", "national", -11)]),
124: dict(chu=[("chu", "VIBRATION", "vibration", "pop", {"mau": "vang"})], s=[("bung_tay", "vibration", -12)]),
127: dict(chu=[("chu", "Every ant feels it", "feels", "go", {})], nh=[("rung", "every", {"manh": 0.6})]),
129: dict(chu=[("chu", "Not to plan a sting", "plan", "go", {})]),
130: dict(chu=[("nhan", "NC State", "north", "truot", {"uu": "duoi"})], s=[("ting", "north", -11)]),
133: dict(chu=[("chu", "(still debated)", "debate", "mo", {})], s=[("de_keu", "debate", -16)]),
136: dict(chu=[("chu", "The signal from YOU", "you", "go", {})], s=[("bung_tay", "you", -12)]),
139: dict(d=(30, 75), chu=[("chu", "YOU DID.", "did", "dap", {"mau": "do"})], s=[("boom", "did", -11)], nh=[("dap", "did", {})]),
140: dict(v="len", s=[("swoosh_tram", "<", -12)]),
142: dict(v="zoom", chu=[("chu", "What's in a sting?", "sting", "mo", {})], s=[("swoosh_tram", "<", -12)]),
143: dict(chu=[("chu", "WEIRD", "weird", "pop", {})], s=[("bung_tay", "weird", -12)]),
144: dict(chu=[("nhan", "Bee & wasp: proteins", "proteins", "pop", {})], s=[("ting", "proteins", -12)]),
145: dict(chu=[("so", "95%+", "ninety", "pop", {"sub": "OILY ALKALOIDS", "mau": "vang"})], s=[("ting", "ninety", -11)]),
146: dict(d=(50, 45), chu=[("chu", "Kills skin cells", "destroy", "go", {})], s=[("rac", "destroy", -11)]),
147: dict(chu=[("chu", "= the FIRE", "name", "pop", {})]),
148: dict(chu=[("so", "~1 day", "day", "pop", {})], s=[("ting", "day", -12)]),
149: dict(chu=[("chu", "Pustule", "white+", "lo", {})]),
151: dict(chu=[("chu", "NOT infected", "isn't", "pop", {})], s=[("bung_tay", "isn't", -12)]),
152: dict(chu=[("chu", "Sterile", "sterile", "go", {})]),
154: dict(chu=[("so", "3-10 days", "three", "pop", {})], s=[("ting", "three", -11)]),
155: dict(v="phai", chu=[("chu", "Don't scratch", "scratch", "pop", {"mau": "do"})], s=[("swoosh", "<", -15)]),
159: dict(chu=[("so", "5%", "five", "pop", {"sub": "PROTEIN"})], s=[("ting", "five", -11)]),
160: dict(chu=[("chu", "Allergy trigger", "allergic", "lo", {})]),
162: dict(chu=[("chu", "Just itching", "itching", "go", {})]),
164: dict(d=(50, 50), chu=[("chu", "SERIOUS", "serious", "pop", {"mau": "do"})], s=[("cang", "serious", -10)]),
165: dict(chu=[("chu", "Not rare", "rare", "go", {})]),
166: dict(chu=[("so", "14 million", "fourteen", "dap", {"sub": "STUNG EVERY YEAR", "mau": "vang"}),
              ("nhan", "Texas A&M", "texas", "truot", {"uu": "duoi"})],
         s=[("ting", "texas", -12), ("dap", "fourteen", -9)], nh=[("dap", "fourteen", {"manh": 0.8})]),
168: dict(chu=[("chu", "Southern rite of passage", "southern", "lo", {})], s=[("ding", "passage", -13)]),
169: dict(v="trai", chu=[("chu", "Why so many?", "full", "mo", {})], s=[("swoosh_tram", "<", -12)]),
170: dict(chu=[("chu", "Not from here", "not", "pop", {})], s=[("bung_tay", "not", -12)]),
171: dict(chu=[("nhan", "South America", "south", "pop", {"uu": "duoi"})], s=[("ting", "south", -11)]),
172: dict(chu=[("so", "1930s", "the+", "pop", {})], s=[("ting", "the+", -11)]),
173: dict(chu=[("nhan", "Mobile, Alabama", "mobile", "truot", {"uu": "duoi"})], s=[("ting", "mobile", -11)]),
175: dict(d=(50, 65), chu=[("chu", "Hidden in ballast", "ballast", "go", {})]),
176: dict(v="quet_trai", chu=[("chu", "The wild part", "wild", "lo", {})], s=[("swoosh", "<", -14)]),
177: dict(chu=[("so", "1942", "nineteen", "pop", {})], s=[("ting", "nineteen", -11)]),
178: dict(chu=[("so", "13", "thirteen", "pop", {"sub": "YEARS OLD"})], s=[("ting", "thirteen", -11)]),
180: dict(chu=[("chu", "A strange nest", "strange", "mo", {})]),
181: dict(chu=[("chu", "First US record", "first", "lo", {"mau": "vang"})], s=[("ding", "states", -13)]),
182: dict(s=[("dun_dun", "boy", -11)], nh=[("bat", "wilson", {"x": 33, "y": 55, "w": 36, "h": 84, "dai": 1.6})]),
185: dict(chu=[("so", "20 years", "twenty", "pop", {"sub": "LATER"})], s=[("ting", "twenty", -11)]),
187: dict(chu=[("chu", "Top ant expert", "experts", "go", {})]),
188: dict(chu=[("chu", "His FIRST discovery", "first", "lo", {})], s=[("ding", "ankle", -13)]),
189: dict(v="phai", s=[("swoosh", "<", -14)]),
192: dict(chu=[("so", "5x", "five", "pop", {"sub": "DENSER THAN BACK HOME"})], s=[("ting", "five", -11)]),
194: dict(chu=[("chu", "Natural enemies", "natural", "go", {})]),
196: dict(chu=[("chu", "Stowaways' grandkids", "great", "mo", {})]),
197: dict(v="lat", chu=[("chu", "Even stranger", "stranger", "mo", {})], s=[("swoosh_tram", "<", -12)]),
198: dict(chu=[("chu", "Calling more ants?", "call", "pop", {})], s=[("huh", "call", -12)]),
199: dict(chu=[("nhan", "AC repairman", "air", "pop", {"uu": "duoi"})], s=[("ting", "air", -12)]),
200: dict(chu=[("nhan", "AC units", "units", "pop", {})], s=[("ting", "units", -12)]),
201: dict(chu=[("nhan", "Electrical boxes", "electrical", "pop", {})], s=[("ting", "electrical", -12)]),
202: dict(chu=[("nhan", "Traffic lights", "traffic", "pop", {})], s=[("ting", "traffic", -12)]),
203: dict(d=(45, 55), chu=[("chu", "SHORTED OUT", "shorting", "pop", {})], s=[("nhieu_radio", "shorting", -14)]),
205: dict(d=(50, 65), chu=[("chu", "Piles of dead ants", "piles", "go", {})], nh=[("bat", "piles", {"x": 50, "y": 66, "w": 36, "h": 48})], s=[("chup_anh", "piles", -14)]),
206: dict(chu=[("so", "2002", "two", "pop", {})], s=[("ting", "two", -11)]),
207: dict(chu=[("nhan", "USDA + Texas Tech", "scientists", "truot", {"uu": "duoi"})], s=[("ting", "scientists", -11)]),
208: dict(chu=[("so", "120 V", "one", "pop", {"sub": "CURRENT"})], s=[("ting", "one", -11)]),
209: dict(chu=[("chu", "= a home outlet", "outlet", "go", {})]),
211: dict(chu=[("chu", "Venom", "venom", "pop", {})], s=[("bung_tay", "venom", -12)]),
212: dict(chu=[("chu", "+ ALARM", "alarm", "pop", {"mau": "vang"})], nh=[("rung", "other", {"manh": 0.6})]),
213: dict(c=1), 214: dict(c=1, d=(55, 55), s=[("nhieu_radio", "zapped", -12)], nh=[("flash", "zapped", {"manh": 0.7})]),
215: dict(c=1, chu=[("chu", "Calls its sisters", "sisters", "go", {})]),
216: dict(c=1, s=[("nhieu_radio", "zapped", -14)]),
217: dict(c=1, chu=[("chu", "even MORE", "more", "pop", {})]),
218: dict(c=1, chu=[("chu", "Feedback loop", "feedback", "lo", {"mau": "vang"})], s=[("cang", "body", -10)]),
219: dict(v="len", s=[("swoosh_tram", "<", -12)]),
220: dict(chu=[("chu", "Why not switch it off?", "switched", "mo", {})], s=[("huh", "switched", -12)]),
221: dict(chu=[("chu", "Outlets are NEW", "new", "pop", {})], s=[("bung_tay", "new", -12)]),
222: dict(chu=[("chu", "Built for predators", "predators", "go", {})]),
223: dict(chu=[("chu", "Other costs", "costs", "go", {})]),
224: dict(chu=[("nhan", "USDA researchers", "researchers", "truot", {"uu": "duoi"})], s=[("ting", "researchers", -11)]),
225: dict(chu=[("chu", "Parasitic flies", None, "mo", {})]),
226: dict(chu=[("chu", "Same alarm chemical", "same", "lo", {})]),
227: dict(chu=[("chu", "So why keep it?", "keep", "pop", {})], s=[("huh", "keep", -12)]),
228: dict(chu=[("so", "~200,000", "couple", "pop", {"sub": "ANTS PER COLONY"})], s=[("ting", "couple", -11)]),
229: dict(chu=[("chu", "Worth it", "worth", "pop", {})], s=[("ding", "worth", -13)]),
230: dict(chu=[("chu", "(a guess)", "guess", "mo", {})], s=[("de_keu", "guess", -16)]),
232: dict(v="zoom", s=[("swoosh_tram", "<", -12)]),
233: dict(d=(50, 50), chu=[("chu", "the WORST thing?", "worst", "dap", {})], s=[("boom", "worst", -11)]),
234: dict(chu=[("chu", "Killing isn't the problem", "killing", "go", {})]),
235: dict(chu=[("nhan", "WHEN", "when", "pop", {"uu": "tren"}), ("nhan", "WHERE", "where", "pop", {"uu": "tren"})],
         s=[("ting", "when", -11), ("ting", "where", -11)]),
236: dict(d=(52, 70), s=[("giot", "leaks", -8)]),
237: dict(s=[("vut", "running", -12)]),
238: dict(c=1), 239: dict(c=1),
240: dict(c=1, s=[("bonk", "slap", -9)]),
241: dict(c=1, d=(55, 60), chu=[("chu", "ALL AT ONCE", "all", "dap", {"mau": "do"})], s=[("dap", "fire", -8)],
         nh=[("dap", "fire", {}), ("flash", "fire", {"manh": 0.6})]),
242: dict(chu=[("chu", "The smell calls", "smell", "go", {})]),
243: dict(d=(44, 77), chu=[("chu", "YOUR SLAP", "slap", "pop", {"mau": "do"})], s=[("bonk", "slap", -10)]),
244: dict(v="trai", s=[("swoosh_tram", "<", -12)]),
245: dict(chu=[("chu", "DON'T slap", "slap", "pop", {"mau": "do"})], s=[("bung_tay", "slap", -12)]),
246: dict(chu=[("chu", "Don't hose them", "hose", "go", {})]),
247: dict(chu=[("nhan", "Texas A&M", "texas", "truot", {"uu": "duoi"})], s=[("ting", "texas", -12)]),
248: dict(chu=[("chu", "Water = tighter grip", "tighter", "go", {})]),
249: dict(chu=[("chu", "No shaking", "shaking", "pop", {})], nh=[("rung", "doesn't", {"manh": 0.8})]),
250: dict(d=(40, 80), chu=[("chu", "BRUSH fast", "brush", "pop", {"mau": "vang"})], s=[("vut", "brush", -12)]),
251: dict(chu=[("chu", "over & over", "over", "go", {})], s=[("bung_tay", "over", -13)]),
252: dict(chu=[("chu", "Step away", "step", "mo", {})]),
254: dict(chu=[("chu", "Shoes off", "take", "pop", {})], s=[("bung_tay", "take", -12)]),
255: dict(chu=[("nhan", "Trouble breathing", "trouble", "pop", {})], s=[("ting", "trouble", -11)]),
256: dict(chu=[("nhan", "Unusual swelling", "unusual", "pop", {})], s=[("ting", "unusual", -11)]),
257: dict(chu=[("nhan", "Nausea", "nausea", "pop", {})], s=[("ting", "nausea", -11)]),
258: dict(c=1, chu=[("chu", "Get help NOW", "medical", "pop", {"mau": "do"})], s=[("cang", "medical", -10)]),
259: dict(v="quet", s=[("swoosh_tram", "<", -12)]),
261: dict(chu=[("chu", "Same hand", "same", "go", {})]),
263: dict(d=(40, 30), chu=[("chu", "Just brush.", "brush", "pop", {})], s=[("ding", "brush", -12)]),
}
# ảnh đã có sẵn chữ/số này (theo dòng "The only text in the image" trong prompt) -> không thêm chữ trùng
TRUNG = {8, 10, 17, 18, 19, 20, 21, 22, 23, 24, 26, 39, 40, 44, 68, 69, 70, 72, 86, 98, 103, 119, 120, 123, 130,
         145, 152, 154, 159, 172, 177, 206, 207, 208, 247}
for n in TRUNG:
    S[n]["chu"] = []
S[166]["chu"] = [c for c in S[166]["chu"] if c[0] != "so"]
S[69].setdefault("nh", []).append(("dap", "two", {"manh": 0.7}))
S[24].setdefault("nh", []).append(("dap", "two", {"manh": 0.6}))
THEM = {
25: [("chu", "No wonder.", "wonder", "mo", {})],
28: [("chu", "smaller than salt", "smaller", "go", {})],
31: [("chu", "Trace amounts", "trace", "lo", {})],
37: [("chu", "Up close?", "close", "pop", {})],
51: [("chu", "Never know", "never", "mo", {})],
54: [("chu", "One on you...", "one", "go", {})],
64: [("chu", "Tunnels everywhere", "tunnels", "lo", {})],
79: [("chu", "Not a few bugs", "few", "go", {})],
99: [("chu", "Those 20 seconds", "twenty", "go", {})],
121: [("chu", "Sounds right...", "sounds", "mo", {})],
125: [("chu", "Ground moves = sting", "moves", "go", {})],
131: [("chu", "One stings, ALL sting", "others", "pop", {})],
138: [("chu", "Never pulled the trigger", "trigger", "lo", {})],
}
for n, cs in THEM.items():
    S.setdefault(n, {}).setdefault("chu", []).extend(cs)
XY = {14: (560, 560), 25: (1100, 1000), 28: (1250, 1000), 76: (700, 1000), 111: (960, 990), 144: (960, 1010), 180: (1440, 170), 185: (960, 1000), 187: (480, 960),
      196: (560, 990), 215: (520, 150), 218: (1400, 990), 220: (960, 1010), 222: (520, 150), 228: (1440, 170),
      230: (1500, 620), 242: (960, 990), 250: (1450, 170), 251: (960, 110)}
for n, xy in XY.items():
    S[n]["chu"] = [(k, t, w, h, dict(o, xy=xy)) for k, t, w, h, o in S[n]["chu"]]
S[235]["chu"] = [("nhan", "WHEN", "when", "pop", {"xy": (480, 990)}), ("nhan", "WHERE", "where", "pop", {"xy": (1440, 990)})]
S[14]["chu"] = []                                       # ảnh đã có biểu tượng mắt/mũi gạch chéo
S[48]["chu"] = [("nhan", "Close range only", "close", "lo", {"xy": (1550, 900)})]
S[131]["chu"] = [("chu", "ALL sting", "others", "pop", {"xy": (1450, 170)})]
S[196]["chu"] = [("chu", "Stowaway kids", "great", "mo", {"xy": (480, 990)})]
S[218]["chu"] = [("nhan", "FEEDBACK LOOP", "feedback", "lo", {"xy": (1650, 540), "mau": "vang"})]
XY.update({147: (520, 540), 185: (960, 150), 198: (520, 990), 209: (1450, 170)})
for n in (147, 185, 198, 209):
    S[n]["chu"] = [(k, t, w, h, dict(o, xy=XY[n])) for k, t, w, h, o in S[n]["chu"]]
S[192]["chu"] = []
S[129]["chu"] = []
S[136]["chu"] = [("chu", "The signal from YOU", "signal", "go", {})]

S[5]["chu"] = [("chu", "SLAP!", "slap", "dap", {"mau": "do", "xy": (1450, 200)})]
FS = {"chu": 112, "so": 150, "nhan": 62}
canh = []


def moc_chu(hid, w):
    m = moc[hid]
    if w is None:
        return round(H[hid]["bat_dau"] + 0.15, 2)
    het = w.endswith("+")                     # "chu+" = ngay sau chữ đó (chữ kế tiếp không có trong từ điển)
    w = w.rstrip("+").lower().replace("'", "")
    for ten, s, e in m["words"]:
        if ten.replace("'", "").startswith(w):
            return e + 0.05 if het else s
    canh.append(f"{hid}: không thấy chữ '{w}' → dùng đầu câu")
    return m["start"]


b["chu"], b["sfx"], b["nhan"] = [], [], []
for n, sp in S.items():
    hid = f"H{n:03d}"
    h = H[hid]
    if sp.get("v"):
        h["vao"] = sp["v"]
    if sp.get("c"):
        h["cang"] = True
    if sp.get("d"):
        h["chuyen_dong"] = {"kieu": "dam", "x": sp["d"][0], "y": sp["d"][1]}
    cam = (sp["d"][0] * 19.2, sp["d"][1] * 10.8) if sp.get("d") else None
    a = Anh(h["anh"]); da = []
    for kieu, text, w, hieu, op in sp.get("chu", []):
        t = moc_chu(hid, w)
        rong = len(text) * FS[kieu] * 0.55 + (70 if kieu == "nhan" else 30)
        if kieu == "so" and op.get("sub"):
            rong = max(rong, len(op["sub"]) * 44 * 0.62 + 40)
        cao = {"chu": 140, "so": 240 if op.get("sub") else 180, "nhan": 100}[kieu]
        uu = op.get("uu", "duoi" if kieu == "nhan" else "tren")
        x, y, nen, hop = a.cho(rong, cao, uu, da, cam)
        if op.get("xy"):
            x, y = op["xy"]; hop = (x - rong / 2, y - cao / 2, x + rong / 2, y + cao / 2)
        da.append(hop)
        c = {"h": hid, "kieu": kieu, "text": text, "t": round(t, 2), "x": x, "y": y, "nen": nen, "hieu": hieu}
        ids = [x["id"] for x in b["hinh"]]; i = ids.index(hid)
        het_h = b["hinh"][i + 1]["bat_dau"] if i + 1 < len(ids) else b["ket_thuc"]
        # (19/11 user góp ý H012) chữ KHÔNG được kéo sang hình sau; kiem_bang tự dời chữ sớm lên trong hình
        for k in ("sub", "mau"):
            if op.get(k):
                c[k] = op[k]
        b["chu"].append(c)
    for am, w, db in sp.get("s", []):
        t = h["bat_dau"] - (0.35 if am == "swoosh_tram" else 0.3) if w == "<" else moc_chu(hid, w)
        if am == "vut" and w != "<":
            t -= 0.25
        b["sfx"].append({"h": hid, "am": am, "t": round(max(t, 0), 2), "db": db})
    for kieu, w, op in sp.get("nh", []):
        nh = {"t": round(moc_chu(hid, w), 2), "kieu": kieu}
        nh.update(op)
        if kieu == "dap" and sp.get("d"):
            nh.setdefault("x", sp["d"][0]); nh.setdefault("y", sp["d"][1])
        if kieu == "bat":
            nh["anh"] = hid
        b["nhan"].append(nh)

for c in b["chu"]:                            # chữ kéo dài nhường chỗ cho chữ kế tiếp
    if "het" in c:
        for d in b["chu"]:
            if d is not c and c["t"] < d["t"] < c["het"]:
                c["het"] = round(max(d["t"] - 0.05, c["t"] + 0.6), 2)
json.dump(b, open("bang_dung.json", "w"), ensure_ascii=False, indent=1)
from collections import Counter
print(len(b["chu"]), "lớp chữ,", len(b["sfx"]), "SFX,", len(b["nhan"]), "điểm nhấn;",
      "chuyển cảnh:", Counter(h.get("vao", "mo") for h in b["hinh"]))
print("\n".join(canh) or "mọi mốc chữ đều tìm thấy")
