import heatmap
import pytest

def test_spacing():
    HOW_MANY=5
    reference=100
    number_points=1000
    fib_grid=heatmap.create_gridpoint(number_points)
    neighbors = heatmap.find_neighbors(HOW_MANY,reference,fib_grid)
    spacing=[]
    for i in range(number_points):
        neighbor_test=heatmap.find_neighbors(HOW_MANY,i,fib_grid)
        close=neighbor_test[0][0]
        spacing.append(close)
    min_spacing=min(spacing)
    max_spacing=max(spacing)
    assert min_spacing <2.6
    assert max_spacing<5
    print(f'this is the min {min_spacing} and this is the max {max_spacing}, diff is {max_spacing-min_spacing}')