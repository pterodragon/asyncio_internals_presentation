import sys
import numpy as np
import matplotlib.pyplot as plt
from functools import partial


def on_press(event, xl):
    print('press', event.key)
    sys.stdout.flush()
    if event.key == 'x':
        visible = xl.get_visible()
        xl.set_visible(not visible)
        fig.canvas.draw()

# Fixing random state for reproducibility
np.random.seed(19680801)


fig, ax = plt.subplots()
ax.plot(np.random.rand(12), np.random.rand(12), 'go')
xl = ax.set_xlabel('easy come, easy go')

fig.canvas.mpl_connect('key_press_event', partial(on_press, xl=xl))
ax.set_title('Press a key')
plt.show()
