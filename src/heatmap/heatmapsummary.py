#!/usr/bin/env python

import argparse
import os
import datetime
import sys
import jsonpickle
from types import SimpleNamespace

def summary(args):
    infilename = args.heatmapfile
    with open(infilename, "r") as inf:
        mydata = jsonpickle.decode(inf.read())
    mydata = SimpleNamespace(mydata)

    print(f"Array radius: {mydata.arrayradius}")
    print(f"Grid spacing: {mydata.radius_point_deg}")
    print(f"Num grid points: {len(mydata.grid_array)}")
    print(f"Num Earthquakes: {len(mydata.eq_list)}")
    print(f"Good Arrays: {len(mydata.good_arrays)}")
    if args.arrays:
        for arr_eq in mydata.good_arrays:
            arr = arr_eq.array
            print(f"  {arr.pt.loc.lat:0.2f}/{arr.pt.loc.lon:0.2f} {arr.basestation.netwrk}_{arr.basestation.name} {len(arr.sta_list)} stations, {len(arr_eq.eqlists)} earthquakes")


def parseArgs():
    parser = argparse.ArgumentParser(prog='HeatmapCalc',
                    description='Finds arrays for beamforming',
                    epilog='Text at the bottom of help')
    parser.add_argument('-f', '--heatmapfile', default="heatmap.json", help="input file")
    parser.add_argument('--arrays', action='store_true', help="print arrays")

    return parser.parse_args()


def main():
    args = parseArgs()
    return summary(args)

if __name__ == '__main__':
    sys.exit(main())
