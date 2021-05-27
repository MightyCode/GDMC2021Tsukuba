import time
milliseconds = int(round(time.time() * 1000))

from generation._resources import *
from generation._chestGeneration import *
from generation._structureManager import *
from generation._floodFill import *
import generation.generator as generator
import generation._resourcesLoader as resLoader
import utils._utils as _utils
from utils._worldModification import *
import utils.argumentParser as argParser
import generation.loremaker as loremaker
import generation.road as road
import lib.interfaceUtils as iu
from random import choice


file = "temp.txt"
interface = interfaceUtils.Interface(buffering=True, caching = True)
interface.setCaching(True)
interface.setBuffering(True)
iu.setCaching(True)
iu.setBuffering(True)
worldModif = WorldModification(interface)
args, parser = argParser.giveArgsAndParser()
area = argParser.getBuildArea(interface, args)

if area == -1:
    exit()
    
# Three main steps : choose structures and find its positions, make road between these structures, and finaly build structures.
if not args.remove:
    
    resources = Resources()
    resLoader.loadAllResources(resources)

    chestGeneration = ChestGeneration(resources, interface)
    iu.makeGlobalSlice()
    floodFill = FloodFill(area)
    
    settlementData = generator.createSettlementData(area, resources)

    structureMananager = StructureManager(settlementData, resources)

    for i in range(settlementData["structuresNumberGoal"]) : 
        # 0 -> normal, 1 -> replacement, 2 -> no more structure
        result = structureMananager.chooseOneStructure()
        structureMananager.printStructureChoose()

        if result == 2 :
            settlementData["structuresNumberGoal"] = i
            break
        
        if result == 1: 
            settlementData["structuresNumberGoal"] -= 1
            continue

        structure = resources.structures[settlementData["structures"][i]["name"]]

        """settlementData["structures"][i]["position"] = [random.randint(0, 256), 0, random.randint(0, 256)]
        settlementData["structures"][i]["flip"] = 0
        settlementData["structures"][i]["rotation"] = 0"""

        corners = structure.setupInfoAndGetCorners()
        result = floodFill.findPosHouse(corners)

        settlementData["structures"][i]["validPosition"] = result["validPosition"]

        settlementData["structures"][i]["position"] = result["position"]
        settlementData["structures"][i]["position"][1] -= 1

        settlementData["structures"][i]["flip"] = result["flip"]
        settlementData["structures"][i]["rotation"] = result["rotation"]
         
        settlementData["structures"][i]["prebuildingInfo"] = structure.getNextBuildingInformation(result["flip"], result["rotation"])

        # If new chunck discovererd, add new ressources
        chunk = [int(settlementData["structures"][i]["position"][0] / 16), int(settlementData["structures"][i]["position"][2] / 16)] 
        if not chunk in settlementData["discoveredChunk"] :
            structureBiomeId = _utils.getBiome(settlementData["structures"][i]["position"][0], settlementData["structures"][i]["position"][2], 1, 1)
            structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
            structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

            settlementData["discoveredChunk"].append(chunk)
            _utils.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

        loremaker.alterSettlementDataWithNewStructures(settlementData, i)
        structureMananager.checkDependencies()

    # Murderer
    settlementData["murdererIndex"] = choice([i for i in range(0, len(settlementData["villagerNames"])) if settlementData["villagerProfession"][i] != "Mayor"])
    settlementData["murdererTargetIndex"] = choice([i for i in range(0, len(settlementData["villagerNames"])) if i != settlementData["murdererIndex"]])

    books = generator.generateBooks(settlementData)
    generator.placeBooks(settlementData, books, floodFill, worldModif)
    
    # Add books replacements
    settlementData["materialsReplacement"]["villageBook"] = books["villageNameBook"]
    settlementData["materialsReplacement"]["villagerRegistry"] = books["villagerNamesList"]
    settlementData["materialsReplacement"]["deadVillagerRegistry"] = books["deadVillagersBook"]
    
    # Creates roads
    road.initRoad(floodFill, settlementData, worldModif, settlementData["materialsReplacement"])

    #structureMananager.printStructureChoose()

    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        generator.generateStructure(settlementData["structures"][i], settlementData, resources, worldModif, chestGeneration)
        #_utils.spawnVillagerForStructure(settlementData, settlementData["structures"][i], settlementData["structures"][i]["position"])
    worldModif.saveToFile(file)  

else : 
    if args.remove == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(args.remove)
    worldModif.undoAllModification()


milliseconds2 = int(round(time.time() * 1000))
result = milliseconds2 - milliseconds 

print("Time took : ", result / 1000)