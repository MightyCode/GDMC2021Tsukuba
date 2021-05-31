import time
milliseconds = int(round(time.time() * 1000))

from generation.resources import *
from generation.chestGeneration import *
from generation.structureManager import *
from generation.floodFill import *
import generation.generator as generator
import generation.resourcesLoader as resLoader
import utils.util as util
from utils.worldModification import *
import utils.argumentParser as argParser
import generation.loremaker as loremaker
import generation.road as road
import lib.interfaceUtils as iu
import lib.toolbox as toolbox
from random import choice


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

area = (area[0], area[1], area[2], area[3] - 1, area[4] - 1, area[5] - 1)
    
# Three main steps : choose structures and find its positions, make road between these structures, and finaly build structures.
if not args.remove:
    
    resources = Resources()
    resLoader.loadAllResources(resources)

    chestGeneration = ChestGeneration(resources, interface)
    iu.makeGlobalSlice()
    
    settlementData = generator.createSettlementData(area, resources)

    floodFill = FloodFill(worldModif, area, settlementData["structuresNumberGoal"])

    structureMananager = StructureManager(settlementData, resources)

    i = 0
    while i < settlementData["structuresNumberGoal"] : 
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
        
        if not result["validPosition"]:
            settlementData["structuresNumberGoal"] -= 1 
            structureMananager.removeLastStructure()
            floodFill.setNumberHouse(settlementData["structuresNumberGoal"])
            continue

        settlementData["structures"][i]["validPosition"] = result["validPosition"]

        settlementData["structures"][i]["position"] = result["position"]
        settlementData["structures"][i]["flip"] = result["flip"]
        settlementData["structures"][i]["rotation"] = result["rotation"]
         
        settlementData["structures"][i]["prebuildingInfo"] = structure.getNextBuildingInformation(result["flip"], result["rotation"])

        # If new chunck discovererd, add new ressources
        chunk = [int(settlementData["structures"][i]["position"][0] / 16), int(settlementData["structures"][i]["position"][2] / 16)] 
        if not chunk in settlementData["discoveredChunk"] :
            structureBiomeId = util.getBiome(settlementData["structures"][i]["position"][0], settlementData["structures"][i]["position"][2], 1, 1)
            structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
            structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

            settlementData["discoveredChunk"].append(chunk)
            util.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

        loremaker.alterSettlementDataWithNewStructures(settlementData, i)
        structureMananager.checkDependencies()
        i += 1

    # Murderer
    settlementData["murdererIndex"] = choice([i for i in range(0, len(settlementData["villagerNames"])) if settlementData["villagerProfession"][i] != "Mayor"])
    settlementData["murdererTargetIndex"] = choice([i for i in range(0, len(settlementData["villagerNames"])) if i != settlementData["murdererIndex"]])
    for structureData in settlementData["structures"]:
        if settlementData["murdererTargetIndex"] in structureData["villagersId"]:
            structureData["gift"] = "minecraft:tnt"

    books = generator.generateBooks(settlementData)
    generator.placeBooks(settlementData, books, floodFill, worldModif)

    # Villager interaction
    for i in range(len(settlementData["villagerNames"])):
        settlementData["villagerDiary"].append([])
        
        available = True
        for structureData in settlementData["structures"]:
            if i in structureData["villagersId"]:
                available = not "haybale" in structureData["name"]
                break

        if random.randint(1, 3) == 1 and available:
            print("Genere diary of " + settlementData["villagerNames"][i])
            settlementData["villagerDiary"][i] = book.createBookForVillager(settlementData, i)
            settlementData["villagerDiary"][i][0] = "minecraft:written_book" + toolbox.writeBook(settlementData["villagerDiary"][i][0], 
                title="Diary of " + settlementData["villagerNames"][i], author=settlementData["villagerNames"][i], description="Diary of " + settlementData["villagerNames"][i])
            if settlementData["villagerDiary"][i][1] != "":
                structureData["gift"] = settlementData["villagerDiary"][i][1]
    
    # Add books replacements
    settlementData["materialsReplacement"]["villageBook"] = "minecraft:written_book" + books["villageNameBook"]
    settlementData["materialsReplacement"]["villageLecternBook"] = books["villageNameBook"]
    settlementData["materialsReplacement"]["villagerRegistry"] = "minecraft:written_book" + books["villagerNamesBook"]
    settlementData["materialsReplacement"]["deadVillagerRegistry"] = "minecraft:written_book" + books["deadVillagersBook"]
    
    # Creates roads
    road.initRoad(floodFill, settlementData, worldModif, settlementData["materialsReplacement"])

    #structureMananager.printStructureChoose()

    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        generator.generateStructure(settlementData["structures"][i], settlementData, resources, worldModif, chestGeneration)
        #util.spawnVillagerForStructure(settlementData, settlementData["structures"][i], settlementData["structures"][i]["position"])
    worldModif.saveToFile(file)  
    
    floodFill.placeDecorations(settlementData["materialsReplacement"])

else : 
    if args.remove == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(args.remove)
    worldModif.undoAllModification()


milliseconds2 = int(round(time.time() * 1000))
result = milliseconds2 - milliseconds 

print("Time took : ", result / 1000)