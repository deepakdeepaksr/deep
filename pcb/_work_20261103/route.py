"""Grid A* router for the J26 reroute.

Routes one net at a time on F.Cu/B.Cu inside a rectangle, against every other-net
copper item on the same layer, then hands back a simplified segment list.
"""
import heapq
import math
import os
import sys

import numpy as np
from shapely.geometry import Point, box

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import clear  # noqa: E402

STEP = 0.1
X0, Y0, X1, Y1 = 128.0, 145.0, 236.0, 205.0
NX = int(round((X1 - X0) / STEP)) + 1
NY = int(round((Y1 - Y0) / STEP)) + 1
LAYERS = ["F.Cu", "B.Cu"]
EDGE = (126.5, 87.5, 304.5, 205.5)


def cells(poly):
    b = poly.bounds
    ix0 = max(0, int(math.floor((b[0] - X0) / STEP)))
    ix1 = min(NX - 1, int(math.ceil((b[2] - X0) / STEP)))
    iy0 = max(0, int(math.floor((b[1] - Y0) / STEP)))
    iy1 = min(NY - 1, int(math.ceil((b[3] - Y0) / STEP)))
    for iy in range(iy0, iy1 + 1):
        y = Y0 + iy * STEP
        for ix in range(ix0, ix1 + 1):
            x = X0 + ix * STEP
            if poly.contains(Point(x, y)):
                yield ix, iy


class Grid:
    def __init__(self):
        self.blocked = {l: np.zeros((NX, NY), dtype=bool) for l in LAYERS}
        self.via_blocked = np.zeros((NX, NY), dtype=bool)


def build(net, halfwidth, extra_obstacles=(), skip_ref="J26"):
    g = Grid()
    obs = []
    for o in clear.OBST:
        if o["net"] == net:
            continue
        if skip_ref and o["id"].startswith(skip_ref + "."):
            continue
        obs.append(o)
    obs.extend(extra_obstacles)
    for o in obs:
        need = halfwidth + clear.clearance_for(net, o["net"])
        buf = o["poly"].buffer(need, resolution=16)
        for l in o["layers"]:
            if l not in g.blocked:
                continue
            for ix, iy in cells(buf):
                g.blocked[l][ix, iy] = True
        if o["kind"] in ("via", "pad"):
            vb = o["poly"].buffer(0.3 + clear.clearance_for(net, o["net"]), resolution=16)
        else:
            vb = o["poly"].buffer(0.3 + clear.clearance_for(net, o["net"]), resolution=16)
        for ix, iy in cells(vb):
            g.via_blocked[ix, iy] = True
    # board edge: 0.5 mm from the cut plus the track halfwidth
    m = 0.5 + halfwidth
    for l in LAYERS:
        arr = g.blocked[l]
        arr[: int(math.ceil(m / STEP)) + 1, :] = True
        arr[-int(math.ceil(m / STEP)) - 1:, :] = True
        arr[:, : int(math.ceil(m / STEP)) + 1] = True
        arr[:, -int(math.ceil(m / STEP)) - 1:] = True
    return g


def idx(x, y):
    return int(round((x - X0) / STEP)), int(round((y - Y0) / STEP))


def pt(ix, iy):
    return (round(X0 + ix * STEP, 2), round(Y0 + iy * STEP, 2))


def route(g, start, goal, via_cost=8.0):
    sx, sy = idx(*start)
    gx, gy = idx(*goal)
    for (ix, iy) in ((sx, sy), (gx, gy)):
        for l in LAYERS:
            g.blocked[l][ix, iy] = False
    dist = {(0, sx, sy): 0.0}
    prev = {}
    pq = [(0.0, 0.0, 0, sx, sy)]
    goal_state = None
    while pq:
        f, d, l, ix, iy = heapq.heappop(pq)
        if d > dist.get((l, ix, iy), 1e18):
            continue
        if (ix, iy) == (gx, gy):
            goal_state = (l, ix, iy)
            break
        arr = g.blocked[LAYERS[l]]
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (1, -1), (-1, 1), (-1, -1)):
            jx, jy = ix + dx, iy + dy
            if not (0 <= jx < NX and 0 <= jy < NY) or arr[jx, jy]:
                continue
            if dx and dy and (arr[ix + dx, iy] or arr[ix, iy + dy]):
                continue
            nd = d + STEP * (1.4142 if dx and dy else 1.0)
            st = (l, jx, jy)
            if nd < dist.get(st, 1e18):
                dist[st] = nd
                prev[st] = (l, ix, iy)
                heapq.heappush(pq, (nd + math.hypot(jx - gx, jy - gy) * STEP, nd, l, jx, jy))
        other = 1 - l
        if not g.via_blocked[ix, iy]:
            st = (other, ix, iy)
            nd = d + via_cost
            if nd < dist.get(st, 1e18):
                dist[st] = nd
                prev[st] = (l, ix, iy)
                heapq.heappush(pq, (nd + math.hypot(ix - gx, iy - gy) * STEP, nd, other, ix, iy))
    if goal_state is None:
        return None
    path = []
    s = goal_state
    while s in prev:
        path.append(s)
        s = prev[s]
    path.append(s)
    path.reverse()
    return [(LAYERS[l], pt(ix, iy)) for (l, ix, iy) in path]


def simplify(path):
    """One segment per straight same-layer run; drop collinear midpoints."""
    segs = []
    i = 0
    n = len(path)
    while i < n - 1:
        layer, p0 = path[i]
        j = i
        # longest run on this layer with a constant direction
        while j + 1 < n and path[j + 1][0] == layer:
            j += 1
        # split the run at direction changes
        k = i
        while k < j:
            m = k + 1
            d0 = (path[m][1][0] - path[k][1][0], path[m][1][1] - path[k][1][1])
            while m + 1 <= j:
                d1 = (path[m + 1][1][0] - path[m][1][0], path[m + 1][1][1] - path[m][1][1])
                if abs(d0[0] * d1[1] - d0[1] * d1[0]) > 1e-9 or (d0[0] * d1[0] + d0[1] * d1[1]) < 0:
                    break
                m += 1
            segs.append((layer, path[k][1], path[m][1]))
            k = m
        i = j + 1
    return segs


def add_route_to_grid(g, net, halfwidth, segs, vias):
    for (layer, p0, p1) in segs:
        from shapely.geometry import LineString
        poly = LineString([p0, p1]).buffer(halfwidth + 0.05, cap_style=1)
        for ix, iy in cells(poly):
            g.blocked[layer][ix, iy] = True
    for v in vias:
        poly = Point(v).buffer(0.35)
        for ix, iy in cells(poly):
            g.via_blocked[ix, iy] = True
            for l in LAYERS:
                g.blocked[l][ix, iy] = True
