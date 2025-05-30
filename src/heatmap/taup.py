
import subprocess
import json
import sys



def getTauPAsJson(cmd):
    """
    Gets results for a TauP command via json. The --json parameter is
    automatically appended to the command.
    """
    splitCmd = cmd.split(" ")
    splitCmd.append("--json")
    result = subprocess.run(splitCmd, capture_output=True)
    result.check_returncode() # will raise CalledProcessError if not ok
    return json.loads(result.stdout)


def taup_phase(phases, sourcedepth=0, model=None):
    """
    Describes the phases.
    Parameters:
    -----------
    phases  - comma separated list of phases, or list of phases
    sourcedepth - optional source depth, defaults to zero
    model - optional velocity model name, defaults to iasp91

    Returns dict parsed from the json containing 'arrivals' with a list of the
    Arrival objects.
    """
    if isinstance(phases, list):
        ph = ",".join(phases)
    else:
        ph = phases
    cmd = f"taup phase -p {ph} -h {sourcedepth}"
    if model is not None:
        cmd += f" --mod {model}"
    taupjson = getTauPAsJson(cmd)
    return taupjson



def taup_time(degrees, phases, sourcedepth=0, model=None, amp=False):
    """
    Calculates arrivals for the phases.
    Parameters:
    -----------
    degrees - either a single distance or a list of distances
    phases  - comma separated list of phases, or list of phases
    sourcedepth - optional source depth, defaults to zero

    Returns dict parsed from the json containing 'arrivals' with a list of the
    Arrival objects.
    """
    if isinstance(degrees, list):
        deg = ",".join(map(str, degrees))
    else:
        deg = degrees
    if isinstance(phases, list):
        ph = ",".join(phases)
    else:
        ph = phases
    cmd = f"taup time --deg {deg} -p {ph} -h {sourcedepth}"
#cmd = f"{TAUP_PATH}/taup time --deg {deg} -p {ph} -h {sourcedepth}"
    if model is not None:
        cmd += f" --mod {model}"
    if amp:
        cmd += " --amp"
    taupjson = getTauPAsJson(cmd)
    return taupjson

def phase_dist_range(phase, sourcedepth=0, model=None):
    phaseDesc = taup_phase(phase, sourcedepth, model)
    dist = None
    if 'descriptions' in phaseDesc and len(phaseDesc['descriptions']) > 0:
        minDist = float(phaseDesc['descriptions'][0]['minexists']['dist'])
        maxDist = float(phaseDesc['descriptions'][0]['maxexists']['dist'])
        delta = maxDist - minDist
        if delta >= 360:
            dist = (0, 180)
        else:
            maxDist = (maxDist-1) % 360 +1 # 0<maxDist<=360
            minDist = minDist % 360        # 0<=minDist<360
            if minDist < 180 and maxDist <= 180:
                dist = (minDist, maxDist)
            elif minDist < 180 and maxDist > 180:
                dist = (min(minDist, 360-maxDist), 180)
            elif minDist > 180 and maxDist < 180:
                dist = (0, max(360-minDist, maxDist))
            else:
                dist = (min(360-minDist, 360-maxDist), max(360-minDist, 360-maxDist))

    return dist

def main():
    # calculate travel times and parse the output json.
    # Note that taup must be on your PATH env var
    degrees = 35
    depth = 100
    phases = "P,S,SKKKS"

    taupjson = taup_time(degrees, phases, depth)
    print(f"Got {len(taupjson['arrivals'])} arrivals:")
    for arr in taupjson["arrivals"]:
        print(f"  {arr['phase']} arrives at {arr['time']} and traveled {arr['puristdist']} deg.")
    return 0

if __name__ == '__main__':
    sys.exit(main())
