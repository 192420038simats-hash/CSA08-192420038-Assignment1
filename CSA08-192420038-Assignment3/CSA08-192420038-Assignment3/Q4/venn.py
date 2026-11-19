"""Q4 - draws one Venn diagram per result (saved as PNG)."""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import Circle, Rectangle

titles = ["A | B  (union)", "A & B  (intersection)", "A - B  (difference)", "A ^ B  (symmetric difference)", "U - (A | B)  (neither)"]
fig, axes = plt.subplots(1, 5, figsize=(17, 3.6))
for ax, title in zip(axes, titles):
    ax.set_xlim(0, 10); ax.set_ylim(0, 6); ax.set_aspect("equal"); ax.axis("off"); ax.set_title(title, fontsize=11)
    shade = "#f4a261"
    if title.startswith("U"):
        ax.add_patch(Rectangle((0.2, 0.2), 9.6, 5.6, fc=shade, ec="black"))
        ax.add_patch(Circle((3.9, 3), 2.0, fc="white", ec="black")); ax.add_patch(Circle((6.1, 3), 2.0, fc="white", ec="black"))
    else:
        ax.add_patch(Rectangle((0.2, 0.2), 9.6, 5.6, fc="white", ec="black"))
        ca, cb = Circle((3.9, 3), 2.0, fc="white", ec="black", lw=1.5), Circle((6.1, 3), 2.0, fc="white", ec="black", lw=1.5)
        if title.startswith("A |"):
            ca.set_facecolor(shade); cb.set_facecolor(shade)
        ax.add_patch(ca); ax.add_patch(cb)
        if title.startswith("A &"):
            # lens: draw B clipped to A
            lens = Circle((6.1, 3), 2.0, fc=shade, ec="black"); ax.add_patch(lens); lens.set_clip_path(ca)
        if title.startswith("A -"):
            ca.set_facecolor(shade); ax.add_patch(Circle((6.1, 3), 2.0, fc="white", ec="black"))
        if title.startswith("A ^"):
            ca.set_facecolor(shade); cb.set_facecolor(shade)
            ax.add_patch(ca); ax.add_patch(cb)
            lens = Circle((6.1, 3), 2.0, fc="white", ec="black"); ax.add_patch(lens); lens.set_clip_path(ca)
            ax.add_patch(Circle((3.9, 3), 2.0, fc="none", ec="black", lw=1.5)); ax.add_patch(Circle((6.1, 3), 2.0, fc="none", ec="black", lw=1.5))
    ax.text(2.7, 3, "A", fontsize=14, ha="center"); ax.text(7.3, 3, "B", fontsize=14, ha="center"); ax.text(9.4, 5.3, "U", fontsize=11, ha="right")
plt.tight_layout(); plt.savefig("venn_diagrams.png", dpi=110); print("saved venn_diagrams.png")
