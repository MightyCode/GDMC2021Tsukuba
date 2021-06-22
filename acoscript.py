import threading
import time
import numpy as np
import AntColonyOptimization.aco as antco
from utils.worldModification import *
from lib.worldLoader import WorldSlice
import lib.interfaceUtils as iu

block1 = (10,3,10)
block2 = (-10,3, -4)
interface = iu.Interface()
area = (min(block1[0],block2[0]) - 5, 0, min(block1[2],block2[2]) - 5 , max(block1[0],block2[0]) + 6, 50,  max(block1[2],block2[2]) + 6)
iu.setBuildArea(area[0], area[1], area[2], area[3], area[4], area[5])
iu.makeGlobalSlice()
xmatrix = area[3] - area[0]
zmatrix = area[5] - area[2]
startmatrix = (area[0], area[2])
start = [abs(block1[0] - startmatrix[0]), abs(block1[2] - startmatrix[1])]
end = [abs(block2[0] - startmatrix[0]), abs(block2[2] - startmatrix[1])]

aco = antco.AntColonyOptimizer(xmatrix, zmatrix, startmatrix, start, end)

aco.launch()

print(xmatrix)
print(zmatrix)

