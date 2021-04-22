def strToDictBlock(block) :
    expended = {}
    parts = block.split["["]
    expended["Name"] = parts[0]
    expended["Properties"] = {}

    if len(parts) > 1:
        subParts = parts[1].split(",")
        for i in subParts:
            subsubParts = i.split("=")
            expended["Properties"][subsubParts[0]] = subsubParts[1]

    return expended


def convertNbtBlockToStr(blockPalette, rotation, flip):
    block = blockPalette["Name"].value + "["

    if "Properties" in blockPalette.keys():
        for key in blockPalette["Properties"].keys():
            block += self.convertProperty(key, blockPalette["Properties"][key].value, rotation, flip) + ","
  
        block = block[:-1] 
    block += "]"
    return block


def compareTwoDictBlock(a, b):
    if a["Name"] != b["Name"]:
        return false
    
    if len(a.keys()) != len(b.keys()):
        return false

    for key in a.keys() :
        if not b.keys().contains(key):
            return False
        
        if a[key] != b[key]:
            return False

    return true


def isPointInSquare(point, square):
    if (square[0] <= point[0] and square[3] >= point[0]):
        if (square[1] <= point[1] and square[4] >= point[1]):
            if (square[2] <= point[2] and square[5] >= point[2]):
                return True

    return False