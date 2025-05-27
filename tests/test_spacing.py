import heatmap
import pytest

def test_spacing(number_points):
    HOW_MANY=5
    reference=100
    number_points=10
    fib_grid=heatmap.create_gridpoint(number_points)
    neighbors = heatmap.find_neighbors(HOW_MANY,reference,fib_grid)
    spacing=[]
    for i in range(number_points):
        neighbor_test=heatmap.find_neighbors(HOW_MANY,i,fib_grid)
        close=neighbor_test[0][0]
        spacing.append(close)
    min_spacing=min(spacing)
    max_spacing=max(spacing)
    #assert min_spacing <2.6
    #assert max_spacing<5
    #add in the average grid spacing 
    print(f'this is the min {min_spacing} and this is the max {max_spacing}, diff is {max_spacing-min_spacing}')
    
def test_spacing_2():
    #changing fib grid to be a grid that we do know 
    HOW_MANY=5
    reference=100
    number_points=1000
    #fib_grid=heatmap.create_gridpoint(number_points)
    lat=[90,-90,30,0]
    lon=[0,0,0,0]
    x_com=[]
    y_com=[]
    z_com=[]
    for i in range(len(lat)):
        x,y,z=heatmap.latlon_cartesian(lat[i],lon[i])
        x_com.append(x)
        y_com.append(y)
        z_com.append(z)
    fib_grid=Gridpoint(lat,lon,x_com,y_com,z_com)
    neighbors = heatmap.find_neighbors(HOW_MANY,reference,fib_grid)
    spacing=[]
    for i in range(number_points):
        neighbor_test=heatmap.find_neighbors(HOW_MANY,i,fib_grid)
        close=neighbor_test[0][0]
        spacing.append(close)
    min_spacing=min(spacing)
    max_spacing=max(spacing)
    #assert min_spacing <2.6
    #assert max_spacing<5
    #add in the average grid spacing 
    print(f'this is the min {min_spacing} and this is the max {max_spacing}, diff is {max_spacing-min_spacing}')