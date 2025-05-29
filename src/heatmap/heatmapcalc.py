
import argparse
import jsonpickle

from .mesh_create import find_neighbors,fibonacci_sphere,create_gridpoint
from .mesh_setup import latlon_cartesian,cart_latlon, radius_per_gridpoint
from .gridpoint import Gridpoint,Station,EQ,Location
from .array import Array,form_all_array,ArrayToEqlist,EqtoArrayList,EqGridAssignment,form_eq,group_items_by_dist,items_in_dist
from .distaz import DistAz
from .read_datafiles import (
    read_stations_adept, read_earthquakes_adept,
    load_arrays_json, save_arrays_json
    )
from .taup import (
   phase_dist_range, taup_time, taup_phase
   )

def calc_good_arrays(phase_list, array_list, eq_list, min_station=1, min_eq_needed=1):

    # a list of eq for all arrrays
    arrayToeq=[]
    #array class that will hold array-eq pairs class in prep for testing distance
    for arr in array_list:
        arrayToeq.append(ArrayToEqlist(arr))
    #evt class that will holds eq-array pairs
    eqToarray=[]
    for evt in eq_list:
        eqToarray.append(EqtoArrayList(evt))

    #loop over evts and arrays and check if distance range is met
    for phase in phase_list:
        # Distance range of phase, from TauP
        dist = phase_dist_range(phase)
        if dist is None:
            print(f"Cannot determine phase distance range for {phase}")
            sys.exit(0)
        print(f"phase: {phase}  dist: {dist}")
        for arr in arrayToeq:
            for evt in eq_list:
                    arr.check_eq(evt,dist,min_station)


    #loop over array in array list to decided if enough eq exist to be considered an array
    good_arrays=[]
    for arr in arrayToeq:
        if arr.eqcount>=min_eq_needed:
            good_arrays.append(arr)

    if len(good_arrays) == 0:
        print(f"no arrays pass min eq {min_eq_needed} for radius {radius_point_deg} deg")
    return good_arrays



def parseArgs():
    parser = argparse.ArgumentParser(prog='HeatmapCalc',
                    description='Finds arrays for beamforming',
                    epilog='Text at the bottom of help')
    parser.add_argument('-p', '--phases', nargs="+", help="phases of interest")
    parser.add_argument('-s', '--stations')
    parser.add_argument('-e', '--earthquakes')
    parser.add_argument('--grid', type=int, default=1000, help="number of grid points over earth")
    parser.add_argument('--arrayradius', type=float, default=5.0, help="radius of array in degrees")
    parser.add_argument('--minsta', type=int, default=1, help="min number of stations near a grid point to form an array")
    parser.add_argument('--mineq', type=int, default=1, help="min number of earthquakes at an array to be successful")
    parser.add_argument('-o', '--outfile', default="heatmap.json", help="output file")

    return parser.parse_args()


def main():
    args = parseArgs()

    radius_point_deg=radius_per_gridpoint(args.grid)
    if args.arrayradius < radius_point_deg:
        print(f"WARNING: array radius, {args.arrayradius} less than gridpoint spacing, {radius_point_deg}")
    grid_array=create_gridpoint(args.grid)

    station_list=read_stations_adept(args.stations)
    eq_list=read_earthquakes_adept(args.earthquakes)

    array_list=form_all_array(station_list, grid_array, args.arrayradius, args.minsta)
    if len(array_list) == 0:
        print(f"no arrays pass for radius {args.arrayradius} deg with  min {args.minsta} stations")
        return 1

    good_arrays = calc_good_arrays(args.phases, array_list, eq_list, args.minsta, args.mineq)

    mydata={
        "array_list":array_list,
        "grid_array": grid_array,
        "good_arrays": good_arrays,
        "phase": args.phases,
        "dist": phase_dist_range(args.phases),
        "arrayradius": args.arrayradius,
        "min_sta_per_array": args.minsta,
        "min_eq_at_array": args.mineq,
        "eq_list": eq_list,
        "station_list": station_list,
        "radius_point_deg": args.arrayradius,
        "radius_of_earth": 6371
    }

    with open(args.outfile, "w") as outf:
        outf.write(jsonpickle.encode(mydata))
    return 0

if __name__ == '__main__':
    sys.exit(main())
