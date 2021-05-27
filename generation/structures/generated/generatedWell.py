import utils._utils as utils
from generation.structures.baseStructure import * 

class GeneratedWell(BaseStructure):
    def __init__(self) :
        super(BaseStructure, self).__init__()


    def setupInfoAndGetCorners(self):
        self.setSize([6, 9, 6])
        self.info["mainEntry"]["position"] = [int(self.size[0] / 2), self.size[1] - 5, 0]
        return self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])
    

    def getNextBuildingInformation(self, flip, rotation):
        info = {}
        info["size"] = self.size
        self.info["mainEntry"]["facing"] = "north"
        info["entry"] = { 
            "position" : self.info["mainEntry"]["position"], 
            "facing" : self.getFacingMainEntry(flip, rotation) 
        }

        return info


    def build(self, worldModif, buildingCondition, chestGeneration):
        self.setSize(buildingCondition["size"])
        self.entry = buildingCondition["referencePoint"].copy()
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - 1 - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][2] = self.size[2] - 1 - buildingCondition["referencePoint"][2] 
            
        woodType = "*woodType*"
        result = utils.changeNameWithBalise(woodType, buildingCondition["replacements"])
        if result[0] >= 0:
            woodType = result[1]
        else :
            woodType = "oak"
        
        self.plankType = "minecraft:" + woodType + "_planks"
    
        # Add water
        fromBlock = self.returnWorldPosition(
                        [2, int(self.size_y()), 2], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])

        toBlock =  self.returnWorldPosition(
                        [3, int(self.size_y()), 3], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])              

        worldModif.fillBlocks(fromBlock[0], fromBlock[1] - 3, fromBlock[2], toBlock[0], toBlock[1]- 7, toBlock[2],"minecraft:air")
        worldModif.fillBlocks(fromBlock[0], fromBlock[1] - 6, fromBlock[2], toBlock[0], toBlock[1] - 5, toBlock[2], "minecraft:water")

        self.addStoneBricks(worldModif, buildingCondition)
        self.addStoneBrickStairs(worldModif, buildingCondition)
        self.addWoodAroundTheWell(worldModif, buildingCondition)

        
    def addWoodAroundTheWell(self, worldModif, buildingCondition):
        positions = [[0, 0], [1, 0], [2, 0], [3, 0], [4, 0], [5, 0], [1, 5], [2, 5], [3, 5], [4, 5], [5, 5], 
        [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [5, 1], [5, 2], [5, 3], [5, 4]]
        # Add wood plank
        for i in range(len(positions)):
            localPosition = [positions[i][0], self.size_y() - 5, positions[i][1]] 
            position = self.returnWorldPosition(
                        localPosition, buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], self.plankType)
            
         

    def addStoneBrickStairs(self, worldModif, buildingCondition):
        # Add stairs
        positions = [[2, 4], [3, 4], [1, 2], [1, 3], [2, 1], [3, 1], [4, 2], [4, 3]]
        orientations = ["north", "north", "east", "east", "south", "south", "west", "west"]
        for i in range(len(positions)):
            localPosition = positions[i][0],  self.size_y() - 4, positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:stone_brick_stairs[" + self.convertProperty('facing', orientations[i] )  + "]")
            for j in range(1, 3):
                worldModif.setBlock(position[0], position[1] + 3, position[2], "minecraft:stone_brick_slab")

    def addStoneBricks(self, worldModif, buildingCondition):
        # Add stones to the corner
        positions = [[1, 1], [1, 4], [4, 1], [4, 4]]
        for i in range(len(positions)):
            localPosition = positions[i][0], self.size_y() - 4, positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"]) 
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:chiseled_stone_bricks")
            for j in range(1, 3):
                # Add cobblestone walls
                worldModif.setBlock(position[0], position[1] + j, position[2], "minecraft:cobblestone_wall")
            # Add stone brick slabs
            worldModif.setBlock(position[0], position[1] + j + 1, position[2], "minecraft:stone_brick_slab")  
            
        # Add stones upside the well    
        positions = [[2, 2], [2, 3], [3, 2], [3, 3]]
        for i in range(len(positions)):
            localPosition = positions[i][0], self.size_y() - 1 , positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"]) 
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:chiseled_stone_bricks")