import tikzplotlib
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import matplotlib.patches as mpatch
from matplotlib.patches import FancyBboxPatch
from matplotlib import cm
from matplotlib.collections import PatchCollection

from dimagine.drawable import Rect, Drawable
from dimagine.ds import DTree

def build_dtree():
    dt = DTree([Rect((x + 1, 1), (x + 3, 3)) for x in range(0, 21, 5)])
    dt.root.add_child(Rect((10, 0), (10 + 2, 2)))
    return dt

dt = build_dtree()

figax = plt.subplots()
fig: plt.Figure = figax[0]
fig.set_figheight(5)
fig.set_figwidth(10)
ax: plt.Axes = figax[1]
ax.autoscale(True)

def build_boxes(dt: DTree):
    patches = []
    def build_patch(da: Drawable):
        fancybox = mpatch.FancyBboxPatch(
            da.bbox.bl, *da.bbox.wh,
            boxstyle=mpatch.BoxStyle("Round", pad=1),
            facecolor='white', edgecolor='black'
            )
        patches.append(fancybox)
    dt.dfs(build_patch)

    return patches

for patch in build_boxes(dt):
    ax.add_artist(patch)
(bl_x, bl_y), (tr_x, tr_y) = dt.bbox

m = max(tr_x, tr_y) + 2
ax.set_xlim((0, m + 100))
ax.set_ylim((0, m))
ax.set_aspect('equal')
# ax.set_axis_off()

tikzplotlib.save("mytikz.tex")
plt.show()

