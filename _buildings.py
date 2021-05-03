import _math
import math
import _utils
from nbt import nbt

class Buildings:
    REPLACEMENTS = "replacements"
    CHANGE = "Change"
    CHANGE_TO = "ChangeTo"
    CHANGE_STATE = "ChangeState"
    CHANGE_ORIGINAL_BLOCK = "OriginalBlock"
    CHANGE_REPLACEMENT_WORD = "ReplacementWord"
    CHANGE_EXCLUDED_ZONES = ""

    AIR_BLOCK = "minecraft:air"

    ORIENTATIONS = ["west", "north" , "east", "south"]

    REPLACEMENTS_EXCLUSIF = {
        "oak" : "dark_oak"
    }

    """
    Flip is applied before rotation

    flip : No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    rotation : No rotation = 0, rotation 90 = 1, rotation 180 = 2, rotation 270 = 3
    replaceAllAir : 0 no air placed, 1 place all air block, 2 place all choosen air block, 3 take the prefered replacement air from info file
    position : the center of the contruction
    referencePoint : point x, z where the building will rotate around, the block at the reference point will be on position point
    replacement : change one type of block to another
    """
    BUILDINGS_CONDITIONS =  {
        "rotation" : 0,
        "flip" : 0,
        "replaceAllAir" : 0,
        "position" : [0, 0, 0],
        "referencePoint" : [0, 0, 0],
        "replacements" : {},
    }

    def __init__(self, nbtfile, info, name):
        self.size = [nbtfile["size"][0].value, nbtfile["size"][1].value, nbtfile["size"][2].value]
        self.file = nbtfile
        self.info = info
        self.name = name

        self.computedOrientation = {}
        # Indicate for each block in palette if it should change or not and to change to what
        for block in self.file["palette"]:
            if Buildings.REPLACEMENTS in self.info.keys():
                blockName = block["Name"].value.split("[")[0]

                for replacementWord in self.info[Buildings.REPLACEMENTS].keys():
                    # Checking for block replacement
                    if blockName == replacementWord:
                        block.tags.append(nbt.TAG_Int(name=Buildings.CHANGE_STATE, value=self.info[Buildings.REPLACEMENTS][blockName]["state"]))
                                                                        #  """AND states equals"""
                        if block[Buildings.CHANGE_STATE].value == 1 or (block[Buildings.CHANGE_STATE].value == 0):
                            block.tags.append(nbt.TAG_Byte(name=Buildings.CHANGE, value=True))
                            block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_TO, value=self.info[Buildings.REPLACEMENTS][block["Name"].value]["type"]))   
                            block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_ORIGINAL_BLOCK, value=block["Name"].value))
                            block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_REPLACEMENT_WORD, value=replacementWord))
                            block.tags.append(nbt.TAG_Byte(name=Buildings.CHANGE_EXCLUDED_ZONES, 
                                value=("excluded" in self.info[Buildings.REPLACEMENTS][replacementWord].keys())))
                            break
                        
                    # Checking for substr replacement 
                    elif replacementWord in blockName:
                        # The replacementWord can be in unexpected blocks
                        # "oak" is on every "...dark_oak..." block
                        if replacementWord in Buildings.REPLACEMENTS_EXCLUSIF:
                            if Buildings.REPLACEMENTS_EXCLUSIF[replacementWord] in blockName:
                                continue

                        if replacementWord in self.info[Buildings.REPLACEMENTS].keys():
                            if self.info[Buildings.REPLACEMENTS][replacementWord]["state"] == 2:
                                block.tags.append(nbt.TAG_Byte(name=Buildings.CHANGE, value=True))
                                block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_TO, value=self.info[Buildings.REPLACEMENTS][replacementWord]["type"]))  
                                block.tags.append(nbt.TAG_Int(name=Buildings.CHANGE_STATE, value=2))
                                block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_ORIGINAL_BLOCK, value=(block["Name"].value) ))
                                block.tags.append(nbt.TAG_String(name=Buildings.CHANGE_REPLACEMENT_WORD, value=replacementWord))

                                # True or False
                                block.tags.append(nbt.TAG_Byte(name=Buildings.CHANGE_EXCLUDED_ZONES, 
                                    value=("excluded" in self.info[Buildings.REPLACEMENTS][replacementWord].keys())))
                                break
                                

            block.tags.append(nbt.TAG_Byte(name=Buildings.CHANGE, value=False))
        
        # Looting table
        self.lootTable = False
        if "lootTables" in self.info.keys():
            self.lootTable = len(self.info["lootTables"]) > 0


    def build(self, worldModif, buildingCondition, chestGeneration):
        ## Pre computing :
        print("Pre building : " + self.name)
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - 1 - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][2] = self.size[2] - 1 - buildingCondition["referencePoint"][2] 

        # Replace bloc by these given
        print("Prebuilding Palette")
        for blockPalette in self.file["palette"]:
            if blockPalette[Buildings.CHANGE].value:
                changeState = blockPalette[Buildings.CHANGE_STATE].value
                if changeState == 0 or changeState == 1:
                    blockPalette["Name"].value = buildingCondition["replacements"][blockPalette[Buildings.CHANGE_TO].value].split("[")[0]
                elif changeState == 2:
                    blockPalette["Name"].value = blockPalette[Buildings.CHANGE_ORIGINAL_BLOCK].value.replace(
                        blockPalette[Buildings.CHANGE_REPLACEMENT_WORD].value, buildingCondition["replacements"][blockPalette[Buildings.CHANGE_TO].value].split("[")[0] )

        # Air zone
        print("Prebuilding air")
        if buildingCondition["replaceAllAir"] == 3:
            buildingCondition["replaceAllAir"] = self.info["air"]["preferedAirMode"]

        if buildingCondition["replaceAllAir"] == 2:
            for zones in self.info["air"]["replacements"]:
                blockFrom = self.returnWorldPosition([ zones[0], zones[1], zones[2] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])
                blockTo   = self.returnWorldPosition([ zones[3], zones[4], zones[5] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])
                                                     
                worldModif.fillBlocks(blockFrom[0], blockFrom[1], blockFrom[2], blockTo[0], blockTo[1], blockTo[2], Buildings.AIR_BLOCK)

        print("Building : " + self.name)

        ## Computing : Modify from blocks
        for block in self.file["blocks"]:
            blockPalette = self.file["palette"][block["state"].value]

            # Check if the current block is in excluded zone
            takeOriginalBlock = False
            blockName = blockPalette["Name"].value
            if (blockPalette[Buildings.CHANGE].value):
                if (blockPalette[Buildings.CHANGE_EXCLUDED_ZONES].value):
                    for zone in self.info["replacements"][blockPalette[Buildings.CHANGE_REPLACEMENT_WORD].value]["excluded"] :
                        if _math.isPointInSquare([ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value], zone) :
                            print(blockPalette[Buildings.CHANGE_ORIGINAL_BLOCK].value)
                            takeOriginalBlock = True
                            blockName = blockPalette[Buildings.CHANGE_ORIGINAL_BLOCK].value
                            break

            # Check for block air replacement
            if blockName == Buildings.AIR_BLOCK and buildingCondition["replaceAllAir"] == 1:
                continue
            
            # Compute position of block from local space to world space
            blockPosition = self.returnWorldPosition(
                [ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value ],
                buildingCondition["flip"], buildingCondition["rotation"], 
                buildingCondition["referencePoint"], buildingCondition["position"] )
            
            worldModif.setBlock(
                blockPosition[0], blockPosition[1], blockPosition[2],
                self.convertNbtBlockToStr(
                    self.file["palette"][block["state"].value],
                    buildingCondition["rotation"],
                    buildingCondition["flip"],
                    takeOriginalBlock
                    ), 
            )

            # If structure has loot tables and chest encounter
            if "chest" in blockName:
                if self.lootTable :
                    choosenLootTable = ""
                    for lootTable in self.info["lootTables"] :
                        if len(lootTable) == 1:
                            choosenLootTable = lootTable[0]
                        elif _math.isPointInSquare([ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value ], lootTable[1]) :
                            choosenLootTable = lootTable[0]
                    
                    if choosenLootTable  != "":
                        chestGeneration.generate(blockPosition[0], blockPosition[1], blockPosition[2], choosenLootTable, buildingCondition["replacements"])

        print("Finish building : " + self.name)

    def returnWorldPosition(self, localPoint, flip, rotation, referencePoint, worldStructurePosition) :
        worldPosition = [0, 0, 0]
        
        # Position in building local spacereplacements
        if flip == 1 or flip == 3 :
            worldPosition[0] = self.size[0] - 1 - localPoint[0]
            worldPosition[2] = self.size[2] - 1 - localPoint[2]
        else : 
            worldPosition[0] = localPoint[0]
            worldPosition[2] = localPoint[2]

        worldPosition[1] = localPoint[1]

        # Take rotation into account, apply to building local positions
        worldPosition[0], worldPosition[2] = _math.rotatePointAround(
            [worldStructurePosition[0] + referencePoint[0], worldStructurePosition[2] + referencePoint[2]], 
            [worldStructurePosition[0] + worldPosition[0], worldStructurePosition[2] + worldPosition[2]], 
            rotation *  math.pi / 2)

        # Position in real world
        
        worldPosition[0] = int(worldPosition[0])                        - referencePoint[0]
        worldPosition[1] = worldStructurePosition[1] + worldPosition[1] - referencePoint[1] 
        worldPosition[2] = int(worldPosition[2])                        - referencePoint[2]
        return worldPosition 
    

    def convertNbtBlockToStr(self, blockPalette, rotation, flip, takeOriginalBlockName=False):
        block = "["
        if takeOriginalBlockName:
            block = blockPalette[Buildings.CHANGE_ORIGINAL_BLOCK].value + block
        else:
            block = blockPalette["Name"].value + block

        if "Properties" in blockPalette.keys():
            for key in blockPalette["Properties"].keys():
                block += self.convertProperty(key, blockPalette["Properties"][key].value, rotation, flip) + ","
  
            block = block[:-1] 
        block += "]"
        return block


    def convertProperty(self, propertyName, propertyValue, rotation, flip):
        if propertyValue in self.computedOrientation.keys():
            propertyValue = self.computedOrientation[propertyValue]

        return propertyName + "=" + propertyValue


    def computeOrientation(self, rotation, flip) :
        # Construct orientation
        self.computedOrientation = { 
            "left" : "left",
            "right" : "right",
            "x" : "x",
            "y" : "y",
            Buildings.ORIENTATIONS[0] : Buildings.ORIENTATIONS[0],
            Buildings.ORIENTATIONS[1] : Buildings.ORIENTATIONS[1],
            Buildings.ORIENTATIONS[2] : Buildings.ORIENTATIONS[2],
            Buildings.ORIENTATIONS[3] : Buildings.ORIENTATIONS[3]
        }
        
        # Apply flip to orientation
        if flip == 1 or flip == 3:
            self.computedOrientation["east"] = "west" 
            self.computedOrientation["west"] = "east"

            if flip != 3:
                self.computedOrientation["left"] = "right"
                self.computedOrientation["right"] = "left"
            
        if flip == 2 or flip == 3:
            self.computedOrientation["south"] = "north"
            self.computedOrientation["north"] = "south"


        # Apply rotation to orientation
        for orientation in self.computedOrientation.keys():
            if orientation in Buildings.ORIENTATIONS:
                self.computedOrientation[orientation] = Buildings.ORIENTATIONS[
                    (Buildings.ORIENTATIONS.index(self.computedOrientation[orientation]) + rotation) % len(Buildings.ORIENTATIONS)
                ]

        if rotation == 1 or rotation == 3:
            self.computedOrientation["x"] = "z"
            self.computedOrientation["z"] = "x"

    """
    Return position where reference position is the center of the local space
    """
    def getCornersLocalPositions(self, referencePosition, flip, rotation):

        if flip == 1 or flip == 3 :
            referencePosition[0] = self.size[0] - 1 - referencePosition[0]
            referencePosition[2] = self.size[2] - 1 - referencePosition[2]
        else : 
            referencePosition[0] = self.size[0] - 1 - referencePosition[0]
            referencePosition[2] = self.size[2] - 1 - referencePosition[2]

        positions = [[- referencePosition[0],                        - referencePosition[2]], 
                     [self.size[0] - referencePosition[0],           - referencePosition[2]], 
                     [- referencePosition[0] - referencePosition[0], self.size[2] - referencePosition[2]], 
                     [self.size[0] - referencePosition[0],           self.size[2] - referencePosition[2]]]
        toReturn = []

        for position in positions :
            temp = _math.rotatePointAround([0, 0], 
                position ,   math.pi / 2 * rotation)
            
            toReturn.append([int(temp[0]), referencePosition[1], int(temp[1])])
        
        return positions


    def getSize(self):
        return self.size
    

    def size_x(self):
        return self.size[0]
        

    def size_y(self):
        return self.size[1]
        

    def size_z(self):
        return self.size[2]


    def getRotateSize(self):
        return [self.size[2], self.size[1], self.size[0]]