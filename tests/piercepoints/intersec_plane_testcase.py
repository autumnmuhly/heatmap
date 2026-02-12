
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from heatmap import create_gridpoint,latlon_cartesian
import sys
from pierce import create_plane


normal,d,point=create_plane((33,-98,0),(37,-98,0),(41,-98,1))



# Choose a grid size that surrounds your point
grid_size = 3000 
x0, y0, z0 = point 
# Grid spanning around the anchor point
x_range=np.linspace(x0-grid_size,x0+grid_size,200)
y_range=np.linspace(y0-grid_size,y0+grid_size,200)
xx,yy=np.meshgrid(x_range,y_range)
z=(-normal[0] * xx - normal[1] * yy - d) * 1. / normal[2]


radius_of_earth=6378
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_surface(xx, yy, z, cmap='viridis', alpha=0.7)
ax.set_box_aspect([radius_of_earth,radius_of_earth,radius_of_earth])
plt.show()






# ax.scatter(third.x,third.y,third.z,color='green',s=20)
# ax.scatter(second.x,second.y,second.z, color='green',s=20)
# ax.scatter(first.x,first.y,first.z,color='green' ,s=20)
# ax.scatter(fourth.x,fourth.y,fourth.z, color='green',s=20)
#plot normal vector
#origin = np.zeros(3)
#origin = np.array([first.x, first.y, first.z])
#ax.quiver(origin[0], origin[1], origin[2],normal[0], normal[1], normal[2],color='red', linewidth=2)