"""Check that each silk label is present in the plotted F.Silkscreen Gerber.

Gerber coordinates are absolute mm with Y up; KiCad plots at the board origin, so
y_gerber = -y_board.
"""
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
GTO = os.path.join(ROOT, "revC", "silk_check", "MoriShield_Carrier-F_Silkscreen.gto")

LABELS = [("SOIL", 150.38, 202.6), ("FSR", 163.94, 202.6), ("SGP41", 176.0, 202.6),
          ("SHT45", 192.0, 202.6), ("SPS30", 236.0, 202.6), ("BME688", 250.0, 202.6),
          ("BUZZ", 139.31, 202.6), ("REED", 135.5, 123.5), ("WIND", 134.0, 158.8),
          ("LED", 128.6, 147.0), ("RTC", 157.65, 164.4), ("IMU", 212.11, 169.3),
          ("M0", 261.6, 162.38), ("M1", 261.6, 164.92), ("TXD", 261.6, 167.46),
          ("RXD", 261.6, 170.0), ("AUX", 261.6, 172.54), ("5V", 261.6, 175.08),
          ("GND", 261.6, 177.62), ("1", 260.9, 160.6)]

text = open(GTO, encoding="utf-8", errors="ignore").read()
print("format:", re.search(r"%FSLAX\d\dY\d\d\*%", text).group(0) if re.search(r"%FSLAX\d\dY\d\d\*%", text) else "?")
xs, ys = [], []
cur = None
for m in re.finditer(r"(?:X(-?\d+))?(?:Y(-?\d+))?D0?([123])\*", text):
    x, y, d = m.group(1), m.group(2), m.group(3)
    if x is not None:
        cur = [int(x) / 1e6, cur[1] if cur else 0.0]
    if y is not None:
        cur = [cur[0] if cur else 0.0, int(y) / 1e6]
    if cur and d in ("1", "2"):
        xs.append(cur[0])
        ys.append(cur[1])
print("points %d  x %.2f..%.2f  y %.2f..%.2f" % (len(xs), min(xs), max(xs), min(ys), max(ys)))

# find the vertical flip: board y 87.5..205.5 maps to some range
ymin, ymax = min(ys), max(ys)
for (name, bx, by) in LABELS:
    gy = -by
    hit = sum(1 for (x, y) in zip(xs, ys) if abs(x - bx) < 3.5 and abs(y - gy) < 1.3)
    print("  %-6s board (%7.2f,%7.2f) gerber y %8.2f  strokes in box: %3d %s" %
          (name, bx, by, gy, hit, "OK" if hit else "MISSING"))
