import sys
import lib.interfaceUtils as interfaceUtils
import numpy, collections
from generation.structures.structures import *
from generation.structures.generated.generatedQuarry import *
from utils._worldModification import *
from generation._resources import *
from generation._chestGeneration import *


file = "temp.txt"

interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
resources = Resources()
chestGeneration = ChestGeneration(resources, interface)

# x position, z position, x size, z size
area = (0, 0, 128, 128)  # default build area if build area is not set

interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")


# see if a build area has been specified
# you can set a build area in minecraft using the /setbuildarea command
buildArea = interfaceUtils.requestBuildArea()
if buildArea == -1:
    exit()
x1 = buildArea[0]
z1 = buildArea[2]
x2 = buildArea[3]
z2 = buildArea[5]
# print(buildArea)
area = (x1, z1, x2 - x1, z2 - z1)

if len(sys.argv) <= 1:

    # Find the highest non-air block and build the quarry there

    cx = int(area[0] + area[2]/2)
    cz = int(area[1] + area[3]/2)

    ## Find highest non-air block
    ## Note that in real construction, you want to ignore "transparent" blocks,
    ## Such as leaves, snow, grass, etc.
    cy = 255
    while interfaceUtils.getBlock(cx, cy, cz) == 'minecraft:air' :
        cy -= 1

    buildingConditions = Structures.BUILDING_CONDITIONS.copy()
    buildingConditions["position"] = [cx, cy, cz]

    quarry = GeneratedQuarry()
    quarry.build(worldModif, buildingConditions, chestGeneration) 


    worldModif.saveToFile(file)

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
