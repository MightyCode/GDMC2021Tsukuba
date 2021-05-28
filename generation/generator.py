import utils._utils as _utils
import random
import copy
import lib.toolbox as toolbox
from generation.structures.baseStructure import BaseStructure
import generation.loremaker as loremaker

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

    loremaker.fillSettlementDataWitholor(settlementData, "white")

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
    strVillagers = settlementData["villagerNames"][0] + " : " + settlementData["villagerProfession"][0] + ";"
    for i in range(1, len(settlementData["villagerNames"])):
        strVillagers += settlementData["villagerNames"][i] + " : " + settlementData["villagerProfession"][i] + ";"
    listOfVillagers = strVillagers.split(";")

    textVillagersNames = _utils.createTextForVillagersNames(listOfVillagers)
    textDeadVillagers = _utils.createTextForDeadVillagers(listOfVillagers)
    settlementData["villagerDeadName"] = textDeadVillagers[2]
    textVillagePresentationBook = _utils.createTextOfPresentationVillage(settlementData["villageName"], 
                settlementData["structuresNumberGoal"], settlementData["structures"], textDeadVillagers[1], listOfVillagers)
    settlementData["textOfBooks"] = [textVillagersNames, textDeadVillagers]
    
    books = {}
    books["villageNameBook"] = toolbox.writeBook(textVillagePresentationBook, title="Village Presentation", author="Mayor", description="Presentation of the village")
    books["villagerNamesBook"] = toolbox.writeBook(textVillagersNames, title="List of all villagers", author="Mayor", description="List of all villagers")
    books["deadVillagersBook"] = toolbox.writeBook(textDeadVillagers[0], title="List of all dead villagers", author="Mayor", description="List of all dead villagers")

    return books


def placeBooks(settlementData, books, floodFill, worldModif):

    items = []
    for key in books.keys():
        items += [["minecraft:written_book" + books[key], 1]]

    # Set a chest for the books and place the books in the chest
    worldModif.setBlock(settlementData["center"][0], 
                        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]), 
                        settlementData["center"][2], "minecraft:chest[facing=east]", placeImmediately=True)
    _utils.addItemChest(settlementData["center"][0], 
                        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]),
                        settlementData["center"][2], items)


    # Set a lectern for the book of village presentation
    toolbox.placeLectern(
        settlementData["center"][0], 
        floodFill.getHeight(settlementData["center"][0], settlementData["center"][2]), 
        settlementData["center"][2] + 1, books["villageNameBook"], worldModif, 'east')


def generateStructure(structureData, settlementData, resources, worldModif, chestGeneration):
    print(structureData["name"])
    print(structureData["validPosition"])
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildMurdererCache = False
    
    buildingCondition = BaseStructure.createBuildingCondition() 
    for index in structureData["villagersId"]:
        if index == settlementData["murdererIndex"]:
            if "murdererTrap" in info["villageInfo"].keys():
                buildMurdererCache = True

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

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, structure, structureData["name"])

    structure.build(worldModif,  buildingCondition, chestGeneration)
    
    """_utils.spawnVillagerForStructure(settlementData, structureData,
        [structureData["position"][0], 
         structureData["position"][1] + 1, 
         structureData["position"][2]])"""

    if buildMurdererCache:
        buildMurdererHouse(structureData, settlementData, resources, worldModif, chestGeneration, buildingCondition)


def buildMurdererHouse(structureData, settlementData, resources, worldModif, chestGeneration, buildingCondition):
    print("Build a house hosting a murderer")
    structure = resources.structures[structureData["name"]]
    info = structure.info

    buildingCondition = copy.deepcopy(buildingCondition)
    buildingCondition["position"] = structure.returnWorldPosition(
            info["villageInfo"]["murdererTrap"], buildingCondition["flip"], buildingCondition["rotation"], 
             buildingCondition["referencePoint"], buildingCondition["position"])

    structureMurderer = resources.structures["murderercache"]
    buildingInfo = structureMurderer.setupInfoAndGetCorners()
    buildingCondition["flip"] = random.randint(0, 3)
    buildingCondition["rotation"] = random.randint(0, 3)
    buildingInfo = structureMurderer.getNextBuildingInformation( buildingCondition["flip"], buildingCondition["rotation"])
    buildingCondition["referencePoint"] = buildingInfo["entry"]["position"]
    buildingCondition["size"] = buildingInfo["size"]

    modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, structureMurderer, "murderercache")

    structureMurderer.build(worldModif, buildingCondition, chestGeneration)
    facing = structureMurderer.getFacingMainEntry(buildingCondition["flip"], buildingCondition["rotation"])

    # Generate murderer trap
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 2, buildingCondition["position"][2], "minecraft:ladder[facing=" + facing + "]")
    worldModif.setBlock(buildingCondition["position"][0], buildingCondition["position"][1] + 3, buildingCondition["position"][2], 
        "minecraft:" + buildingCondition["replacements"]["woodType"] + "_trapdoor[half=bottom,facing=" + facing  +"]")



def modifyBuildingConditionDependingOnStructure(buildingCondition, settlementData, structure, structureName):
    if structureName == "basicgraveyard":
        pass
    elif structure == "murdererCache":
        buildingCondition["special"] = { "sign" : ["Next target :", "", "", ""] }
        name = settlementData["villagerNames"][settlementData["murdererTargetIndex"]]
        _utils.parseVillagerNameInLines([name], buildingCondition["special"]["sign"], 1)