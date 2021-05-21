import utils._math as _math
import utils._utils as _utils
from generation.structures.baseStructure import *
from nbt import nbt
import generation._floodFill as floodFill

class Structures(BaseStructure):
    REPLACEMENTS = "replacements"
    CHANGE = "Change"
    CHANGE_TO = "ChangeTo"
    CHANGE_STATE = "ChangeState"
    CHANGE_ORIGINAL_BLOCK = "OriginalBlock"
    CHANGE_REPLACEMENT_WORD = "ReplacementWord"
    CHANGE_EXCLUDED_ZONES = "ExcludedZone"

    AIR_BLOCKS = ["minecraft:air", "minecraft:void_air", "minecraft:cave_air"]

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
    BUILDING_CONDITIONS =  {
        "rotation" : 0,
        "flip" : 0,
        "replaceAllAir" : 0,
        "position" : [0, 0, 0],
        "referencePoint" : [0, 0, 0],
        "replacements" : {},
    }


    def __init__(self, nbtfile, info, name):
        super(BaseStructure, self).__init__()
        self.setInfo(info)

        self.setSize([nbtfile["size"][0].value, nbtfile["size"][1].value, nbtfile["size"][2].value])
        self.file = nbtfile
        self.name = name

        # Variable used on building
        self.placeImmediately = False

        self.computedOrientation = {}
        # Indicate for each block in palette if it should change or not and to change to what
        for block in self.file["palette"]:
            if Structures.REPLACEMENTS in self.info.keys():
                blockName = block["Name"].value.split("[")[0]

                for replacementWord in self.info[Structures.REPLACEMENTS].keys():
                    # Checking for block replacement
                    if blockName == replacementWord:
                        block.tags.append(nbt.TAG_Int(name=Structures.CHANGE_STATE, value=self.info[Structures.REPLACEMENTS][blockName]["state"]))
                                                                        #  """AND states equals"""
                        if block[Structures.CHANGE_STATE].value == 1 or (block[Structures.CHANGE_STATE].value == 0):
                            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=True))
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_TO, value=self.info[Structures.REPLACEMENTS][block["Name"].value]["type"]))   
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_ORIGINAL_BLOCK, value=block["Name"].value))
                            block.tags.append(nbt.TAG_String(name=Structures.CHANGE_REPLACEMENT_WORD, value=replacementWord))
                            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE_EXCLUDED_ZONES, 
                                value=("excluded" in self.info[Structures.REPLACEMENTS][replacementWord].keys())))
                            break
                        
                    # Checking for substr replacement 
                    elif replacementWord in blockName:
                        # The replacementWord can be in unexpected blocks
                        # "oak" is on every "...dark_oak..." block
                        if replacementWord in Structures.REPLACEMENTS_EXCLUSIF:
                            if Structures.REPLACEMENTS_EXCLUSIF[replacementWord] in blockName:
                                continue

                        if replacementWord in self.info[Structures.REPLACEMENTS].keys():
                            if self.info[Structures.REPLACEMENTS][replacementWord]["state"] == 2:
                                block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=True))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_TO, value=self.info[Structures.REPLACEMENTS][replacementWord]["type"]))  
                                block.tags.append(nbt.TAG_Int(name=Structures.CHANGE_STATE, value=2))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_ORIGINAL_BLOCK, value=(block["Name"].value) ))
                                block.tags.append(nbt.TAG_String(name=Structures.CHANGE_REPLACEMENT_WORD, value=replacementWord))

                                # True or False
                                block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE_EXCLUDED_ZONES, 
                                    value=("excluded" in self.info[Structures.REPLACEMENTS][replacementWord].keys())))
                                break
                                

            block.tags.append(nbt.TAG_Byte(name=Structures.CHANGE, value=False))
        
        # Looting table
        self.lootTable = False
        if "lootTables" in self.info.keys():
            self.lootTable = len(self.info["lootTables"]) > 0


    def getNextBuildingInformation(self):
        info = {}
        info["corners"] = self.getCornersLocalPositionsAllFlipRotation(self.info["mainEntry"]["position"])
        info["entry"] = { "position" : self.info["mainEntry"]["position"].copy(), "facing" : self.info["mainEntry"]["facing"] }
        info["size"] = self.size

        return info


    def build(self, worldModif, buildingCondition, chestGeneration):
        ## Pre computing :
        buildingCondition["referencePoint"] = buildingCondition["referencePoint"].copy()
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - 1 - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][2] = self.size[2] - 1 - buildingCondition["referencePoint"][2] 

        # Replace bloc by these given
        for blockPalette in self.file["palette"]:
            if blockPalette[Structures.CHANGE].value:
                changeState = blockPalette[Structures.CHANGE_STATE].value
                if changeState == 0 or changeState == 1:
                    blockPalette["Name"].value = buildingCondition["replacements"][blockPalette[Structures.CHANGE_TO].value].split("[")[0]
                elif changeState == 2:
                    blockPalette["Name"].value = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value.replace(
                        blockPalette[Structures.CHANGE_REPLACEMENT_WORD].value, 
                        buildingCondition["replacements"][blockPalette[Structures.CHANGE_TO].value].split("[")[0] )

        
        # Place support underHouse
        self.placeSupportUnderStructure(worldModif, buildingCondition)

        # Air zone
        self.placeAirZones(worldModif, buildingCondition)

        
        ## Computing : Modify from blocks
        for block in self.file["blocks"]:
            blockPalette = self.file["palette"][block["state"].value]
            self.placeImmediately = False

            # Check if the current block is in excluded zone
            takeOriginalBlock = False
            blockName = blockPalette["Name"].value
            if (blockPalette[Structures.CHANGE].value):
                if (blockPalette[Structures.CHANGE_EXCLUDED_ZONES].value):
                    for zone in self.info["replacements"][blockPalette[Structures.CHANGE_REPLACEMENT_WORD].value]["excluded"] :
                        if _math.isPointInSquare([ block["pos"][0].value, block["pos"][1].value, block["pos"][2].value], zone) :
                            takeOriginalBlock = True
                            blockName = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value
                            break


            # Check for block air replacement
            if blockName in Structures.AIR_BLOCKS and buildingCondition["replaceAllAir"] != 1:
                continue
            
            # Compute position of block from local space to world space
            blockPosition = self.returnWorldPosition(
                [ block["pos"][0].value, block["pos"][1].value + 1, block["pos"][2].value ],
                buildingCondition["flip"], buildingCondition["rotation"], 
                buildingCondition["referencePoint"], buildingCondition["position"] )
            
            self.checkBeforePlacing(blockName)

            worldModif.setBlock(
                blockPosition[0], blockPosition[1], blockPosition[2],
                self.convertNbtBlockToStr(
                    self.file["palette"][block["state"].value],
                    takeOriginalBlock
                    ), placeImmediately=self.placeImmediately
            )

            self.checkAfterPlacing(block, blockName, blockPosition, chestGeneration, buildingCondition)
            

    def checkBeforePlacing(self, blockName):
        if "chest" in blockName:
            self.placeImmediately = True


    def checkAfterPlacing(self, block, blockName, blockPosition, chestGeneration, buildingCondition):
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

        if "lectern" in blockName:
            if "lectern" in self.info:
                for key in self.info["lectern"].keys():
                    position = self.info["lectern"][key]
                    if block["pos"][0].value == position[0] and block["pos"][1].value == position[1] and block["pos"][2].value == position[2]:
                        result = _utils.changeNameWithBalise(key, buildingCondition)
                        if result[0] >= 0:
                            _utils.addBookToLectern(blockPosition[0], blockPosition[1], blockPosition[2], result[1])
                        else :
                            print("Can't add a book to a lectern at pos : " + str(blockPosition))
                        break


    def placeSupportUnderStructure(self, worldModif, buildingCondition):
        zones = []
        if "info" in self.info["ground"].keys():
            if "all" == self.info["ground"]["info"] :
                zones.append([0, 0, self.size[0] - 1, self.size[2] - 1])
        elif "zones" in self.info["ground"].keys() :
            zones = self.info["ground"]["zones"]

        for zone in zones : 
            for x in range(zone[0], zone[2] + 1):
                for z in range(zone[1], zone[3] + 1):
                    position = self.returnWorldPosition( 
                        [ x, 0, z],
                        buildingCondition["flip"], buildingCondition["rotation"], 
                        buildingCondition["referencePoint"], buildingCondition["position"] 
                    )

                    if worldModif.interface.getBlock(position[0], position[1], position[2]) in floodFill.FloodFill.IGNORED_BLOCKS:
                        i = -2 
                        while worldModif.interface.getBlock(position[0], position[1] + i, position[2]) in floodFill.FloodFill.IGNORED_BLOCKS:
                            i -= 1
                        
                        worldModif.fillBlocks(position[0], position[1], position[2], position[0], position[1] + i, position[2], 
                        buildingCondition["replacements"]["ground2"])


    def placeAirZones(self, worldModif, buildingCondition):
        if buildingCondition["replaceAllAir"] == 3:
            buildingCondition["replaceAllAir"] = self.info["air"]["preferedAirMode"]

        if buildingCondition["replaceAllAir"] == 2:
            for zones in self.info["air"]["replacements"]:
                blockFrom = self.returnWorldPosition([ zones[0], zones[1] + 1, zones[2] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])
                blockTo   = self.returnWorldPosition([ zones[3], zones[4] + 1, zones[5] ],
                                                     buildingCondition["flip"], buildingCondition["rotation"], 
                                                     buildingCondition["referencePoint"], buildingCondition["position"])
                                                     
                worldModif.fillBlocks(blockFrom[0], blockFrom[1], blockFrom[2], blockTo[0], blockTo[1], blockTo[2], Structures.AIR_BLOCKS[0])


    def convertNbtBlockToStr(self, blockPalette, takeOriginalBlockName=False):
        block = "["
        if takeOriginalBlockName:
            block = blockPalette[Structures.CHANGE_ORIGINAL_BLOCK].value + block
        else:
            block = blockPalette["Name"].value + block

        if "Properties" in blockPalette.keys():
            for key in blockPalette["Properties"].keys():
                block += self.convertProperty(key, blockPalette["Properties"][key].value) + ","
  
            block = block[:-1] 
        block += "]"
        return block
