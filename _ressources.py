from nbt import nbt
from _buildings import *
import json

class Ressources :
    PATH = "data/structures/"
    def __init__(self):
        self.buildings = {}

    def loadBuildings(self, path, infoPath, name):
        nbtfile = nbt.NBTFile(Ressources.PATH + path,'rb')
        with open(Ressources.PATH + infoPath) as json_file:
           info = json.load(json_file)

        assert(not name in self.buildings.keys())
        self.buildings[name] = Buildings(nbtfile, info)

