import utils._utils as utils
from generation.structures.baseStructure import * 

class GeneratedWell(BaseStructure):
    def __init__(self) :
        super(BaseStructure, self).__init__()

    
    def getNextBuildingInformation(self):
        info = {}
        self.setSize([2, 10, 2])
        info["size"] = self.size
        self.info["mainEntry"]["position"] = [int(self.size[0] / 2), self.size[1] - 5, 0]
        self.info["mainEntry"]["facing"] = "north"
        info["entry"] = { "position" : self.info["mainEntry"]["position"], "facing" : "north" }

        info["corners"] = self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])

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
        
        fromBlock = self.returnWorldPosition([1, 0, 1], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
        toBlock = self.returnWorldPosition([self.size_x() - 2, self.size_y() - 1 , self.size_z() - 2], buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])

        worldModif.fillBlocks(fromBlock[0], fromBlock[1], fromBlock[2], toBlock[0], toBlock[1], toBlock[2], "minecraft:air")
        position = self.returnWorldPosition(
                        [self.entry[0], self.entry[1] - 1, self.entry[2]],
                        buildingCondition["flip"], buildingCondition["rotation"], buildingCondition["referencePoint"],
                        buildingCondition["position"])
        # Add water
        for i in range(2):
            for j in range(2):
                worldModif.setBlock(position[0] - i, position[1], position[2] - j, "minecraft:water")

        self.addStoneBricks(worldModif, buildingCondition)
        self.addStoneBrickStairs(worldModif, buildingCondition)
        self.addWoodAroundTheWell(worldModif, buildingCondition)


        
    def addWoodAroundTheWell(self, worldModif, buildingCondition):
        positions =[[ 0,-2], [1,-2], [3, 0], [3,1], [1,3], [0,3], [-2,0], [-2,1], [-2, -1], [3, -1], [3, 2], [-2, 2],
                    [-1, -2], [2, -2], [2, 3], [-1, 3], [-2, -2], [3, -2], [3, 3], [-2, 3]]

        # Add wood plank
        for i in range(len(positions)):
            localPosition = [positions[i][0], int(self.size_y()/2) - 1, positions[i][1]] 
            position = self.returnWorldPosition(
                        localPosition, buildingCondition["flip"], 
                        buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], self.plankType)
            
         

    def addStoneBrickStairs(self, worldModif, buildingCondition):
        # Add stairs
        positions = [[0,-1], [1,-1], [2,0], [2,1], [1,2], [0,2], [-1,0], [-1,1]]
        orientations = ["south", "south", "west", "west", "north", "north", "east", "east"]
        for i in range(len(positions)):
            localPosition = positions[i][0], int(self.size_y()/2), positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"])
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:stone_brick_stairs[" + self.convertProperty('facing', orientations[i] )  + "]")
            for j in range(1, 3):
                worldModif.setBlock(position[0], position[1] + 3, position[2], "minecraft:stone_brick_slab")

    def addStoneBricks(self, worldModif, buildingCondition):
        # Add stones to the corner
        positions = [[-1, -1], [2, -1], [2, 2], [-1, 2]]
        for i in range(len(positions)):
            localPosition = positions[i][0], int(self.size_y()/2), positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"]) 
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:infested_chiseled_stone_bricks")
            for j in range(1, 3):
                # Add cobblestone walls
                worldModif.setBlock(position[0], position[1] + j, position[2], "minecraft:cobblestone_wall")
            # Add stone brick slabs
            worldModif.setBlock(position[0], position[1] + j + 1, position[2], "minecraft:stone_brick_slab")  
            
        # Add stones upside the well    
        positions = [[0, 0], [0, 1], [1, 1], [1, 0]]
        for i in range(len(positions)):
            localPosition = positions[i][0], int(self.size_y() - 2), positions[i][1]
            position = self.returnWorldPosition(
                localPosition, buildingCondition["flip"], 
                buildingCondition["rotation"], buildingCondition["referencePoint"], buildingCondition["position"]) 
            worldModif.setBlock(position[0], position[1], position[2], "minecraft:infested_chiseled_stone_bricks")