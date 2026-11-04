"""Compare the routed length and via count of the two viable J26 bands."""
import json
import os
import sys

from shapely.geometry import LineString, Point, box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402
import route  # noqa: E402

PADW, PADH = 1.70, 1.95


def run(origin, jobs, label):
    pads = {i: (origin[0] + 2.5 * (i - 1), origin[1]) for i in (1, 2, 3, 4)}
    nets = {1: "3V3_C", 2: "GND", 3: "/I2C1_SCL", 4: "/I2C1_SDA"}

    def other_pads(net):
        out = []
        for i, (x, y) in pads.items():
            if nets[i] == net:
                continue
            out.append({"net": nets[i], "layers": {"F.Cu", "B.Cu"}, "kind": "pad",
                        "id": "NEW.%d" % i, "label": "J26.%d" % i,
                        "poly": box(x - PADW / 2, y - PADH / 2, x + PADW / 2, y + PADH / 2),
                        "hole": 0.475})
        return out

    done = []
    total = 0.0
    vias = 0
    print("=== %s  J26 at (%.2f,%.2f)" % (label, origin[0], origin[1]))
    for (net, hw, start_pad, goal) in jobs:
        start = pads[start_pad]
        g = route.build(net, hw, other_pads(net))
        for (onet, ohw, layer, p0, p1) in done:
            need = hw + clear.clearance_for(net, onet)
            for ix, iy in route.cells(LineString([p0, p1]).buffer(ohw / 2 + need, cap_style=1)):
                g.blocked[layer][ix, iy] = True
        path = route.route(g, start, goal, via_cost=20.0)
        if path is None:
            print("   %-10s NO PATH" % net)
            continue
        segs = []
        i = 0
        while i < len(path) - 1:
            layer = path[i][0]
            j = i
            while j + 1 < len(path) and path[j + 1][0] == layer:
                j += 1
            pts = [path[k][1] for k in range(i, j + 1)]
            sp = [(round(x / 0.05) * 0.05, round(y / 0.05) * 0.05)
                  for (x, y) in LineString(pts).simplify(0.12, False).coords]
            for a, b in zip(sp, sp[1:]):
                if a != b:
                    segs.append((layer, a, b))
            i = j + 1
        v = sum(1 for k in range(len(path) - 1) if path[k][0] != path[k + 1][0])
        ln = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for (_, a, b) in segs)
        total += ln
        vias += v
        print("   %-10s %5.1f mm, %d vias" % (net, ln, v))
        for (layer, a, b) in segs:
            print("       %-5s (%7.2f,%7.2f) -> (%7.2f,%7.2f)" % (layer, a[0], a[1], b[0], b[1]))
        for (layer, a, b) in segs:
            done.append((net, hw, layer, a, b))
    print("   TOTAL routed %.1f mm, %d vias" % (total, vias))


LEFT = [("3V3_C", 0.30, 1, (143.55, 159.0)),
        ("/I2C1_SCL", 0.25, 3, (162.73, 163.5)),
        ("/I2C1_SDA", 0.25, 4, (164.75, 165.0))]
BOTTOM = [("3V3_C", 0.30, 1, (209.00, 175.0)),
          ("/I2C1_SCL", 0.25, 3, (215.50, 167.75)),
          ("/I2C1_SDA", 0.25, 4, (222.27, 166.0))]

run((134.0, 153.5), LEFT, "left edge")
run((223.0, 198.5), BOTTOM, "bottom second row")
