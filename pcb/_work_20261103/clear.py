"""Candidate-placement clearance engine.

Loads geom.json, builds shapely geometry for every copper item, and scores a
candidate footprint placement: copper clearance (different nets), hole-to-hole,
board-edge distance, courtyard overlaps, module-outline overlap and distance to
the nearest zone border.
"""
import json
import math
import os

from shapely.geometry import LineString, Point, box
from shapely.ops import unary_union

HERE = os.path.dirname(os.path.abspath(__file__))
G = json.load(open(os.path.join(HERE, "geom.json"), encoding="utf-8"))

LAYERS = ["F.Cu", "In1.Cu", "In2.Cu", "B.Cu"]
EDGE = (126.5, 87.5, 304.5, 205.5)

# module envelopes from User.Drawings / F.Fab (measured in outlines.py)
OUTLINES = {
    "DS3231": (144.70, 162.95, 182.80, 185.05),
    "ESP32": (180.45, 91.45, 212.55, 156.55),
    "GY521": (209.30, 175.95, 230.40, 192.05),
    "MODEM": (228.45, 90.45, 271.55, 150.55),
    "E22": (259.95, 158.57, 297.05, 180.67),
}

POWER_NETS = {"+5V", "+5V_IN", "+5V_F", "/5V_PROT", "/+5V_ESP", "/+5V_SENS", "/+5V_E22",
              "/+5V_E22_IN", "LED5V_A"}
PE_NET = "PE"


def clearance_for(net_a, net_b):
    """KiCad uses the larger of the two netclass clearances."""
    def one(n):
        if n == PE_NET:
            return 0.30
        if n in POWER_NETS:
            return 0.25
        return 0.20
    return max(one(net_a), one(net_b))


def _seg_poly(c):
    ls = LineString([(c["x0"], c["y0"]), (c["x1"], c["y1"])])
    return ls.buffer(c["width"] / 2.0, cap_style=1, join_style=1)


def build_obstacles():
    """Return list of dicts: net, layers(set), poly, kind, uuid, label, hole(radius or None)."""
    out = []
    for c in G["copper"]:
        if c["kind"] == "seg":
            out.append({
                "net": c["net"], "layers": {c["layer"]}, "poly": _seg_poly(c),
                "kind": "seg", "id": c["uuid"],
                "label": "%s %s (%.2f,%.2f)-(%.2f,%.2f) w%.2f" % (c["layer"], c["net"], c["x0"], c["y0"],
                                                                  c["x1"], c["y1"], c["width"]),
                "hole": None,
            })
        else:
            p = Point(c["x"], c["y"]).buffer(c["size"] / 2.0, resolution=24)
            out.append({
                "net": c["net"], "layers": set(LAYERS), "poly": p,
                "kind": "via", "id": c["uuid"],
                "label": "VIA %s (%.2f,%.2f) d%.2f" % (c["net"], c["x"], c["y"], c["size"]),
                "hole": c["drill"] / 2.0,
            })
    for f in G["footprints"]:
        for p in f["pads"]:
            b = p["bbox"]
            out.append({
                "net": p["net"], "layers": set(p["layers"]) & set(LAYERS) or set(LAYERS),
                "poly": box(b[0], b[1], b[2], b[3]),
                "kind": "pad", "id": f["ref"] + "." + p["num"],
                "label": "PAD %s.%s %s (%.2f,%.2f)" % (f["ref"], p["num"], p["net"], p["x"], p["y"]),
                "hole": (p["drill"] / 2.0) if p["drill"] > 0 else None,
            })
    return out


OBST = build_obstacles()
ZONES = G["zones"]

# spatial index over the obstacle polygons so a candidate only looks at its neighbours
from shapely.strtree import STRtree  # noqa: E402

_POLYS = [o["poly"] for o in OBST]
_TREE = STRtree(_POLYS)


def nearby(poly, pad=4.0):
    b = poly.bounds
    idx = _TREE.query(box(b[0] - pad, b[1] - pad, b[2] + pad, b[3] + pad))
    return [OBST[i] for i in idx]


def zones_for_layer(layer):
    return [z for z in ZONES if layer in z["layers"]]


def candidate_pads(origin, rot_deg, pad_defs):
    """pad_defs: list of (dx, dy, w, h, drill, num, net). Returns list of dicts in board coords.

    Rotation matches KiCad: local (dx,dy) -> (dx cos + dy sin, -dx sin + dy cos).
    """
    r = math.radians(rot_deg)
    cs, sn = math.cos(r), math.sin(r)
    out = []
    for (dx, dy, w, h, drill, num, net) in pad_defs:
        x = origin[0] + dx * cs + dy * sn
        y = origin[1] - dx * sn + dy * cs
        # pad is axis-aligned in footprint space; for rot 90 the w/h swap
        if abs(rot_deg % 180) == 90:
            w, h = h, w
        out.append({"x": x, "y": y, "w": w, "h": h, "drill": drill, "num": num, "net": net,
                    "poly": box(x - w / 2, y - h / 2, x + w / 2, y + h / 2)})
    return out


def courtyard_rect(origin, rot_deg, local):
    """local = (x0,y0,x1,y1) relative to footprint origin."""
    r = math.radians(rot_deg)
    cs, sn = math.cos(r), math.sin(r)
    pts = []
    for (dx, dy) in [(local[0], local[1]), (local[2], local[1]), (local[2], local[3]), (local[0], local[3])]:
        pts.append((origin[0] + dx * cs + dy * sn, origin[1] - dx * sn + dy * cs))
    xs = [p[0] for p in pts]
    ys = [p[1] for p in pts]
    return (min(xs), min(ys), max(xs), max(ys))


def score(origin, rot_deg, pad_defs, court_local, skip_ref=None, exclude_ids=()):
    pads = candidate_pads(origin, rot_deg, pad_defs)
    court = courtyard_rect(origin, rot_deg, court_local)
    court_poly = box(*court)

    worst = {"clearance": 9e9, "item": None, "layer": None}
    worst_same = 9e9
    worst_hole = 9e9
    hole_item = None
    for pad in pads:
        for o in nearby(pad["poly"], 2.0):
            if o["id"] in exclude_ids:
                continue
            if skip_ref and o["id"].startswith(skip_ref + "."):
                continue
            d = pad["poly"].distance(o["poly"])
            if o["net"] == pad["net"]:
                worst_same = min(worst_same, d)
                continue
            need = clearance_for(pad["net"], o["net"])
            # layers must overlap for a clearance rule
            if not (o["layers"] & {p for p in LAYERS}):
                continue
            margin = d - need
            if margin < worst["clearance"]:
                worst = {"clearance": margin, "item": o["label"], "layer": sorted(o["layers"])[0],
                         "net": o["net"], "raw": d, "need": need, "pad": pad["num"]}
        if pad["drill"] > 0:
            for o in nearby(pad["poly"], 3.0):
                if o["id"] in exclude_ids or o["hole"] is None:
                    continue
                if skip_ref and o["id"].startswith(skip_ref + "."):
                    continue
                if o["kind"] == "seg":
                    continue
                cx, cy = o["poly"].centroid.x, o["poly"].centroid.y
                d = math.hypot(pad["x"] - cx, pad["y"] - cy) - pad["drill"] / 2 - o["hole"]
                if d < worst_hole:
                    worst_hole = d
                    hole_item = o["label"]

    edge = min(pad["poly"].distance(LineString([(EDGE[0], EDGE[1]), (EDGE[2], EDGE[1])]))
               for pad in pads)
    edge = min(edge,
               min(pad["poly"].distance(LineString([(EDGE[0], EDGE[3]), (EDGE[2], EDGE[3])])) for pad in pads),
               min(pad["poly"].distance(LineString([(EDGE[0], EDGE[1]), (EDGE[0], EDGE[3])])) for pad in pads),
               min(pad["poly"].distance(LineString([(EDGE[2], EDGE[1]), (EDGE[2], EDGE[3])])) for pad in pads))

    court_hits = []
    for f in G["footprints"]:
        if skip_ref and f["ref"] == skip_ref:
            continue
        fb = f["court"]
        if fb[2] <= fb[0] or fb[3] <= fb[1]:
            continue
        if not (fb[2] < court[0] or fb[0] > court[2] or fb[3] < court[1] or fb[1] > court[3]):
            court_hits.append(f["ref"])
    out_hits = [k for k, v in OUTLINES.items()
                if not (v[2] < court[0] or v[0] > court[2] or v[3] < court[1] or v[1] > court[3])]

    pth_in_court = []
    for f in G["footprints"]:
        if skip_ref and f["ref"] == skip_ref:
            continue
        for p in f["pads"]:
            if p["drill"] <= 0:
                continue
            if court[0] < p["x"] < court[2] and court[1] < p["y"] < court[3]:
                pth_in_court.append("%s.%s" % (f["ref"], p["num"]))

    zone_d = 9e9
    zone_item = None
    for z in ZONES:
        b = z["bbox"]
        d = court_poly.distance(box(*b))
        if d < zone_d:
            zone_d = d
            zone_item = "%s %s" % (z["net"], "/".join(z["layers"]))

    return {
        "origin": origin, "rot": rot_deg, "court": court,
        "margin": worst["clearance"], "item": worst["item"], "pad": worst.get("pad"),
        "raw": worst.get("raw"), "need": worst.get("need"),
        "same_net_min": worst_same, "hole_margin": worst_hole, "hole_item": hole_item,
        "edge": edge, "fp_near": court_hits, "outlines": out_hits, "pth_in_court": pth_in_court,
        "zone_d": zone_d, "zone_item": zone_item,
        "court_inside": (court[0] >= EDGE[0] + 0.2 and court[1] >= EDGE[1] + 0.2
                         and court[2] <= EDGE[2] - 0.2 and court[3] <= EDGE[3] - 0.2),
        "legal": (worst["clearance"] >= 0 and worst_hole >= 0.25 and edge >= 0.5
                  and not court_hits and not out_hits and not pth_in_court
                  and court[0] >= EDGE[0] + 0.2 and court[1] >= EDGE[1] + 0.2
                  and court[2] <= EDGE[2] - 0.2 and court[3] <= EDGE[3] - 0.2),
    }


J26_PADS = [(0.0, 0.0, 1.7, 1.95, 0.95, "1", "3V3_C"),
            (2.5, 0.0, 1.7, 1.95, 0.95, "2", "GND"),
            (5.0, 0.0, 1.7, 1.95, 0.95, "3", "/I2C1_SCL"),
            (7.5, 0.0, 1.7, 1.95, 0.95, "4", "/I2C1_SDA")]
J26_COURT = (-2.995, -2.895, 10.495, 3.945)


def j26(origin, rot=0.0):
    return score(origin, rot, J26_PADS, J26_COURT, skip_ref="J26")


if __name__ == "__main__":
    s = j26((162.45, 181.35))
    print(json.dumps({k: v for k, v in s.items() if k != "fp_near"}, indent=1, default=str))
    print("near footprints:", s["fp_near"])
