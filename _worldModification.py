import os.path
from os import path
import json 
import interfaceUtils

# Class which serve to save all modification, do undo actions
class WorldModification: 
    DEBUG_MODE = False
    
    DEFAULT_PATH = "logs/"
    CONFIG_PATH = "config/config.json"
    BLOCK_SEPARATOR = "$"
    PARTS_SEPARATOR = "°"
    

    def __init__(self, interface):
        self.interface = interface

        self.before_modification = []
        self.after_modificaton = []
        
        with open(WorldModification.CONFIG_PATH) as f:
            config = json.load(f)
            if "debugMode" in config.keys():
                WorldModification.DEBUG_MODE = config["debugMode"]

    def setBlock(self, x, y, z, block, compareBlockState=False):
        if WorldModification.DEBUG_MODE:
            previousBlock = self.interface.getBlock(x, y, z, True)

            # We won't replace block by same one, 
            # option to compare or not the state of both blocks -> [...]
            if block.split("[")[0] == previousBlock.split("[")[0]:
                if compareBlockState: 
                    pass
                    # TODO
                else :
                    return

            self.before_modification.append([x, y, z, previousBlock])
            self.after_modificaton.append([x, y, z, block])

        self.interface.setBlock(x, y, z, block)

    def fillBlocks(self, from_x, from_y, from_z, to_x, to_y, to_z, block, compareBlockState=False):
        if WorldModification.DEBUG_MODE :
            if from_x > to_x : 
                to_x, from_x = from_x, to_x
            if from_y > to_y : 
                to_y, from_y = from_y, to_y
            if from_z > to_z : 
                to_z, from_z = from_z, to_z
            
            for x in range(from_x, to_x + 1):
                for y in range(from_y, to_y + 1):
                    for z in range(from_z, to_z + 1):
                        # We won't replace block by same one, 
                        # option to compare or not the state of both blocks -> [...]
                        previousBlock = self.interface.getBlock(x, y, z, True)
                        if block.split("[")[0] == previousBlock.split("[")[0]:
                            if compareBlockState: 
                                pass
                                # TODO
                            else :
                                continue

                        self.before_modification.append([x, y, z, previousBlock])
                        self.after_modificaton.append([x, y, z, block])
        
        self.interface.fill(from_x, from_y, from_z, to_x, to_y, to_z, block)

    def undoLastModification(self):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T UNDO ON NO DEBUG MODE")
            return 

        index = len(self.before_modification) - 1
        self.interface.setBlock(
            self.before_modification[index][0],
            self.before_modification[index][1],
            self.before_modification[index][2],
            self.before_modification[index][3],
        )

        self.before_modification.pop()
        self.after_modificaton.pop()

    def undoAllModification(self):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T UNDO ON NO DEBUG MODE")
            return 

        for i in range(len(self.before_modification)):
            self.undoLastModification()

    def saveToFile(self, file_name) :
        if not WorldModification.DEBUG_MODE:
            print("CAN'T SAVE ON NO DEBUG MODE")
            return 

        assert(len(self.before_modification) == len(self.after_modificaton))

        if path.exists(WorldModification.DEFAULT_PATH + file_name) :
            parts = file_name.split(".")
            if len(file_name.split("_")) > 1 :
                self.saveToFile(parts[0].split("_")[0] + "_" + str(
                    int(file_name.split("_")[1].split(".")[0]) + 1
                ) + "." + parts[1])
            else :             
                self.saveToFile(parts[0] + "_0." + parts[1])
            return

        f = open(WorldModification.DEFAULT_PATH + file_name, "w")
        f.truncate(0)
        for i in range(len(self.before_modification)) :
            f.write(
                str(self.before_modification[i][0]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][1]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][2]) + WorldModification.BLOCK_SEPARATOR +
                str(self.before_modification[i][3]) + WorldModification.PARTS_SEPARATOR +
                str(self.after_modificaton[i][0])   + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modificaton[i][1])   + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modificaton[i][2])   + WorldModification.BLOCK_SEPARATOR +
                str(self.after_modificaton[i][3])
            )

            if i < len(self.before_modification) - 1 :
                f.write("\n")
        f.close()
        

    def loadFromFile(self, file_name):
        if not WorldModification.DEBUG_MODE:
            print("CAN'T LOAD ON NO DEBUG MODE")
            return 

        with open(WorldModification.DEFAULT_PATH + file_name) as f:
            for line in f:
                parts = line.split(WorldModification.PARTS_SEPARATOR)

                before_parts = parts[0].split(WorldModification.BLOCK_SEPARATOR)
                after_parts = parts[1].split(WorldModification.BLOCK_SEPARATOR)
                self.before_modification.append([
                   int(before_parts[0]),
                    int(before_parts[1]),
                    int(before_parts[2]),
                    before_parts[3]
                ])

                self.after_modificaton.append([
                    int(after_parts[0]),
                    int(after_parts[1]),
                    int(after_parts[2]),
                    after_parts[3]
                ])
                
        os.remove(WorldModification.DEFAULT_PATH + file_name) 