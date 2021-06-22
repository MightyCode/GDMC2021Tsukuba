from generation.resources import *
from generation.chestGeneration import *
from generation.structures.structures import *
from generation.structureManager import *
from generation.floodFill import *
from utils.worldModification import *
from lib.worldLoader import WorldSlice
#seed testing : -2997648135289524795


block1 = (10 3 10)
block2 = (-10 3 4)
interface = interfaceUtils.Interface()
area = (min(block1[0],block2[0]), 0, min(block1[2],block2[2]) , max(block1[0],block2[0]), 50,  max(block1[2],block2[2]))
iu.setBuildArea(area[0] -5, area[1], area[2]-5, area[3] + 6, area[4] + 6, area[5] + 6)
floodFill = FloodFill()
if buildArea != -1:
    x1 = buildArea[0]
    z1 = buildArea[2]
    x2 = buildArea[3]
    z2 = buildArea[5]
    print(buildArea)
    area = (x1, z1, x2 - x1, z2 - z1)

print(area)
ws = WorldSlice(area)
xPos = -36
zPos = -25
yPos = floodFill.getHeight(xPos,zPos, ws)
print(xPos,yPos,zPos)
testing = floodFill.floodfill(xPos,yPos,zPos,ws,15)
print(testing)