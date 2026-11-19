#!/usr/bin/env python3
"""Tìm chỗ trống trên ảnh để đặt chữ (dùng khi lập bảng dựng).

from vung_trong import Anh
a = Anh("H001.jpg")
x, y, nen = a.cho(rong=600, cao=150, uu_tien="tren", tranh=[(x0,y0,x1,y1), ...])

- Ảnh được thu về 192×108 (1 ô = 10 px khung 1920×1080), tính độ "rối" = mật độ nét viền + độ đậm tối.
- Chọn trong các vị trí ứng viên chỗ ít rối nhất; tránh các hộp đã có chữ (tranh).
- nen = "trang" nếu vùng sáng và ít màu (chữ đen viền trắng), ngược lại "anh" (chữ trắng viền đen).
"""
import numpy as np
from PIL import Image, ImageFilter

UNG_VIEN = {
    "tren": [(480, 170), (1440, 170), (960, 150), (700, 170), (1220, 170)],
    "duoi": [(960, 930), (480, 930), (1440, 930), (700, 940), (1220, 940)],
    "giua": [(1440, 540), (480, 540), (1500, 400), (420, 400)],
}


class Anh:
    def __init__(self, duong):
        im = Image.open(duong).convert("RGB").resize((192, 108))
        g = im.convert("L")
        canh = np.asarray(g.filter(ImageFilter.FIND_EDGES), float) / 255.0
        a = np.asarray(im, float)
        sang = a.mean(2) / 255.0
        bh = (a.max(2) - a.min(2)) / 255.0
        self.roi = canh * 2.5 + (sang < 0.35) * 0.6
        self.sang, self.bh = sang, bh

    def _o(self, x, y, w, h):
        x0, x1 = int(max((x - w / 2) / 10, 0)), int(min((x + w / 2) / 10, 192))
        y0, y1 = int(max((y - h / 2) / 10, 0)), int(min((y + h / 2) / 10, 108))
        return slice(y0, max(y1, y0 + 1)), slice(x0, max(x1, x0 + 1))

    def diem(self, x, y, w, h):
        o = self._o(x, y, w, h)
        return float(self.roi[o].mean())

    def nen(self, x, y, w, h):
        o = self._o(x, y, w, h)
        return "trang" if self.sang[o].mean() > 0.8 and self.bh[o].mean() < 0.2 else "anh"

    def cho(self, rong, cao, uu_tien="tren", tranh=(), cam=None):
        thu = UNG_VIEN[uu_tien] + [p for k, v in UNG_VIEN.items() if k != uu_tien for p in v]
        tot = None
        for i, (x, y) in enumerate(thu):
            x = int(min(max(x, 60 + rong / 2), 1920 - 60 - rong / 2))
            hop = (x - rong / 2, y - cao / 2, x + rong / 2, y + cao / 2)
            if any(not (hop[2] + 90 < t[0] or hop[0] - 90 > t[2] or hop[3] + 30 < t[1] or hop[1] - 30 > t[3]) for t in tranh):
                continue
            d = self.diem(x, y, rong, cao) + i * 0.012          # hơi ưu tiên vị trí đứng trước
            if cam and abs(x - cam[0]) < rong / 2 + 250 and abs(y - cam[1]) < cao / 2 + 200:
                d += 1.0                                         # tránh điểm phóng của hình "dam"
            if tot is None or d < tot[0]:
                tot = (d, x, y, hop)
        if tot is None:
            return 960, 150, "anh", (0, 0, 0, 0)
        _, x, y, hop = tot
        return x, y, self.nen(x, y, rong, cao), hop
