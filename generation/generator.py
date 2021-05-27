import utils._utils as _utils
import random
import copy
import lib.toolbox as toolbox
from generation.structures.baseStructure import BaseStructure

def createSettlementData(area, resources):
    settlementData = {}
    settlementData["center"] = [int((area[0] + area[3]) / 2) , 82, int((area[2] + area[5]) / 2)]
    settlementData["size"] = [area[0] - area[2], area[1] - area[3]]
    settlementData["discoveredChunk"] = []

    # Materials replacement
    settlementData["materialsReplacement"] = {}

    # Biome 
    settlementData["biomeId"] = _utils.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    if settlementData["biomeBlockId"] == "-1": 
        print("Generation on biome block id -1")
        settlementData["biomeBlockId"] = "0"

    # Load replaceements for structure biome
    for aProperty in resources.biomesBlocks[settlementData["biomeBlockId"]]:
        if aProperty in resources.biomesBlocks["rules"]["village"]:
            settlementData["materialsReplacement"][aProperty] = resources.biomesBlocks[settlementData["biomeBlockId"]][aProperty]

    settlementData["villageName"] = _utils.generateVillageName()

    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = []
    settlementData["villagerGameProfession"] = []
    settlementData["villagerProfessionList"] = [
                "farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", 
                "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]
    
    settlementData["structuresNumberGoal"] = random.randint(15, 70)

    #structures contains "position", "rotation", "flip" "name", "type", "group" ->, "villagersId"
    settlementData["structures"] = []
    settlementData["freeVillager"] = 0

    settlementData["woodResources"] = 0
    settlementData["dirtResources"] = 0
    settlementData["stoneResources"] = 0

    return settlementData


def generateBooks(settlementData):
    # Create books for the village
    strVillagers = ""
    for i in range(len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + " : " + settlementData["villagerProfession"][i] + ";"
    listOfVillagers = strVillagers.split(";")
    listOfDeadVillagers = [i.split(':', 1)[0] for i in listOfVillagers]

    textVillagersNames = _utils.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = _utils.createTextForDeadVillagers(listOfDeadVillagers)
    textVillagePresentationBook = _utils.createTextOfPresentationVillage(settlementData["villageName"], settlementData["villagerNames"], 
                settlementData["structuresNumberGoal"], settlementData["structures"], textDeadVillagers[1])
    
    books = {}
    books["villageNameBook"] = toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor", description="Presentation of the village")
    books["villagerNamesList"] = toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor", description="List of all villagers")
    books["deadVillagersBook"] = toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor", description="List of all dead villagers")
   
    return books


def placeBooks(settlementData, books, floodFill, worldModif, ws):
    names = ["villageNameBook", "villagerNamesList", "deadVillagersBook"]
    for i in range(3):
        toolbox.placeLectern(
            settlementData["center"][0], 
            floodFill.getHeight(settlementData["center"][0], settlementData["center"][2], ws), 
            settlementData["center"][2] + i, books[names[i]], worldModif, 'east')


def generateStructure(structureData, settlementData, resources, worldModif, chestGeneration):
    print(structureData["name"])
    print(structureData["validPosition"])
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildMurdererCache = False
    
    buildingCondition = BaseStructure.createBuildingCondition() 
    for index in structureData["villagersId"]:
        """if index == structureData["murdererIndex"]:
            if "murderer" in info["villageInfo"].keys():
                buildMurdererCache = True"""

        buildingCondition["villager"].append(settlementData["villagerNames"][index])

    buildingCondition["flip"] = structureData["flip"]
    buildingCondition["rotation"] = structureData["rotation"]
    buildingCondition["position"] = structureData["position"]
    buildingCondition["replaceAllAir"] = 3
    buildingCondition["referencePoint"] = structureData["prebuildingInfo"]["entry"]["position"]
    buildingCondition["size"] = structureData["prebuildingInfo"]["size"]
    buildingCondition["prebuildingInfo"] = structureData["prebuildingInfo"]
    structureBiomeId = _utils.getBiome(buildingCondition["position"][0], buildingCondition["position"][2], 1, 1)
    structureBiomeName = resources.biomeMinecraftId[int(structureBiomeId)]
    structureBiomeBlockId = str(resources.biomesBlockId[structureBiomeName])

    if structureBiomeBlockId == "-1" :
        structureBiomeBlockId = settlementData["biomeBlockId"]    
    
    buildingCondition["replacements"] = copy.deepcopy(settlementData["materialsReplacement"])
    # Load block for structure biome
    for aProperty in resources.biomesBlocks[structureBiomeBlockId]:
        if aProperty in resources.biomesBlocks["rules"]["structure"]:
            buildingCondition["replacements"][aProperty] = resources.biomesBlocks[structureBiomeBlockId][aProperty]

    
    structure.build(worldModif, buildingCondition, chestGeneration)
    
    """_utils.spawnVillagerForStructure(settlementData, structureData,
        [structureData["position"][0], 
         structureData["position"][1] + 1, 
         structureData["position"][2]])"""