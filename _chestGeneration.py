import random
import interfaceUtils

class ChestGeneration:
    def __init__(self, resources, interface):
        self.resources = resources
        self.interface = interface
    
    def generate(self, x, y, z, lootTableName):
        lootTable = self.resources.lootTables[lootTableName]["pools"][0]
        numberItem = 0
        if isinstance(lootTable["rolls"], dict):
            numberItem = random.randint(lootTable["rolls"]["min"], lootTable["rolls"]["max"])
        else : 
            numberItem = lootTable["rolls"]

        itemPlaces = self.generatePlaces(numberItem)
        itemPlaces.sort()
        items = []

        sumWeight = 0
        for item in lootTable["entries"]:
            sumWeight += item["weight"]
        
        for i in range(len(itemPlaces)):
            currentWeight = random.randint(0, sumWeight)

            for item in lootTable["entries"]:  
                currentWeight -= item["weight"]
                if currentWeight <= 0:
                    numberOfItem = 1

                    if "functions" in item.keys() :
                        if item["functions"][0]["function"] == "set_count":
                            numberOfItem = random.randint(item["functions"][0]["count"]["min"], 
                                                            item["functions"][0]["count"]["max"])

                    items.append([ item["name"], numberOfItem ])
                    break

        interfaceUtils.Interface.addItemChest(x, y, z, items, itemPlaces)


    def generatePlaces(self, number):
        places = list(range(28))
        if number > 13:
            for i in range(27 - number):
                index = random.randint(0, len(places)-1)
                del places[index]
            return places
        else :
            places_b = []
            for i in range(number) :
                index = random.randint(0, len(places)-1)
                places_b.append(places[index])
                del places[index]
            return places_b
     