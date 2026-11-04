"""E1 stitching plot from the live board: strict links inside both GND pours, 1 mm grid."""
import pcbnew, numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

PCB = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\pcb\MoriShield_Carrier.kicad_pcb"
OUT = r"C:\Users\aswin\OneDrive\Desktop\PCB\SERIGREEN\new pcb\revC"
STEP = 1.0

b = pcbnew.LoadBoard(PCB)
filler = pcbnew.ZONE_FILLER(b)
filler.Fill(b.Zones())

z_in1 = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "In1.Cu")
z_bcu = next(z for z in b.Zones() if z.GetNetname() == "GND" and b.GetLayerName(z.GetLayer()) == "B.Cu")
p_in1 = z_in1.GetFilledPolysList(z_in1.GetLayer())
p_bcu = z_bcu.GetFilledPolysList(z_bcu.GetLayer())

bb = b.GetBoardEdgesBoundingBox()
xs = np.arange(bb.GetX() / 1e6, bb.GetRight() / 1e6, STEP)
ys = np.arange(bb.GetY() / 1e6, bb.GetBottom() / 1e6, STEP)
X, Y = np.meshgrid(xs, ys)
m_in1 = np.zeros(X.shape, bool)
m_bcu = np.zeros(X.shape, bool)
for j in range(X.shape[0]):
    for i in range(X.shape[1]):
        v = pcbnew.VECTOR2I(int(round(X[j, i] * 1e6)), int(round(Y[j, i] * 1e6)))
        m_in1[j, i] = p_in1.Contains(v)
        m_bcu[j, i] = p_bcu.Contains(v)
m = m_in1 & m_bcu

def inside_both(px, py):
    v = pcbnew.VECTOR2I(int(round(px * 1e6)), int(round(py * 1e6)))
    return p_in1.Contains(v) and p_bcu.Contains(v)

links = []
for t in b.GetTracks():
    if t.Type() == pcbnew.PCB_VIA_T and t.GetNetname() == "GND":
        p = t.GetPosition()
        if inside_both(p.x / 1e6, p.y / 1e6):
            links.append((p.x / 1e6, p.y / 1e6))
for f in b.GetFootprints():
    for p in f.Pads():
        if p.GetNetname() == "GND" and p.GetAttribute() == pcbnew.PAD_ATTRIB_PTH:
            pt = p.GetPosition()
            if inside_both(pt.x / 1e6, pt.y / 1e6):
                links.append((pt.x / 1e6, pt.y / 1e6))

D = np.full(X.shape, 1e9)
for (lx, ly) in links:
    D = np.minimum(D, np.hypot(X - lx, Y - ly))
Dm = np.where(m, D, np.nan)
mx = float(np.nanmax(Dm))
pct = 100.0 * np.nansum(Dm > 10) / m.sum()
print("links=%d cells=%d max=%.2f mm over10=%.1f %%" % (len(links), m.sum(), mx, pct))

fig, ax = plt.subplots(figsize=(14, 9), dpi=130)
im = ax.imshow(Dm, origin="lower", extent=[xs[0], xs[-1], ys[0], ys[-1]],
               cmap="RdYlGn_r", vmin=0, vmax=max(11, mx))
cb = fig.colorbar(im, ax=ax, shrink=0.8)
cb.set_label("distance to the nearest ground link (mm)")
ax.contour(X, Y, np.nan_to_num(Dm, nan=-1), levels=[10.0], colors="black", linewidths=0.8)
ax.plot([l[0] for l in links], [l[1] for l in links], "o", ms=2.0, mfc="blue", mec="blue",
        label="ground link in both pours (%d)" % len(links))
ax.set_aspect("equal"); ax.set_xlabel("x (mm)"); ax.set_ylabel("y (mm)")
ax.set_title("E1 - GND stitching, Rev C: max %.2f mm, %.1f %% of the plane beyond 10 mm\n"
             "B.Cu GND pour + In1 plane, %d links, 1 mm grid" % (mx, pct, len(links)))
ax.legend(loc="upper right", fontsize=8)
fig.tight_layout()
fig.savefig(OUT + r"\E1_stitching_plot.png")
print("wrote E1_stitching_plot.png")
