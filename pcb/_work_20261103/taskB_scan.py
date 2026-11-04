"""TASK B: enumerate legal J5 positions outside the modem outline."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

# J5: 2-pin 5.0 mm screw terminal, pads 2.8 sq / 1.3 drill, courtyard 8.90 x 11.59
J5_PADS = [(0.0, 0.0, 2.8, 2.8, 1.3, "1", "+5V"),
           (0.0, 5.0, 2.8, 2.8, 1.3, "2", "GND")]
J5_COURT = (-4.355, -3.545, 4.545, 8.045)

MODEM = clear.OUTLINES["MODEM"]


def j5(origin, rot=0.0):
    s = clear.score(origin, rot, J5_PADS, J5_COURT, skip_ref="J5")
    # lead length proxy: distance from the courtyard to the modem outline
    c = s["court"]
    dx = max(MODEM[0] - c[2], c[0] - MODEM[2], 0.0)
    dy = max(MODEM[1] - c[3], c[1] - MODEM[3], 0.0)
    s["lead"] = (dx * dx + dy * dy) ** 0.5
    s["ok"] = s["legal"] and s["lead"] > 0.0
    return s


if __name__ == "__main__":
    rows = []
    for rot in (0.0, 90.0):
        y = 90.0
        while y <= 200.0:
            x = 128.0
            while x <= 300.0:
                s = j5((round(x, 1), round(y, 1)), rot)
                if s["ok"]:
                    rows.append(s)
                x += 1.0
            y += 1.0
    print("legal candidates outside the modem: %d" % len(rows))
    rows.sort(key=lambda s: (s["lead"], -s["margin"]))
    print("%-8s %-8s %-5s %-8s %-8s %-8s %-8s %s" %
          ("x", "y", "rot", "lead", "margin", "hole", "edge", "near"))
    for s in rows[:30]:
        print("%-8.1f %-8.1f %-5.0f %-8.2f %-8.3f %-8.2f %-8.2f %s %s" %
              (s["origin"][0], s["origin"][1], s["rot"], s["lead"], s["margin"],
               s["hole_margin"], s["edge"], ",".join(s["fp_near"]) or "-",
               (s["item"] or "-")[:44]))
