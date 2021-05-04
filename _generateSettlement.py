from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
from _structureManager import *
import sys
import _resourcesLoader as resLoader
import random

file = "temp.txt"
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)

if len(sys.argv) <= 1 :
    resources = Resources()
    resLoader.loadAllResources(resources)
    settlementData = {}
    settlementData["center"] = [0, 63, 0]
    settlementData["size"] = [250, 250]
    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    settlementData["villageName"] = generateVillageName()

    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = []
    settlementData["villagerGameProfession"] = []
    settlementData["villagerProfessionList"] = [
                "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]
    
    settlementData["structuresNumberGoal"] = random.randint(5, 20)

    #structures contains "position", "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0
    
    # generate random village name
    settlementData["villageName"] = generateVillageName()
    print("Here's a random village name: ")

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    structureMananager = StructureManager(settlementData, resources)

    for i in range(settlementData["structuresNumberGoal"]) : 
        settlementData["structures"].append({})
        structureMananager.chooseOneStructure()
        structure = resources.buildings[settlementData["structures"][i]["name"]]
        print(structure.getCornersLocalPositions(structure.info["mainEntry"]["position"], 0, 0))
        # TODO 
        # settlementData["structures"][i]["position"] = 
        structureMananager.checkDependencies()
    
    print(settlementData)

    strVillagers = "List of all villagers: "

    for i in range(len(settlementData["villagerNames"])):
        # get a random level for the profession of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
        randomProfessionLevel = rd.randint(2, 5)
         
        strVillagers += settlementData["villagerNames"][i] + ":" + settlementData["villagerProfession"][i] + " "
        """spawnVillager(-12, 63, -177, "minecraft:villager", 
            settlementData["villagerNames"][i], settlementData["villagerGameProfession"][i], randomProfessionLevel, settlementData["biomeName"])"""

    # Create some books
    villageNameBook = makeBookItem("Welcome to " + settlementData["villageName"], title="Village Name")
    villagersBook = makeBookItem(strVillagers, title="List of all villagers")
    deadVillagersBook = makeBookItem("List of all dead villagers : ", title="List of all dead villagers")


    # Build after every computations
    for i in range(len(settlementData["structures"])) :
        structure = resources.buildings[settlementData["structures"][i]["name"]]

        info = structure.info
        buildingCondition = Buildings.BUILDINGS_CONDITIONS.copy()
        buildingCondition["rotation"] = 0
        buildingCondition["flip"] = 0
        buildingCondition["position"] = [-80, 63, 0]
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

        #resources.buildings[structure].build(worldModif, buildingCondition, chestGeneration)

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()

