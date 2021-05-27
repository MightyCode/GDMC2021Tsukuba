from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import generation._resourcesLoader as resLoader
import utils._utils as _utils
from utils._worldModification import *
import utils.argumentParser as argParser

file = "temp.txt"
interface = interfaceUtils.Interface(buffering=True)
worldModif = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
area = argParser.getBuildArea(interface, args)

if area == -1:
    exit()

if not args.remove:
    resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration = ChestGeneration(resources, interface)
    structure = resources.structures["basicgeneratedwell"]

    info = structure.info
    buildingCondition = BaseStructure.createBuildingCondition()
    buildingInfo = structure.setupInfoAndGetCorners()
    buildingCondition["flip"] = 0
    buildingCondition["rotation"] = 0
    buildingInfo = structure.getNextBuildingInformation( buildingCondition["flip"], buildingCondition["rotation"])
    buildingCondition["position"] = [9, 72, 0]
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]
    corners = structure.getCornersLocalPositionsAllFlipRotation(info["mainEntry"]["position"])

    buildingCondition["replaceAllAir"] = 3

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

    structure.build(worldModif, buildingCondition, chestGeneration)
    worldModif.saveToFile(file)

else : 
    if args.remove == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(args.remove)
    worldModif.undoAllModification()