"""Produce the E1 stitching plot: distance from every point of the In1 GND plane to a ground link."""
import pcbnew, numpy as np, math
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
STEP = 0.5

b = pcbnew.LoadBoard(PCB)
z = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
poly = z.GetFilledPolysList(z.GetLayer())
bb = poly.BBox()
xs = np.arange(bb.GetX() / 1e6, bb.GetRight() / 1e6, STEP)
ys = np.arange(bb.GetY() / 1e6, bb.GetBottom() / 1e6, STEP)
X, Y = np.meshgrid(xs, ys)
mask = np.zeros(X.shape, bool)
for j in range(X.shape[0]):
    for i in range(X.shape[1]):
        mask[j, i] = poly.Contains(pcbnew.VECTOR2I(int(round(X[j, i] * 1e6)), int(round(Y[j, i] * 1e6))))

# A ground link is a point where the plane meets the ground network: a GND via,
# or a GND through-hole pad that lies inside the plane.
links, padlinks = [], []
def touches_plane(px, py):
    return poly.Contains(pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6))))

for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition()
        if touches_plane(p.x / 1e6, p.y / 1e6):
            links.append((p.x / 1e6, p.y / 1e6))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() == "GND" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            pt = p.GetPosition()
            if touches_plane(pt.x / 1e6, pt.y / 1e6):
                links.append((pt.x / 1e6, pt.y / 1e6))

D = np.full(X.shape, 1e9)
for (lx, ly) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
D = np.where(mask, D, np.nan)

mx = np.nanmax(D)
pct = 100.0 * np.nansum(D > 10) / np.sum(mask)
print("links %d  max %.2f mm  over10 %.1f%%  cells %d" % (len(links), mx, pct, mask.sum()))

fig, ax = plt.subplots(figsize=(14, 9), dpi=130)
im = ax.imshow(D, origin="lower", extent=[xs[0], xs[-1], ys[0], ys[-1]],
               cmap="RdYlGn_r", vmin=0, vmax=max(12, mx))
cb = fig.colorbar(im, ax=ax, shrink=0.8)
cb.set_label("distance to the nearest ground link (mm)")
lv = ax.contour(X, Y, np.nan_to_num(D, nan=-1), levels=[10.0], colors="black", linewidths=0.8)
ax.clabel(lv, fmt="10 mm", fontsize=8)
ax.plot([l[0] for l in links], [l[1] for l in links], "o", ms=2.2, mfc="blue", mec="blue", label="ground link (%d)" % len(links))
ax.set_aspect("equal")
ax.set_xlabel("x (mm)")
ax.set_ylabel("y (mm)")
ax.set_title("E1 - In1 GND plane: distance to the nearest ground link\nmax %.1f mm, %.1f %% of the plane beyond 10 mm" % (mx, pct))
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(OUT + r"\E1_stitching_plot.png")
print("wrote revC\\E1_stitching_plot.png")
