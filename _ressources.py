from nbt import nbt
from _buildings import *

class Ressources :
    def __init__(self):
        self.buildings = {}

    def loadBuildings(self, path, name):
        nbtfile = nbt.NBTFile(path,'rb')
        
        assert(not name in self.buildings.keys())
        self.buildings[name] = Buildings(nbtfile)