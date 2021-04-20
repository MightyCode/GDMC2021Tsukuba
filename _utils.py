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