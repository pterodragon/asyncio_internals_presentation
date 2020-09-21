from itertools import cycle
import tikzplotlib
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.transforms as mtransforms
import matplotlib.patches as mpatch
from matplotlib.patches import FancyBboxPatch
from matplotlib import cm
from matplotlib.collections import PatchCollection
import cycler

from dimagine.drawable import RRect, Drawable, Ellipse, Line, Text
from dimagine.ds import DTree
from dimagine.matplotlib.draw import MPlotDrawer

import re

def _tex_sanitize(s):
    """Sanitizes a string so that it can be properly compiled in TeX.
    Escapes the most common TeX special characters: ~^_#%${}
    Removes backslashes.
    """
    s = re.sub('\\\\', '', s)
    s = re.sub(r'([_^$%&#{}])', r'\\\1', s)
    s = re.sub(r'\~', r'\\~{}', s)
    return s
default_color_cycler = mpl.rcParams['axes.prop_cycle']
cmap_q = cm.get_cmap('Pastel1')
c_cycle = cycle(default_color_cycler.by_key()['color'])
c_cycle2 = cycle(cmap_q.colors)

def build_dtree():
    root = Ellipse((1, 1), (5, 5))
    curr = root

    for dx in range(4):
        curr = curr.conn(curr.trans(x=5))
    curr = curr.conn(curr.morph(RRect).trans(x=5).scale(y=1.5))
    curr = curr.conn(curr.trans((5, 20)))
    curr = curr.conn(curr.morph(Ellipse).trans((5, -20)))
    curr = curr.conn(curr.morph(RRect, facecolor=next(c_cycle2)).trans(x=5).expand(x=10))
    curr = curr.text_label(_tex_sanitize('d_$2'), 36)
    dt = DTree(root)
    
    return dt

def build_lines():
    root = Line((0, 0), (30, 0))
    dt = DTree(root)
    return dt


dt = build_dtree()
dt_line = build_lines()

figax = plt.subplots()
fig: plt.Figure = figax[0]
ax: plt.Axes = figax[1]

# ax.text(2, 6, r'an equation: $E=mc^2$', fontsize=15)
drawer = MPlotDrawer(ax, [dt, dt_line])
drawer.draw()
# tikzplotlib.clean_figure()
eap = []
eap = ["x=15pt", "y=15pt"]
# eap += [ "xmajorticks=false" ]
# eap += ["hide axis"]
eap.append('ticks=none')

tikzplotlib.save(
    "mytikz.tex",
    extra_axis_parameters=eap,
    axis_width="180pt",
    axis_height="180pt",
)
# write text inside shape... # arrows?
# plt.show()

