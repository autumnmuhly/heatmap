stop stalking me

if you've made it this far i assume ur stalking me :)
Heatmap creates heat maps for where on earth is the best place to go 'hunting' for seismic phases. In addition, it can act as an array former. 

Check for dependencies and create environment  
- pip install pip install -v -e .

to run:  

heatmapcalc -s stationfilename -e eqcatalogfilename --minsta 1 --mineq 1 --phase S  

required inputs:  
'-p', '--phases', phase(s) of interest  
'-s', '--stations', stationfile name  
'-e', '--earthquakes' earthquake catalog name  
'--minsta', type=int, default=1, min number of stations near a grid point to form an array  
'--mineq', type=int, default=1, min number of earthquakes at an array to be successful  

optional inputs:  
'--grid', type=int, default=1000, number of grid points over earth  
'--region', type=int, nargs=4, restrict grid points to WESN box  
'--arrayradius', type=float, default=5.0, radius of array in degrees  
'-o', '--outfile', default="heatmap.jsn", output file  

to plot:  
heatmapplot  

to prepare files for array processing:  
prepvespa  
- returns a list of grid points, stations, basestations, and eq catalog  

station file:
if you need to create a station file

Grid spacing:
we use the fibanocci lattice for evenly (as much as possible) spaced grid points. for a chart on number of points and grid spacing please refer to the resources folder. would also like to add a photo of this information here but i dont know how to do that yet so please just look at the grid spacing folder

array configriation, array radius:
1 degree at the poles looks different than 1 degree at the equator. it is recommend that the array radius is 2-2.5 times the grid spacing to ensure proper sampling. this will also ensure that the grid point used to form the array is the best possible grid point in the suite to represent the array. 
