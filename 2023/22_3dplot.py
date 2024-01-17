import matplotlib.pyplot as plt
import numpy as np

# prepare some coordinates
x, y, z = np.indices((8, 8, 8))

# draw cuboids in the top left and bottom right corners, and a link between
# them
# cube1 = (x < 3) & (y < 3) & (z < 3)
# cube2 = (x >= 5) & (y >= 5) & (z >= 5)
# link = abs(x - y) + abs(y - z) + abs(z - x) <= 2
# voxelarray = cube1 | cube2 | link


# sample AoC 2023_22
# 1,0,1~1,2,1
cube1 = np.logical_and(1 <= x, x <= 1) & np.logical_and(0 <= y, y <= 2) & np.logical_and(1 <= z, z <= 1)
# 0,0,2~2,0,2
cube2 = np.logical_and(0 <= x, x <= 2) & np.logical_and(0 <= y, y <= 0) & np.logical_and(2 <= z, z <= 2)
# 0,2,3~2,2,3
# 0,0,4~0,2,4
# 2,0,5~2,2,5
# 0,1,6~2,1,6
# 1,1,8~1,1,9

# combine the objects into a single boolean array
voxelarray = cube1 | cube2

# set the colors of each object
colors = np.empty(voxelarray.shape, dtype=object)

# colors[link] = 'red'
colors[cube1] = 'blue'
colors[cube2] = 'green'

# and plot everything
ax = plt.figure().add_subplot(projection='3d')
ax.voxels(voxelarray, facecolors=colors, edgecolor='k')

# Set the axis labels
ax.set_xlabel('x')
ax.set_ylabel('y')
ax.set_zlabel('z')

plt.show()