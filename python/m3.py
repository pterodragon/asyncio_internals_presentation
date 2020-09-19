import matplotlib.pyplot as plt
import matplotlib.patches as mpatch

fig, ax = plt.subplots()
rectangles = {'skinny' : mpatch.Rectangle((2,2), 8, 2),
              'square' : mpatch.Rectangle((4,6), 6, 6)}

for r in rectangles:
    ax.add_artist(rectangles[r])
    rx, ry = rectangles[r].get_xy()
    cx = rx + rectangles[r].get_width()/2.0
    cy = ry + rectangles[r].get_height()/2.0

    ax.annotate(r, (cx, cy), color='w', weight='bold', 
                fontsize=6, ha='center', va='center')

ax.set_xlim((0, 15))
ax.set_ylim((0, 15))
ax.set_aspect('equal')
plt.show()
