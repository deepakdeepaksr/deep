"""Plan the J26 reroute to (134.0, 153.5).

Each net gets a fresh clearance grid for its own netclass, with every already-routed
track of the other nets added as an explicit obstacle.
"""
import json
import os
import sys

from shapely.geometry import LineString, Point, box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402
import route  # noqa: E402

NEW = {1: ("3V3_C", (134.0, 153.5)), 2: ("GND", (136.5, 153.5)),
       3: ("/I2C1_SCL", (139.0, 153.5)), 4: ("/I2C1_SDA", (141.5, 153.5))}
PADW, PADH = 1.70, 1.95


def other_pads(net):
    out = []
    for num, (n, (x, y)) in NEW.items():
        if n == net:
            continue
        out.append({"net": n, "layers": {"F.Cu", "B.Cu"}, "kind": "pad",
                    "id": "J26new.%d" % num, "label": "J26.%d %s" % (num, n),
                    "poly": box(x - PADW / 2, y - PADH / 2, x + PADW / 2, y + PADH / 2),
                    "hole": 0.475})
    return out


def add_obstacle(g, net, halfwidth, other_net, layer, p0, p1, width):
    need = halfwidth + clear.clearance_for(net, other_net)
    poly = LineString([p0, p1]).buffer(width / 2.0 + need, cap_style=1)
    for ix, iy in route.cells(poly):
        g.blocked[layer][ix, iy] = True


def add_via_obstacle(g, net, other_net, x, y, dia=0.6):
    need = 0.3 + clear.clearance_for(net, other_net)
    for ix, iy in route.cells(Point(x, y).buffer(dia / 2.0 + need)):
        g.via_blocked[ix, iy] = True
        for l in route.LAYERS:
            g.blocked[l][ix, iy] = True


def dp(points, tol=0.12):
    if len(points) < 3:
        return points
    ls = LineString(points).simplify(tol, preserve_topology=False)
    return [(round(x / 0.05) * 0.05, round(y / 0.05) * 0.05) for (x, y) in ls.coords]


JOBS = [
    ("3V3_C", 0.30, (134.0, 153.5), (143.55, 159.0)),
    ("/I2C1_SCL", 0.25, (139.0, 153.5), (162.73, 163.5)),
    ("/I2C1_SDA", 0.25, (141.5, 153.5), (164.75, 165.0)),
]

done = []
result = {}
for (net, hw, start, goal) in JOBS:
    g = route.build(net, hw, other_pads(net))
    for (onet, ohw, layer, p0, p1) in done:
        add_obstacle(g, net, hw, onet, layer, p0, p1, ohw)
    path = route.route(g, start, goal, via_cost=6.0)
    if path is None:
        print("%-10s NO PATH" % net)
        continue
    # split by layer, simplify each run
    segs = []
    i = 0
    while i < len(path) - 1:
        layer = path[i][0]
        j = i
        while j + 1 < len(path) and path[j + 1][0] == layer:
            j += 1
        pts = [path[k][1] for k in range(i, j + 1)]
        sp = dp(pts)
        for a, b in zip(sp, sp[1:]):
            if a != b:
                segs.append((layer, a, b))
        i = j + 1
    vias = []
    for k in range(len(path) - 1):
        if path[k][0] != path[k + 1][0]:
            vias.append(path[k][1])
    length = sum(((b[0] - a[0]) ** 2 + (b[1] - a[1]) ** 2) ** 0.5 for (_, a, b) in segs)
    print("%-10s %d segments, %d vias, %.2f mm" % (net, len(segs), len(vias), length))
    for (layer, a, b) in segs:
        print("   %-5s (%7.2f,%7.2f) -> (%7.2f,%7.2f)" % (layer, a[0], a[1], b[0], b[1]))
    for v in vias:
        print("   VIA at (%.2f, %.2f)" % v)
    result[net] = {"width": hw, "segs": [[l, list(a), list(b)] for (l, a, b) in segs],
                   "vias": [list(v) for v in vias]}
    for (layer, a, b) in segs:
        done.append((net, hw, layer, a, b))

json.dump(result, open(os.path.join(HERE, "route_plan.json"), "w"), indent=1)
print("saved route_plan.json")
