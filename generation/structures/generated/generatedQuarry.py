import collections, numpy
import utils._utils as utils
import math
from generation.structures.baseStructure import * 

class GeneratedQuarry(BaseStructure):
    def __init__(self) :
        self.listOfBlocks = numpy.array([])
        self.size = [11, 11]

    def build(self, worldModif, buildingCondition, chestGeneration):
        self.listOfBlocks = numpy.array([[]])
        ## Building the quarry.
        for dy in range(11):
            for dx in range(11):
                for dz in range(11):
                    # Get all the block we chunk
                    block = worldModif.interface.getBlock(buildingCondition["position"][0] + dx, buildingCondition["position"][1] - dy, buildingCondition["position"][2] + dz)
                    if block != "minecraft:air" and block != "minecraft:cave_air":
                        self.listOfBlocks = numpy.append(self.listOfBlocks, block)   
        # Fill the area with air block           
        worldModif.fillBlocks(buildingCondition["position"][0], buildingCondition["position"][1], buildingCondition["position"][2], buildingCondition["position"][0] + dx, buildingCondition["position"][1] - dy, buildingCondition["position"][2] + dz, "minecraft:air")
        # Set a chest
        worldModif.interface.setBlock(buildingCondition["position"][0] + 5, buildingCondition["position"][1] + 1, buildingCondition["position"][2] - 2, "minecraft:chest")
        # Add the items to the chests
        counter = collections.Counter(self.listOfBlocks)
        items = counter.items()
        itemsList = []
        for i in items:
            # If there is more than one stack of block (64)
            if i[1] > 64:
                x = i[1]/64
                y = math.floor(x)
                for z in range(0, y):
                    newList = []
                    newList.append(i[0])
                    newList.append(64)
                    itemsList.append(newList)
            else:
                sublist = []
                sublist.append(i[0])
                sublist.append(i[1])
                itemsList.append(sublist)
        utils.addItemChest(buildingCondition["position"][0] + 5, buildingCondition["position"][1] + 1, buildingCondition["position"][2] - 2, itemsList)
        print(itemsList)
        print("Done")
