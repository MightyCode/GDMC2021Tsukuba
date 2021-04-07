from nbt import nbt
from _buildings import *

class Ressources :
    PATH = "data/structures/"
    def __init__(self):
        self.buildings = {}

    def loadBuildings(self, path, name):
        nbtfile = nbt.NBTFile(Ressources.PATH + path,'rb')
        
        assert(not name in self.buildings.keys())
        self.buildings[name] = Buildings(nbtfile)