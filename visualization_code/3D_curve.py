import numpy as np
from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, FFMpegWriter
from matplotlib import cm

fig = plt.figure()
ax = fig.add_subplot(projection='3d')

theta = np.linspace(0, 2 * np.pi, 360)
epsilon = 1
u = np.array([1, 0.9, 0.6])
v = np.array([0.2, 0.3, 0.4])
uu = np.dot(u, u)
uv = np.dot(u, v)
vv = np.dot(v, v)

# Move on a circle around (x_0, y_0) with radius epsilon
x = epsilon * np.sin(theta)
y = epsilon * np.cos(theta)

# Estimate the color difference value
z = np.square(epsilon) * (np.square(np.cos(theta)) * uu + 2 * np.cos(theta) * np.sin(theta) * uv + np.square(np.sin(theta)) * vv)

color_difference = ax.scatter(0, 0, 0, color='black')
color_difference = ax.plot(x, y, z)
ax.plot(x, y, zdir='z', zs=0, color='black')

ax.plot(np.array([0, 1]), np.array([0, 0]), zdir='z', zs=0, color='black')
ax.text(0.5, 0.2, 0, r'$\epsilon=1$', horizontalalignment='center')

# Set the axis properties
ax.set_zlim(0)
ax.set_xticks([-1, -0.5, 0, 0.5, 1])
ax.set_yticks([-1, -0.5, 0, 0.5, 1])

ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel(r'$F(\Theta)$')
ax.view_init(22.5, 30, 0)

#plt.title(r'$F(\theta)$ for $\theta \in [0, 360)$')

plt.tight_layout()
#plt.show()

def animation_frame(i):
    elev = 30
    roll = 0
    azim = i % 360
    ax.view_init(elev, azim, roll)
    return color_difference

animation = FuncAnimation(fig, func=animation_frame, frames=np.arange(30, 390, 0.1))
writer = FFMpegWriter(fps=60, metadata={'artist': 'Laszlo Egri'}, bitrate=800)
animation.save('color_difference.mp4', writer)