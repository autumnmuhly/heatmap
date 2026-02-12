#Finding the variance between nearest neighbors 
import heatmap
from heatmap.mesh_create import find_neighbors,fibonacci_sphere,create_gridpoint
from heatmap.mesh_setup import Neighbors

number_pts=9000
grid=create_gridpoint(number_pts)
how_many=2
reference=2
neighbors_list=[]

for pt in grid:
    pairs_list=find_neighbors(how_many,pt,grid)
    distance = []
    neighbor = []
    for pair in pairs_list:
        distance.append(pairs_list[0])
        neighbor.append(pairs_list[1])
    neighbors_list.append(Neighbors(pt,distance,neighbor))

for pt in neighbors_list:
    min_var=min(pt.distances)
    max_var=max(pt.distances)
    print (f'the variance is {min_var},{max_var}')