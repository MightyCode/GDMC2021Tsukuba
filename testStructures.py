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

file = "temp.txt"
interface = interfaceUtils.Interface()
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

if len(sys.argv) <= 1 :
    resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration = ChestGeneration(resources, interface)
    structure = resources.structures["haybalehouse1"]

    info = structure.info
    buildingCondition = Structures.BUILDING_CONDITIONS.copy()
    buildingInfo = structure.getNextBuildingInformation()
    buildingCondition["flip"] = 3
    buildingCondition["rotation"] = 3
    buildingCondition["position"] = [82, 63, -3]
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]
    print(structure.getCornersLocalPositions(info["mainEntry"]["position"], 3, 1))
    corners = structure.getCornersLocalPositionsAllFlipRotation(info["mainEntry"]["position"])
    print(_math.isTwoRectOverlapse([-30, 64, 0], [-1, -2, 4, 2], [-22, 65, 2], [-2, -1, 1, 5], 4))
    
    exit()

    buildingCondition["replaceAllAir"] = 3

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

    structure.build(worldModif, buildingCondition, chestGeneration)
    worldModif.saveToFile(file)

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()