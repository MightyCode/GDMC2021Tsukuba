from generation._resources import *
from generation._buildings import *
from utils._worldModification import *
import lib.interfaceUtils as interfaceUtils
from nbt.nbt import *


ressources = Resources()
interface = interfaceUtils.Interface()
worldModif = WorldModification(interface)
area = (0,0,128,128)
interfaceUtils.runCommand("execute at @p run setbuildarea ~-64 0 ~-64 ~64 255 ~64")
buildArea = interfaceUtils.requestBuildArea()

cx = int(area[0] + area[2]/2)
cz = int(area[1] + area[3]/2)
cy = 255

print(interfaceUtils.getAllBiome())