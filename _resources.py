from nbt import nbt
from _buildings import *
import json

class Resources :
    STRUCTURE_PATH = "data/structures/"
    LOOT_TABLE_PATH = "data/lootTables/"
    BIOME = "data/biome.txt"
    BIOME_BLOCK = "data/biomeBlocks.json"

    def __init__(self):

        # Each structures
        self.buildings = {}
        self.lootTables = {}

        # Contains for each biome, its minecraft id
        # biomename -> id minecraft
        self.biomes = {}
        # Contains for each id biome, its name
        # id minecraft -> biomename
        self.biomeMinecraftId = {}
        # Contains for each id biome, its block id
        # biomename -> id block (decoration)
        self.biomesBlockId = {}

        # Indicates for each block id, what should be blocks for types (ex : wookType)
        self.biomesBlocks = {}
        with open(Resources.BIOME_BLOCK) as json_file:
            self.biomesBlocks = json.load(json_file)

        filin = open(Resources.BIOME)

        lines = filin.readlines()
        i = 0
        for line in lines:
            if len(line.split(":")) > 1 :
                biomename = line.split(":")[0]
                value = int(line.split(":")[1])

                self.biomeMinecraftId[i] = biomename
                self.biomes[biomename] = i
                self.biomesBlockId[biomename] = value
            i = i + 1


    def loadBuildings(self, path, infoPath, name):
        nbtfile = nbt.NBTFile(Resources.STRUCTURE_PATH + path,'rb')
        with open(Resources.STRUCTURE_PATH + infoPath) as json_file:
           info = json.load(json_file)

        assert(not name in self.buildings.keys())
        self.buildings[name] = Buildings(nbtfile, info, name)


    def loadLootTable(self, path, name):
        with open(Resources.LOOT_TABLE_PATH + path) as json_file:
           self.lootTables[name] = json.load(json_file)



