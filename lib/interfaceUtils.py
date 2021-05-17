# ! /usr/bin/python3
"""### Provide tools for placing and getting blocks and more.

This module contains functions to:
* Request the build area as defined in-world
* Run Minecraft commands
* Get the name of a block at a particular coordinate
* Place blocks in the world
"""
__all__ = ['Interface', 'requestBuildArea', 'runCommand',
           'setBlock', 'getBlock', 'sendBlocks']
# __version__

import requests
from requests.exceptions import ConnectionError
from io import BytesIO
from lib.bitarray import BitArray
import requests
import math
import nbt
import numpy as np
import lib.worldLoader as worldLoader
from lib.worldLoader import WorldSlice
import random

class Interface:
    """**Provides tools for interacting with the HTML interface**.

    All function parameters and returns are in local coordinates.
    """
    def __init__(self, x=0, y=0, z=0, buffering=False, bufferlimit=1024):
        """**Initialise an interface with offset and buffering**."""
        self.offset = x, y, z
        self.__buffering = buffering
        self.bufferlimit = bufferlimit
        self.buffer = []

        random.seed(a=None, version=2)

    def __del__(self):
        """**Clean up before destruction**."""
        self.sendBlocks()

    def getBlock(self, x, y, z, includeState=False):
        """**Return the name of a block in the world**."""
        x, y, z = self.local2global(x, y, z)

        state = 'true' if includeState else 'false'
        url = 'http://localhost:9000/blocks?x={}&y={}&z={}&includeState={}'.format(x, y, z, state)
        try:
            response = requests.get(url)
        except ConnectionError:
            return "minecraft:void_air"
        return response.text

    def fill(self, x1, y1, z1, x2, y2, z2, blockStr):
        """**Fill the given region with the given block**."""
        x1, y1, z1 = self.local2global(x1, y1, z1)
        x2, y2, z2 = self.local2global(x2, y2, z2)
        xlo, ylo, zlo = min(x1, x2), min(y1, y2), min(z1, z2)
        xhi, yhi, zhi = max(x1, x2), max(y1, y2), max(z1, z2)

        for x in range(xlo, xhi + 1):
            for y in range(ylo, yhi + 1):
                for z in range(zlo, zhi + 1):
                    self.setBlock(x, y, z, blockStr)

    def setBlock(self, x, y, z, blockStr):
        """**Place a block in the world depending on buffer activation**."""
        if self.__buffering:
            self.placeBlockBatched(x, y, z, blockStr, self.bufferlimit)
        else:
            self.placeBlock(x, y, z, blockStr)

    def placeBlock(self, x, y, z, blockStr):
        """**Place a single block in the world**."""
        x, y, z = self.local2global(x, y, z)

        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        try:
            response = requests.put(url, blockStr)
        except ConnectionError:
            return "0"
        return response.text

    # ----------------------------------------------------- block buffers

    def toggleBuffer(self):
        """**Activates or deactivates the buffer function safely**."""
        self.buffering = not self.buffering
        return self.buffering

    def isBuffering(self):
        """**Get self.__buffering**."""
        return self.__buffering

    def setBuffering(self, value):
        """**Set self.__buffering**."""
        self.__buffering = value
        if self.__buffering:
            print("Buffering has been activated.")
        else:
            self.sendBlocks()
            print("Buffering has been deactivated.")

    def getBufferlimit(self):
        """**Get self.bufferlimit**."""
        return self.bufferlimit

    def setBufferLimit(self, value):
        """**Set self.bufferlimit**."""
        self.bufferlimit = value

    def placeBlockBatched(self, x, y, z, blockStr, limit=50):
        """**Place a block in the buffer and send once limit is exceeded**."""
        x, y, z = self.local2global(x, y, z)

        self.buffer.append((x, y, z, blockStr))
        if len(self.buffer) >= limit:
            return self.sendBlocks()
        else:
            return None

    def sendBlocks(self, x=0, y=0, z=0, retries=5):
        """**Send the buffer to the server and clear it**.

        Since the buffer contains global coordinates
            no conversion takes place in this function
        """
        url = 'http://localhost:9000/blocks?x={}&y={}&z={}'.format(x, y, z)
        body = str.join("\n", ['~{} ~{} ~{} {}'.format(*bp)
                               for bp in self.buffer])
        try:
            response = requests.put(url, body)
            self.buffer = []
            return response.text
        except ConnectionError as e:
            print("Request failed: {} Retrying ({} left)".format(e, retries))
            if retries > 0:
                return self.sendBlocks(x, y, z, retries - 1)

    # ----------------------------------------------------- utility functions

    def local2global(self, x, y, z):
        """**Translate local to global coordinates**."""
        result = []
        if x is not None:
            result.append(x + self.offset[0])
        if y is not None:
            result.append(y + self.offset[1])
        if z is not None:
            result.append(z + self.offset[2])
        return result

    def global2local(self, x, y, z):
        """**Translate global to local coordinates**."""
        result = []
        if x is not None:
            result.append(x - self.offset[0])
        if y is not None:
            result.append(y - self.offset[1])
        if z is not None:
            result.append(z - self.offset[2])
        return result

    #------------ caranha functions

    def makeBuildArea(width = 128, height = 128):
        runCommand("execute at @p run setbuildarea ~{} 0 ~{} ~{} 255 ~{}".format(int(-1*width/2), int(-1*height/2), int(width/2), int(height/2)))
        buildArea = requestBuildArea()
        x1 = buildArea["xFrom"]
        z1 = buildArea["zFrom"]
        x2 = buildArea["xTo"]
        z2 = buildArea["zTo"]
        return (x1, z1, x2 - x1, z2 - z1)

    def setSignText(x, y, z, line1 = "", line2 = "", line3 = "", line4 = ""):
        l1 = 'Text1:\'{"text":"'+line1+'"}\''
        l2 = 'Text2:\'{"text":"'+line2+'"}\''
        l3 = 'Text3:\'{"text":"'+line3+'"}\''
        l4 = 'Text4:\'{"text":"'+line4+'"}\''
        blockNBT = "{"+l1+","+l2+","+l3+","+l4+"}"
        return(runCommand("data merge block {} {} {} ".format(x, y, z) + blockNBT))

    def addItemChest(x, y, z, items, places=[]):
        if len(places) == 0:
            places = list(range(len(items)))

        for id, v in enumerate(items):
            id = places[id]
            command = "replaceitem block {} {} {} {} {} {}".format(x, y, z,
                                                                   "container."+str(id),
                                                                   v[0],
                                                                   v[1])
            runCommand(command)

    def makeBookItem(text, title = "", author = "", desc = ""):
        booktext = "pages:["
        while len(text) > 0:
            page = text[:15*23]
            text = text[15*23:]
            bookpage = "'{\"text\":\""
            while len(page) > 0:
                line = page[:23]
                page = page[23:]
                bookpage += line+"\\\\n"
            bookpage += "\"}',"
            booktext += bookpage

        booktext = booktext + "],"

        booktitle = "title:\""+title+"\","
        bookauthor = "author:\""+author+"\","
        bookdesc = "display:{Lore:[\""+desc+"\"]}"

        return "written_book{"+booktext+booktitle+bookauthor+bookdesc+"}"


    #------- our functions    
    def requestBuildArea():
        """**Requests a build area and returns it as an dictionary containing
        the keys xFrom, yFrom, zFrom, xTo, yTo and zTo**"""
        response = requests.get('http://localhost:9000/buildarea')
        if response.ok:
            return response.json()
        else:
            print(response.text)
            return -1

    def getBiome(seld,x, z, dx, dz):
        """**Returns the chunk data.**"""
        x = math.floor(x / 16)
        z = math.floor(z / 16)

        url = f'http://localhost:9000/chunks?x={x}&z={z}&dx={dx}&dz={dz}'
        try:
            response = requests.get(url)
        except ConnectionError:
            #return "minecraft:plains"
            return 0
        biomeId = response.text.split(":")
        biomeinfo = biomeId[6].split(";")
        biome = biomeinfo[1].split(",")
        return biome[0]

    def getAllBiome(self):
      
        bytes = worldLoader.getChunks(-4, -4, 9, 9, 'bytes')
        file_like = BytesIO(bytes)
        nbtfile = nbt.nbt.NBTFile(buffer=file_like)
        dicochunk = {}
        for y in range(81):
            for x in range(1024):
                if f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}" in dicochunk:
                    dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"] = int(dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"]) + 1 
                else:
                    dicochunk[f"{nbtfile['Chunks'][y]['Level']['Biomes'].value[x]}"] = "1"

        max = 0
        savedbiome = 0
        for x,y in dicochunk.items():
            if y > max:
                savedbiome = x
                max = y
        value = getNameBiome(savedbiome)
        return value
            

    def getNameBiome(self, biome):
        filin = open("data/biome.txt")
        lignes = filin.readlines()
        biomename = lignes[int(biome)].split(":")[0]
        print(biomename)
        value = int(lignes[int(biome)].split(":")[1])
        return value


    def registerSetBlock(x, y, z, str):
        """**Places a block in the buffer.**"""
        global blockBuffer
        # blockBuffer += () '~{} ~{} ~{} {}'.format(x, y, z, str)
        blockBuffer.append((x, y, z, str))


    def clearBlockBuffer():
        """**Clears the block buffer.**"""
        global blockBuffer
        blockBuffer = []


def runCommand(command):
    """**Run a Minecraft command in the world**."""
    url = 'http://localhost:9000/command'
    try:
        response = requests.post(url, bytes(command, "utf-8"))
    except ConnectionError:
        return "connection error"
    return response.text


def requestBuildArea():
    """**Return the building area**."""
    area = 0, 0, 0, 128, 256, 128   # default area for beginners
    response = requests.get('http://localhost:9000/buildarea')
    if response.ok:
        buildArea = response.json()
        if buildArea != -1:
            x1 = buildArea["xFrom"]
            y1 = buildArea["yFrom"]
            z1 = buildArea["zFrom"]
            x2 = buildArea["xTo"]
            y2 = buildArea["yTo"]
            z2 = buildArea["zTo"]
            area = x1, y1, z1, x2, y2, z2
    else:
        print(response.text)
        print("Using default build area.")
    return area

# ========================================================= global interface

blockBuffer = []
globalinterface = Interface()


def isBuffering():
    """**Global isBuffering**."""
    return globalinterface.isBuffering()

def getHeight(x,z):
    return globalinterface.getHeight(x,z)


def setBuffering(val):
    """**Global setBuffering**."""
    globalinterface.setBuffering(val)



def getBufferLimit():
    """**Global getBufferLimit**."""
    return globalinterface.getBufferLimit()



def setBufferLimit(val):
    """**Global setBufferLimit**."""
    globalinterface.setBufferLimit(val)


def getBlock(x, y, z):
    """**Global getBlock**."""
    return globalinterface.getBlock(x, y, z)

def getAllBiome():
    return globalinterface.getAllBiome()

def getNameBiome(biome):     
    return globalinterface.getNameBiome(biome)

def fill(x1, y1, z1, x2, y2, z2, blockStr):
    """**Global fill**."""
    return globalinterface.fill(x1, y1, z1, x2, y2, z2, blockStr)

def getHeight(x,z,ws):
    return globalinterface.getHeight(x,z,ws)

def is_ground(x,y,z,ws):
    return globalinterface.is_ground(x,y,z,ws)

def is_air(x,y,z,ws):
    return globalinterface.is_air(x,y,z,ws)

def setBlock(x, y, z, blockStr):
    """**Global setBlock**."""
    return globalinterface.setBlock(x, y, z, blockStr)

def getBiome(x, z, dx, dz):
    return globalinterface.getBiome(x,z,dx,dz)

def findPosHouse(CornerPos,ws):
    return globalinterface.findPosHouse(CornerPos,ws)

def verifHouse(xPos, yPos, zPos, CornerPos):
    return globalinterface.verifHouse(xPos, yPos, zPos, CornerPos)

# ----------------------------------------------------- block buffers



def toggleBuffer():
    """**Global toggleBuffer**."""
    return globalinterface.toggleBuffer()


def sendBlocks(x=0, y=0, z=0, retries=5):
    """**Global sendBlocks**."""
    return globalinterface.sendBlocks(x, y, z, retries)

