from _worldModification import *
from _resources import *
from _buildings import *
import requests
import time
import sys
import random
import interfaceUtils
from nbt.nbt import *



ressources = Resources()
ressources.loadBuildings("fireplace.nbt", "fireplace.json", "fireplace")
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
print(interfaceUtils.getHeight(0,0))