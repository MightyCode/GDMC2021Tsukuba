from generation.resources import *
from generation.chestGeneration import *
from generation.structures.structures import *
from generation.structureManager import *
from generation.floodFill import *
import generation.resourcesLoader as resLoader
import utils.utils as utils
from utils.worldModification import *
import utils.argumentParser as argParser
import lib.interfaceUtils as iu
import generation.loremaker as loremaker
import copy

file = "temp.txt"
interface = interfaceUtils.Interface(buffering=True, caching = True)
interface.setCaching(True)
interface.setBuffering(True)
iu.setCaching(True)
iu.setBuffering(True)
worldModif = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
area = argParser.getBuildArea(args)

if area == -1:
    exit()

if not args.remove:
    resources = Resources()
    resLoader.loadAllResources(resources)
    chestGeneration = ChestGeneration(resources, interface)
    structure = resources.structures["adventurerhouse"]

    info = structure.info
    buildingCondition = BaseStructure.createBuildingCondition()
    buildingInfo = structure.setupInfoAndGetCorners()
    buildingCondition["flip"] = 0
    buildingCondition["rotation"] = 0
    buildingInfo = structure.getNextBuildingInformation( buildingCondition["flip"], buildingCondition["rotation"])
    buildingCondition["position"] = [3220, 72, 4086]
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]

    buildingCondition["replaceAllAir"] = 3

    structureBiomeId = utils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = "0" 
        
    settlementData = {}
    settlementData["materialsReplacement"] = {}
    settlementData["materialsReplacement"]["villageName"] = "TestLand"
    loremaker.voteForColor(settlementData)
    buildingCondition["replacements"] = copy.deepcopy(settlementData["materialsReplacement"])

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