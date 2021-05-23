# Make sure that your config/config.json -> debugMode = false
import time
milliseconds = int(round(time.time() * 1000))

from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import generation._resourcesLoader as resLoader
from utils._worldModification import *
import utils.argumentParser as argParser
import utils._utils as _utils

interface = interfaceUtils.Interface(buffering=True)
worldModif = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
area = argParser.getBuildArea(interface, args)

if area == -1:
    exit()

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
structureBiomeId = _utils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
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

for i in range(200):
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["position"] = [ - 150 + 20 * (int(i / 10)), 71, - 150 + 20 * (int(i % 10))]
    print(str(i) + " : " + str(buildingCondition["position"]))
    structure.build(worldModif, buildingCondition, chestGeneration)


milliseconds2 = int(round(time.time() * 1000))
result = milliseconds2 - milliseconds 

print(result / 1000)