import collections, numpy
import utils._utils as utils
import math
from generation.structures.baseStructure import * 

class GeneratedQuarry(BaseStructure):
    def __init__(self) :
        super(BaseStructure, self).__init__()
        self.listOfBlocks = numpy.array([])
        self.setSize([11, 11, 11])

    def build(self, worldModif, buildingCondition, chestGeneration):
        cx = buildingCondition["position"][0]
        cy = buildingCondition["position"][1]
        cz = buildingCondition["position"][2]
        self.listOfBlocks = numpy.array([])
        self.setSize([11, 11, 11])
        uselessBlocks = ["minecraft:air", "minecraft:cave_air", "minecraft:grass", "minecraft:tall_grass", "minecraft:poppy", "minecraft:water", "minecraft:lava", "minecraft:dead_bush", "minecraft:cactus", "minecraft:sugar_cane"]
        ## Building the quarry.
        for dy in range(self.size_y()):
            for dx in range(self.size_x()):
                for dz in range(self.size_z()):
                    # Get all the block we chunk
                    block = worldModif.interface.getBlock(cx + dx, cy - dy, cz + dz)
                    if block != "minecraft:air" and block != "minecraft:cave_air":
                        self.listOfBlocks = numpy.append(self.listOfBlocks, block)         
        # Fill the area with air block           
        worldModif.fillBlocks(cx, cy, cz, cx+dx, cy-dy, cz+dz, "minecraft:air")
        # Set a chest
        worldModif.interface.setBlock(cx+5, cy + 1, cz - 2, "minecraft:chest")
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
        utils.addItemChest(cx+5, cy+1, cz-2, itemsList)
        print(itemsList)
        
        # Add the fences for the quarry
        worldModif.interface.setBlock(cx-1, cy+1, cz-1, "minecraft:oak_fence")
        
        # First line
        for i in range(self.size_x() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx+i, cy-y, cz-1)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if  block in uselessBlocks:
                    worldModif.interface.setBlock(cx+i, cy-y, cz-1, "minecraft:oak_fence")
            worldModif.interface.setBlock(cx+i, cy+1, cz-1, "minecraft:oak_fence")
            
        # Second line
        for j in range(self.size_z() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx+self.getSize()[0], cy-y, cz+j)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in uselessBlocks:
                    worldModif.interface.setBlock(cx+self.getSize()[0], cy-y, cz+j, "minecraft:oak_fence")
            worldModif.interface.setBlock(cx+self.getSize()[0], cy+1, cz+j, "minecraft:oak_fence")
            
        # Third line
        for k in range(self.size_x() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx-k+self.getSize()[0], cy-y, cz+self.getSize()[2])
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in uselessBlocks:
                    worldModif.interface.setBlock(cx-k+self.getSize()[0], cy-y, cz+self.getSize()[2], "minecraft:oak_fence")
            worldModif.interface.setBlock(cx-k+self.getSize()[0], cy+1, cz+self.getSize()[2], "minecraft:oak_fence")
            
        # Fourth line
        for l in range(self.size_z() + 1):
            for y in range(self.size_y()):
                block = worldModif.interface.getBlock(cx-1, cy-y, cz+l)
                # print(block)
                # Check if there is an useless block below so we can replace it with a fence
                if block in uselessBlocks:
                    worldModif.interface.setBlock(cx-1, cy-y, cz+l, "minecraft:oak_fence")
            worldModif.interface.setBlock(cx-1, cy+1, cz+l, "minecraft:oak_fence")
            
        # Add the fence gate
        z = math.floor(self.size_z()/2)
        for y in range(self.size_y()):
            block = worldModif.interface.getBlock(cx-1, cy-y, cz+z)
            if block == "minecraft:oak_fence":
                worldModif.interface.setBlock(cx-1, cy-y, cz+z, "minecraft:oak_fence_gate[facing=east]")
        worldModif.interface.setBlock(cx-1, cy+1, cz+z, "minecraft:oak_fence_gate[facing=east]")
        
        # Set air around the fence gate
        worldModif.interface.setBlock(cx-2, cy+1, cz+z, "minecraft:air")
        worldModif.interface.setBlock(cx, cy+1, cz+z, "minecraft:air")
        worldModif.interface.setBlock(cx-2, cy+2, cz+z, "minecraft:air")
        worldModif.interface.setBlock(cx, cy+2, cz+z, "minecraft:air")
        
        
        # Add the ladders
        for ladder in range(self.size_y()):
            worldModif.interface.setBlock(cx, cy-ladder, cz+z, "minecraft:ladder[facing=east]")
        
        print("Finish building : basicQuarry")
        