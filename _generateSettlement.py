from _worldModification import *
from _resources import *
from _buildings import *
from _utils import *
import time
import sys
import _resourcesLoader as resLoader

file = "temp.txt"
interface = interfaceUtils.Interface()
resources = Resources()
worldModif = WorldModification(interface)

if len(sys.argv) <= 1 :
    resLoader.loadAllResources(resources)
    settlementData = {}
    settlementData["center"] = [0, 63, 0]
    settlementData["size"] = [250, 250]
    settlementData["biomeId"] = interface.getBiome(settlementData["center"][0], settlementData["center"][2], 1, 1) # TODO get mean
    settlementData["biomeName"] = resources.biomeMinecraftId[int(settlementData["biomeId"])]
    settlementData["biomeBlockId"] = str(resources.biomesBlockId[settlementData["biomeName"]])
    settlementData["villageName"] = generateVillageName()
    settlementData["villagerNames"] = []
    settlementData["villagerProfession"] = ["farmer", "fisherman", "shepherd", "fletcher", "librarian", "cartographer", "cleric", "armorer", "weaponsmith", "toolsmith", "butcher", "leatherworker", "mason", "nitwit"]

    villagerFirstNamesList = getFirstNamelist()
    firstName = getRandomVillagerNames(villagerFirstNamesList, NUMBER)
    villagerLastNamesList = getLastNamelist()
    lastName = getRandomVillagerNames(villagerLastNamesList, NUMBER)

    print("Here's a random village name: ")
    print(settlementData["villageName"])
    print("Here's some random villager names : ")
    strVillagers = "List of all villagers: "
    for i in range(NUMBER):
        # get a random profession for a villager
        randomProfession = rd.randint(0, len(settlementData["villagerProfession"]) - 1)
        # get a random level for the profession of the villager (2: Apprentice, 3: Journeyman, 4: Expert, 5: Master)
        randomProfessionLevel = rd.randint(2, 5)
        
        settlementData["villagerNames"].append(firstName[i] + " " + lastName[i]) 
        strVillagers += settlementData["villagerNames"][i] + ":" + settlementData["villagerProfession"][randomProfession] + " "
        spawnVillager(-12, 63, -177, "minecraft:villager", settlementData["villagerNames"][i], settlementData["villagerProfession"][randomProfession], randomProfessionLevel, settlementData["biomeName"])

    # Add chest
    interface.setBlock(-12, 63, -180, "minecraft:chest")
    # Create some books
    villageNameBook = makeBookItem("Welcome to " + settlementData["villageName"], title="Village Name")
    villagersBook = makeBookItem(strVillagers, title="List of all villagers")
    deadVillagersBook = makeBookItem("List of all dead villagers : ", title="List of all dead villagers")
    items = [[villageNameBook, 1], [villagersBook, 1], [deadVillagersBook, 1]]
    # Add chest with items
    addItemChest(-12, 63, -180, items)
    print(settlementData["villagerNames"])

else : 
    if sys.argv[1] == "r" :   
        worldModif.loadFromFile(file)
    else :
        worldModif.loadFromFile(sys.argv[1])
    worldModif.undoAllModification()
