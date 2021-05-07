import collections, numpy
from generation.structures.baseStructure import * 

class GeneratedQuarry(BaseStructure):
    def __init__(self) :
        self.listOfBlocks = numpy.array([])

    def build(self, worldModif, buildingCondition, chestGeneration):
        self.listOfBlocks = numpy.array([])
        ## Building the quarry.
        for dy in range(11):
            for dx in range(11):
                for dz in range(11):
                    block = worldModif.interface.getBlock(buildingCondition["position"][0] + dx, buildingCondition["position"][1] - dy, buildingCondition["position"][2] + dz)
                    listOfBlocks = numpy.append(listOfBlocks, block)
                    worldModif.interface.setBlock(buildingCondition["position"][0] + dx,
                         buildingCondition["position"][1] - dy, buildingCondition["position"][2] + dz, "minecraft:air")
        worldModif.interface.sendBlocks()

        print(collections.Counter(listOfBlocks))
        print("Done")
