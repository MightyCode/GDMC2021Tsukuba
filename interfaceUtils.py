# ! /usr/bin/python3
"""### Provide tools for placing and getting blocks and more.

This module contains functions to:
* Request the build area as defined in-world
* Run Minecraft commands
* Get the name of a block at a particular coordinate
* Place blocks in the world
"""
__all__ = ['requestBuildArea', 'runCommand',
           'setBlock', 'getBlock',
           'placeBlockBatched', 'sendBlocks']
# __version__

import requests

## ======== Caranha Functions ========== ##

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

def addItemChest(x, y, z, items):
    for id,v in enumerate(items):
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

## ======================================

def requestBuildArea():
    """**Requests a build area and returns it as an dictionary containing
    the keys xFrom, yFrom, zFrom, xTo, yTo and zTo**"""
    response = requests.get('http://localhost:9000/buildarea')
    if response.ok:
        return response.json()
    else:
        print(response.text)
        return -1

def runCommand(command):
    """**Executes one or multiple minecraft commands (separated by newlines).**"""
    # print("running cmd " + command)
    url = 'http://localhost:9000/command'
    try:
        response = requests.post(url, bytes(command, "utf-8"))
    except ConnectionError:
        return "connection error"
    return response.text

## ----------------------------------------------- get biome information

def getBiome (x, z, dx, dz):
    """**Returns the chunk data.**"""
    x = int(x / 16)
    z = int(z / 16)

    url = f'http://localhost:9000/chunks?x={x}&z={z}&dx={dx}&dz={dz}'
    try:
        response = requests.get(url)
    except ConnectionError:
        return "minecraft:plains"
    biomeId = response.text.split(":")
    biomeinfo = biomeId[6].split(";")
    biome = biomeinfo[1].split(",")
    return biome[0]


# --------------------------------------------------------- get/set block


def getBlock(x, y, z, includeState=False):
    """**Returns the namespaced id of a block in the world.**"""
    state = 'true' if includeState else 'false'
    url = f'http://localhost:9000/blocks?x={x}&y={y}&z={z}&includeState={state}'
    # print(url)
    try:
        response = requests.get(url)
    except ConnectionError:
        return "minecraft:void_air"
    return response.text
    # print("{}, {}, {}: {} - {}".format(x, y, z, response.status_code, response.text))


def setBlock(x, y, z, str):
    """**Places a block in the world.**"""
    url = f'http://localhost:9000/blocks?x={x}&y={y}&z={z}'
    # print('setting block {} at {} {} {}'.format(str, x, y, z))
    try:
        response = requests.put(url, str)
    except ConnectionError:
        return "0"
    return response.text
    # print("{}, {}, {}: {} - {}".format(x, y, z, response.status_code, response.text))


# --------------------------------------------------------- block buffers

blockBuffer = []


def placeBlockBatched(x, y, z, str, limit=50):
    """**Place a block in the buffer and send if the limit is exceeded.**"""
    registerSetBlock(x, y, z, str)
    if len(blockBuffer) >= limit:
        return sendBlocks(0, 0, 0)
    else:
        return None


def sendBlocks(x=0, y=0, z=0, retries=5):
    """**Sends the buffer to the server and clears it.**"""
    global blockBuffer
    body = str.join("\n", ['~{} ~{} ~{} {}'.format(*bp) for bp in blockBuffer])
    url = f'http://localhost:9000/blocks?x={x}&y={y}&z={z}'
    try:
        response = requests.put(url, body)
        clearBlockBuffer()
        return response.text
    except ConnectionError as e:
        print(f"Request failed: {e} Retrying ({retries} left)")
        if retries > 0:
            return sendBlocks(x, y, z, retries - 1)


def registerSetBlock(x, y, z, str):
    """**Places a block in the buffer.**"""
    global blockBuffer
    # blockBuffer += () '~{} ~{} ~{} {}'.format(x, y, z, str)
    blockBuffer.append((x, y, z, str))


def clearBlockBuffer():
    """**Clears the block buffer.**"""
    global blockBuffer
    blockBuffer = []
