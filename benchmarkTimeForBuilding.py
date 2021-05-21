# Make sure that your config/config.json -> debugMode = false
import time
milliseconds = int(round(time.time() * 1000))

from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import generation._resourcesLoader as resLoader
import utils._math as _math
from utils._worldModification import *
from lib.worldLoader import WorldSlice
import sys

interface = interfaceUtils.Interface(buffering=True)
worldModif = WorldModification(interface)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-150 0 ~-150 ~150 255 ~150")
buildArea = interfaceUtils.requestBuildArea()

if buildArea == -1:
    exit()
x1 = buildArea[0]
z1 = buildArea[2]
x2 = buildArea[3]
z2 = buildArea[5]
area = (x1, z1, x2 - x1, z2 - z1)

resources = Resources()
resLoader.loadAllResources(resources)
chestGeneration = ChestGeneration(resources, interface)
structure = resources.structures["basicwindmill"]
info = structure.info
buildingCondition = Structures.BUILDING_CONDITIONS.copy()
buildingInfo = structure.getNextBuildingInformation()
buildingCondition["flip"] = 3
buildingCondition["rotation"] = 3
buildingCondition["size"] = buildingInfo["size"]

buildingCondition["replaceAllAir"] = 3
buildingCondition["position"] = [0, 71, 0]
structureBiomeId = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]

structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])
if structureBiomeBlockId == "-1" :
    structureBiomeBlockId = "0" 
    
# Load block for structure biome
for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
    if aProperty in resources.biomesBlocks["rules"]["village"]:
        buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]
# Load block for structure biome
for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
    if aProperty in resources.biomesBlocks["rules"]["structure"]:
        buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

for i in range(70):
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["position"] = [ - 100 + 20 * (int(i / 10)), 71, - 100 + 20 * (int(i % 10))]
    print(str(i) + " : " + str(buildingCondition["position"]))
    structure.build(worldModif, buildingCondition, chestGeneration)


milliseconds2 = int(round(time.time() * 1000))
result = milliseconds2 - milliseconds 

print(result / 1000)