import random
import lib.interfaceUtils as interfaceUtils

class ChestGeneration:
    def __init__(self, resources, interface):
        self.resources = resources
        self.interface = interface
    
    def generate(self, x, y, z, lootTableName, changeItemName={}):
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

                # This item is choosen
                if currentWeight <= 0:
                    numberOfItem = 1

                    # Compute number of items
                    if "functions" in item.keys() :
                        if item["functions"][0]["function"] == "set_count":
                            numberOfItem = random.randint(item["functions"][0]["count"]["min"], 
                                                            item["functions"][0]["count"]["max"])
                    
                    # Compute item's name if balise *, means that one word should change
                    index = item["name"].find("*")
                    if index != -1 :
                        secondIndex = item["name"].find("*", index+1)
                        word = item["name"][index +1 : secondIndex]
                        added = False
                        for key in changeItemName.keys():
                            if key == word:
                                added = True
                                items.append([ item["name"].replace("*" + word + "*", changeItemName[key]), numberOfItem ])
                                break
                        
                         # If the balise can't be replace
                        if not added:
                            items.append([ "", 0 ])
                    else :
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
     