import argparse
import lib.interfaceUtils as iu

def giveArgsAndParser():
    parser = argparse.ArgumentParser(description="Build a Minecraft Settlement, by Bordeaux Team (2021)")
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument("-p", "--player",
                        help="build the settlement around the player's current location",
                    action="store_true")

    group.add_argument("-c", "--coordinates", nargs = 6, type=int,
                    metavar=('x0', 'y0', 'z0', 'x1', 'y1', 'z1'),
                    help="build the settlement on the area defined by these coordinates")
    parser.add_argument("-a", "--radius", type=int, metavar="A",
                        help="Radius for building area, only meaningful with -p")

    parser.add_argument("-r", "--remove", type=str, metavar="R", nargs='?',
                        help="Remove all structure if debug was activated, temp.txt if r specified, elsewhere file name: -r temp_0.txt")


    args = parser.parse_args()
    return [args, parser]

def getBuildArea(interfaceUtils, args):
    size = 128 

    if(args.radius):
        size = args.radius

    if (args.player):
        area = iu.requestPlayerArea(size * 2 , size * 2)
    elif (args.coordinates):
        x0, y0, z0, x1, y1, z1 = args.coordinates
        area = iu.setBuildArea(x0, y0, z0, x1, y1, z1)
    else :
        area = iu.setBuildArea(-size, 0, -size, size, 255, size)

    print("AREA :" + str(area))
    return area