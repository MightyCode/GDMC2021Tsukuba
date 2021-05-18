from generation._resources import *
from generation._chestGeneration import *
from generation.structures.structures import *
from generation._structureManager import *
from generation._floodFill import *
import _bookGeneration
import generation._resourcesLoader as resLoader
import utils._utils as _utils
from utils._worldModification import *
from lib.worldLoader import WorldSlice
import random
import sys
import time

file = "temp.txt"
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
size = str(150)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-" + size + " 0 ~-" + size +  "~" + size + " 255 ~" + size)
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
    ws = WorldSlice(area)
    floodFill = FloodFill()
    
    settlementData = {}
    settlementData["center"] = [int((area[0] + area[2]) / 2) , 70, int((area[1] + area[3]) / 2)]
    settlementData["size"] = [area[0] - area[2], area[1] - area[3]]
    settlementData["discoveredChunk"] = []

    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
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
    
    settlementData["structuresNumberGoal"] = random.randint(15, 50)

    #structures contains "position", "rotation", "flip" "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    structureMananager = StructureManager(settlementData, resources)

    for i in range(settlementData["structuresNumberGoal"]) : 
        settlementData["structures"].append({})
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
        corners = structure.getCornersLocalPositionsAllFlipRotation(structure.info["mainEntry"]["position"])

        settlementData["structures"][i]["position"] = [random.randint(0, 256), 0, random.randint(0, 256)]
        settlementData["structures"][i]["flip"] = 0
        settlementData["structures"][i]["rotation"] = 0 

        result = floodFill.findPosHouse(corners, ws)

        settlementData["structures"][i]["position"] = result["position"]
        settlementData["structures"][i]["position"][1] -= 1
        settlementData["structures"][i]["flip"] = result["flip"]
        settlementData["structures"][i]["rotation"] = result["rotation"]

        # If new chunck discovererd, add new ressources
        chunk = [int(settlementData["structures"][i]["position"][0] / 16), int(settlementData["structures"][i]["position"][2] / 16)] 
        if not chunk in settlementData["discoveredChunk"] :
            structureBiomeId = interfaceUtils.getBiome(settlementData["structures"][i]["position"][0], settlementData["structures"][i]["position"][2], 1, 1)
            structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
            structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

            settlementData["discoveredChunk"].append(chunk)
            _utils.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

        structureMananager.checkDependencies()

    strVillagers = ""
    for i in range(len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + " : " + settlementData["villagerProfession"][i] + ";"
    listOfVillagers = strVillagers.split(";")
    print (listOfVillagers)

    # Create some books
    textVillageName = ('\f\\\\s--------------\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|   Welcome to      |\\\\n'
           f'| {settlementData["villageName"]} |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|                      |\\\\n'
            '|--------------')
    textVillagerNames = ('\f\\\\s-----------------\\\\n')
    for i in range(len(listOfVillagers)):
        if i <= 6: 
            textVillagerNames += (f'{listOfVillagers[i]}       \\\\n')
        if i == 6 or i == 12 or i == 18:
            textVillagerNames += ('-----------------\\\\n\f')
        if i > 6:
            textVillagerNames += (f'{listOfVillagers[i]}       \\\\n')
    textVillagerNames += ('-----------------\\\\n\f')

        
    villageNameBook = _bookGeneration.writeBook(textVillageName, title="Village Name", author="Yusuf", description="Presentation of the village")
    villagersBook = _bookGeneration.writeBook(textVillagerNames, title="Villagers Names", author="Yusuf", description="Name and Job of all the villagers")
    deadVillagersBook = _utils.makeBookItem("List of all dead villagers : ", title="List of all dead villagers")
    print(settlementData)
    
    #_bookGeneration.placeLectern(settlementData["center"][0], settlementData["center"][1], settlementData["center"][2], villageNameBook, worldModif, 'east')
    #_bookGeneration.placeLectern(settlementData["center"][0], settlementData["center"][1], settlementData["center"][2] + 1, villagersBook, worldModif, 'east')
    print("")
    #structureMananager.printStructureChoose()

    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        print(settlementData["structures"][i]["name"])
        structure = resources.structures[settlementData["structures"][i]["name"]]
        info = structure.info
        buildingCondition = Structures.BUILDING_CONDITIONS.copy()
        buildingCondition["flip"] = settlementData["structures"][i]["flip"]
        buildingCondition["rotation"] = settlementData["structures"][i]["rotation"]
        buildingCondition["position"] = settlementData["structures"][i]["position"]
        buildingCondition["replaceAllAir"] = 3
        buildingCondition["referencePoint"] = [info["mainEntry"]["position"][0], info["mainEntry"]["position"][1], info["mainEntry"]["position"][2]]

        structureBiomeId = interfaceUtils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
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
        buildingCondition["replacements"]["villagerRegistry"] = villagersBook
        buildingCondition["replacements"]["deadVillagerRegistry"] = deadVillagersBook

        #structure.build(worldModif, buildingCondition, chestGeneration)
        
        #_utils.spawnVillagerForStructure(settlementData, settlementData["structures"][i], settlementData["structures"][i]["position"])
        time.sleep(0)
    #worldModif.saveToFile(file)  
    

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()

