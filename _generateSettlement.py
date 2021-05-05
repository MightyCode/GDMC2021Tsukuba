from _worldModification import *
from _resources import *
from _chestGeneration import *
from _buildings import *
import _utils
from _structureManager import *
import sys
import _resourcesLoader as resLoader
import random
from worldLoader import WorldSlice

file = "temp.txt"
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
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

    settlementData = {}
    settlementData["center"] = [int((area[0] + area[2]) / 2) , 63, int((area[1] + area[3]) / 2)]
    settlementData["size"] = [area[0] - area[2], area[1] - area[3]]
    settlementData["discoveredChunk"] = []
    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    settlementData["villageName"] = _utils.generateVillageName()

    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = []
    settlementData["villagerGameProfession"] = []
    settlementData["villagerProfessionList"] = [
                "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]
    
    settlementData["structuresNumberGoal"] = random.randint(5, 20)

    #structures contains "position", "rotation", "flip" "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    structureMananager = StructureManager(settlementData, resources)

    for i in range(settlementData["structuresNumberGoal"]) : 
        settlementData["structures"].append({})
        structureMananager.chooseOneStructure()
        structure = resources.buildings[settlementData["structures"][i]["name"]]
        corners = structure.getCornersLocalPositions(structure.info["mainEntry"]["position"], 0, 0)
        settlementData["structures"][i]["flip"] = 0
        settlementData["structures"][i]["rotation"] = 0

        settlementData["structures"][i]["position"] = interface.findPosHouse(corners, ws)

        # If new chunck discovererd, add new ressources
        chunk = [int(settlementData["structures"][i]["position"][0] / 16), int(settlementData["structures"][i]["position"][2] / 16)] 
        if not chunk in settlementData["discoveredChunk"] :
            structureBiomeId = interfaceUtils.getBiome(settlementData["structures"][i]["position"][0], settlementData["structures"][i]["position"][2], 1, 1)
            structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
            structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

            settlementData["discoveredChunk"].append(chunk)
            _utils.addResourcesFromChunk(resources, settlementData, structureBiomeBlockId)

        structureMananager.checkDependencies()

    strVillagers = "List of all villagers: "

    for i in range(len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + ":" + settlementData["villagerProfession"][i] + " "


    # Create some books
    villageNameBook = _utils.makeBookItem("Welcome to " + settlementData["villageName"], title="Village Name")
    villagersBook = _utils.makeBookItem(strVillagers, title="List of all villagers")
    deadVillagersBook = _utils.makeBookItem("List of all dead villagers : ", title="List of all dead villagers")
    print(settlementData)

    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        structure = resources.buildings[settlementData["structures"][i]["name"]]
        info = structure.info
        buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
        buildingCondition["flip"] = settlementData["structures"][i]["flip"]
        buildingCondition["rotation"] = settlementData["structures"][i]["rotation"]
        buildingCondition["position"] = settlementData["structures"][i]["position"]
        buildingCondition["replaceAllAir"] = 0
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

        structure.build(worldModif, buildingCondition, chestGeneration)

        _utils.spawnVillagerForStructure(settlementData, settlementData["structures"][i], settlementData["structures"][i]["position"])

    worldModif.saveToFile(file)

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()

