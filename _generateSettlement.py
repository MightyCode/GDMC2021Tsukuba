from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import generation._resourcesLoader as resLoader
import utils._utils as _utils
from utils._worldModification import *
from lib.worldLoader import WorldSlice
import utils.argumentParser as argParser
import random
import time
import lib.toolbox as toolbox

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
    ws = WorldSlice(area[0], area[2], area[3], area[5])
    floodFill = FloodFill(area)
    
    settlementData = {}
    settlementData["center"] = [int((area[0] + area[2]) / 2) , 82, int((area[1] + area[3]) / 2)]
    settlementData["size"] = [area[0] - area[2], area[1] - area[3]]
    settlementData["discoveredChunk"] = []

    settlementData["biomeId"] = _utils.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    if settlementData["biomeBlockId"] == "-1": 
        print("Generation on biome block id -1")
        settlementData["biomeBlockId"] = "0"

    settlementData["villageName"] = _utils.generateVillageName()

    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = []
    settlementData["villagerGameProfession"] = []
    settlementData["villagerProfessionList"] = [
                "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]
    
    settlementData["structuresNumberGoal"] = random.randint(15, 30)

    #structures contains "position", "rotation", "flip" "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

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
                
        settlementData["structures"][i]["prebuildingInfo"] = structure.getNextBuildingInformation()

        """settlementData["structures"][i]["position"] = [random.randint(0, 256), 0, random.randint(0, 256)]
        settlementData["structures"][i]["flip"] = 0
        settlementData["structures"][i]["rotation"] = 0"""

        result = floodFill.findPosHouse(settlementData["structures"][i]["prebuildingInfo"]["corners"], ws)

        settlementData["structures"][i]["validPosition"] = result["validPosition"]

        settlementData["structures"][i]["position"] = result["position"]
        settlementData["structures"][i]["position"][1] -= 1

        settlementData["structures"][i]["flip"] = result["flip"]
        settlementData["structures"][i]["rotation"] = result["rotation"]


        # If new chunck discovererd, add new ressources
        chunk = [int(settlementData["structures"][i]["position"][0] / 16), int(settlementData["structures"][i]["position"][2] / 16)] 
        if not chunk in settlementData["discoveredChunk"] :
            structureBiomeId = _utils.getBiome(settlementData["structures"][i]["position"][0], settlementData["structures"][i]["position"][2], 1, 1)
            structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
            structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

            settlementData["discoveredChunk"].append(chunk)
            _utils.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

        structureMananager.checkDependencies()

    strVillagers = ""
    for i in range(len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + " : " + settlementData["villagerProfession"][i] + ";"
    listOfVillagers = strVillagers.split(";")
    listOfDeadVillagers = [i.split(':', 1)[0] for i in listOfVillagers]

    textVillagersNames = _utils.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = _utils.createTextForDeadVillagers(listOfDeadVillagers)
    textVillagePresentationBook = _utils.createTextOfPresentationVillage(settlementData["villageName"], settlementData["villagerNames"], 
                settlementData["structuresNumberGoal"], settlementData["structures"], textDeadVillagers[1])
    
    villageNameBook = toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor", description="Presentation of the village")
    villagerNamesList = toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor", description="List of all villagers")
    deadVillagersBook = toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor", description="List of all dead villagers")

    print(settlementData["center"])
    books = [villageNameBook, villagerNamesList, deadVillagersBook]
    for i in range(3):
        toolbox.placeLectern(settlementData["center"][0], settlementData["center"][1], settlementData["center"][2] + i, books[i], worldModif, 'east')

    #structureMananager.printStructureChoose()

    # Build after every computationsr
    for i in range(len(settlementData["structures"])) :
        print(settlementData["structures"][i]["name"])
        print(settlementData["structures"][i]["validPosition"])

        structure = resources.structures[settlementData["structures"][i]["name"]]
        info = structure.info

        buildingCondition = Structures.BUILDING_CONDITIONS.copy()
        buildingCondition["flip"] = settlementData["structures"][i]["flip"]
        buildingCondition["rotation"] = settlementData["structures"][i]["rotation"]
        buildingCondition["position"] = settlementData["structures"][i]["position"]

        buildingCondition["replaceAllAir"] = 3
        buildingCondition["referencePoint"] = settlementData["structures"][i]["prebuildingInfo"]["entry"]["position"]
        buildingCondition["size"] = settlementData["structures"][i]["prebuildingInfo"]["size"]

        buildingCondition["prebuildingInfo"] = settlementData["structures"][i]["prebuildingInfo"]

        structureBiomeId = _utils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
        structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
        structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

        if structureBiomeBlockId == "-1" :
            structureBiomeBlockId = settlementData["biomeBlockId"]    
        
        # Load block for structure biome
        for aProperty in resources.biomesBlocks[settlementData["biomeBlockId"]]:
            if aProperty in resources.biomesBlocks["rules"]["village"]:
                buildingCondition["replacements"][aProperty] = resources.biomesBlocks[settlementData["biomeBlockId"]][aProperty]

        # Load block for structure biome
        for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
            if aProperty in resources.biomesBlocks["rules"]["structure"]:
                buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

        # Add books replacements
        buildingCondition["replacements"]["villageBook"] = villageNameBook
        buildingCondition["replacements"]["villagerRegistry"] = villagerNamesList
        buildingCondition["replacements"]["deadVillagerRegistry"] = deadVillagersBook

        structure.build(worldModif, buildingCondition, chestGeneration)
        time.sleep(0.3)
        _utils.spawnVillagerForStructure(settlementData, settlementData["structures"][i], settlementData["structures"][i]["position"])
    worldModif.saveToFile(file)  

else : 
    if args.remove == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(args.remove)
    worldModif.undoAllModification()

