import collections, numpy
import utils._utils as utils
import math
from generation.structures.baseStructure import * 

class GeneratedQuarry(BaseStructure):
    def __init__(self) :
        super(BaseStructure, self).__init__()
        self.listOfBlocks = numpy.array([])
        self.setSize([11, 13, 11])
        self.uselessBlocks = ["minecraft:air", "minecraft:cave_air", "minecraft:grass", "minecraft:tall_grass", "minecraft:poppy", "minecraft:water",
             "minecraft:lava", "minecraft:dead_bush", "minecraft:cactus", "minecraft:sugar_cane"]
        
    def build(self, worldModif, buildingCondition, chestGeneration):
        woodType = "*woodType*"
        result = utils.changeNameWithBalise(woodType, buildingCondition["replacements"])
        if result[0] >= 0:
            woodType = result[1]
        else :
            woodType = "oak"

        self.fenceType = "minecraft:" + woodType + "_fence"
        self.fenceGateType = self.fenceType + "_gate"
        
        cx = buildingCondition["position"][0]
        cy = buildingCondition["position"][1]
        cz = buildingCondition["position"][2]


        self.setSize([11, 13, 11])
        self.listOfBlocks = numpy.array([])
        ## Building the quarry.
        for dy in range(self.size_y()):
            for dx in range(self.size_x()):
                for dz in range(self.size_z()):
                    # Get all the block we chunk
                    block = worldModif.interface.getBlock(cx + dx, cy - dy, cz + dz)
                    if block not in self.uselessBlocks:
                        self.listOfBlocks = numpy.append(self.listOfBlocks, block)   

        utils
                        
        # Fill the area with air block  
        worldModif.fillBlocks(cx, cy, cz, cx + dx, cy - dy, cz + dz, "minecraft:air")
        # Add the fences
        GeneratedQuarry.addFencesToQuarry(self, worldModif, cx, cy, cz)
        # Add the fence gate and the ladders
        GeneratedQuarry.addFenceGateToQuarry(self, worldModif, cx, cy, cz)   
        # Add the items to the chests
        GeneratedQuarry.addChestToQuarry(self, worldModif, cx, cy, cz, self.listOfBlocks)
                      
        print("Done")
        
    def addChestToQuarry(self, worldModif, cx ,cy, cz, list):   
        # Set a chest
        worldModif.setBlock(cx+5, cy + 1, cz - 2, "minecraft:chest[facing=north]")
        counter = collections.Counter(list)
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
        utils.addItemChest(cx+5, cy+1, cz-2, itemsList)
        print(itemsList)
        
        
    def addFencesToQuarry(self, worldModif, cx, cy, cz):
        # Add the fences for the quarry
        worldModif.setBlock(cx-1, cy+1, cz-1, self.fenceType)
        
        # First line
        for i in range(self.size_x() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx+i, cy-y, cz-1)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if  block in self.uselessBlocks:
                    worldModif.setBlock(cx+i, cy-y, cz-1, self.fenceType)
            worldModif.setBlock(cx+i, cy+1, cz-1, self.fenceType)
            
        # Second line
        for j in range(self.size_z() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx+self.getSize()[0], cy-y, cz+j)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in self.uselessBlocks:
                    worldModif.setBlock(cx+self.size[0], cy-y, cz+j, self.fenceType)
            worldModif.setBlock(cx+self.size[0], cy+1, cz+j, self.fenceType)
            
        # Third line
        for k in range(self.size_x() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx-k+self.getSize()[0], cy-y, cz+self.getSize()[2])
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in self.uselessBlocks:
                    worldModif.setBlock(cx-k+self.size[0], cy-y, cz+self.size[2], self.fenceType)
            worldModif.setBlock(cx-k+self.size[0], cy+1, cz+self.size[2], self.fenceType)
            
        # Fourth line
        for l in range(self.size_z() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx-1, cy-y, cz+l)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in self.uselessBlocks:
                    worldModif.setBlock(cx-1, cy-y, cz+l, self.fenceType)
            worldModif.setBlock(cx-1, cy+1, cz+l, self.fenceType)
    
    
    def addFenceGateToQuarry(self, worldModif, cx, cy, cz):
        # Add the fence gate
        z = math.floor(self.size_z()/2)
        for y in range(self.size_y()):
            block = worldModif.interface.getBlock(cx-1, cy-y, cz+z)
            if block ==  self.fenceType:
                worldModif.setBlock(cx-1, cy-y, cz+z,  self.fenceGateType + "[facing=east]")
        worldModif.setBlock(cx-1, cy+1, cz+z, self.fenceGateType + "[facing=east]")
        
        # Set air around the fence gate
        worldModif.setBlock(cx-2, cy+1, cz+z, "minecraft:air")
        worldModif.setBlock(cx, cy+1, cz+z, "minecraft:air")
        worldModif.setBlock(cx-2, cy+2, cz+z, "minecraft:air")
        worldModif.setBlock(cx, cy+2, cz+z, "minecraft:air")
        
        
        # Add the ladders
        for ladder in range(self.size_y()):
            worldModif.setBlock(cx, cy-ladder, cz+z, "minecraft:ladder[facing=east]")
        
        print("Finish building : basicQuarry")
        