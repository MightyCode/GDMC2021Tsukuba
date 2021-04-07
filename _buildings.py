import _math
import math

class Buildings:
    ORIENTATIONS = ["west", "north" , "east", "south"]

    """
    Flip is applied before rotation

    flip : No flip = 0, Flip x = 1, flip z = 2, Flip xz = 3
    rotation : No rotation = 0, rotation 90 = 1, rotation 180 = 2, rotation 270 = 3
    replaceAllAir : 0 no air placed, 1 place all air block, 2 place all choosen air block
    position : the center of the contruction
    referencePoint : point x, z where the building will rotate around, the block at the reference point will be on position point
    """
    BUILDINGS_CONDITIONS =  {
        "rotation" : 0,
        "flip" : 0,
        "replaceAllAir" : 0,
        "position" : [0, 0, 0],
        "referencePoint" : [0, 0]
    }

    def __init__(self, nbtfile, info):
        self.size = [nbtfile["size"][0].value, nbtfile["size"][1].value, nbtfile["size"][2].value]
        self.file = nbtfile
        self.info = info

        self.computedOrientation = {}

    def build(self, worldModif, buildingCondition):
        self.computeOrientation(buildingCondition["rotation"], buildingCondition["flip"])

        if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][0] = self.size[0] - buildingCondition["referencePoint"][0] 
        if buildingCondition["flip"] == 2 or buildingCondition["flip"] == 3:
            buildingCondition["referencePoint"][1] = self.size[2] - buildingCondition["referencePoint"][1] 
         
        toRemove = [buildingCondition["referencePoint"][0], 0, buildingCondition["referencePoint"][1]]

        if "mainEntry" in self.info.keys():
            toRemove[1] = self.info["mainEntry"]["position"][1]

        print(_math.rotatePointAround(
                [buildingCondition["position"][0] + buildingCondition["referencePoint"][0], buildingCondition["position"][2] + buildingCondition["referencePoint"][1]], 
                [buildingCondition["position"][0] + 3, buildingCondition["position"][2] + 3], 
                buildingCondition["rotation"] *  math.pi / 2))

        for block in self.file["blocks"]:
            # Position of block in building local space
            # Take flip into account
            if buildingCondition["flip"] == 1 or buildingCondition["flip"] == 3 :
                x = self.size[0] - block["pos"][0].value
                z = self.size[2] - block["pos"][2].value
            else:
                x = block["pos"][0].value
                z = block["pos"][2].value

            y = block["pos"][1].value

            y = y - toRemove[1]

            # Take rotation into account
            positionX, positionZ = _math.rotatePointAround(
                [buildingCondition["position"][0] + buildingCondition["referencePoint"][0], buildingCondition["position"][2] + buildingCondition["referencePoint"][1]], 
                [buildingCondition["position"][0] + x, buildingCondition["position"][2] + z], 
                buildingCondition["rotation"] *  math.pi / 2)

            positionX = int(positionX) - toRemove[0]
            positionZ = int(positionZ) - toRemove[2]
            positionY = buildingCondition["position"][1] + y

            
            worldModif.setBlock(
                positionX, positionY, positionZ,
                self.convertNbtBlockToStr(
                    self.file["palette"][block["state"].value],
                    buildingCondition["rotation"],
                    buildingCondition["flip"])
            )
            
    
    def convertNbtBlockToStr(self, blockState, rotation, flip):
        block = blockState["Name"].value + "["

        if "Properties" in blockState.keys():
            for key in blockState["Properties"].keys():
                block += self.convertProperty(key, blockState["Properties"][key].value, rotation, flip) + ","
  
            block = block[:-1] 
        block += "]"
        return block


    def convertProperty(self, propertyName, propertyValue, rotation, flip):
        if propertyValue in self.computedOrientation.keys():
            propertyValue = self.computedOrientation[propertyValue]

        return propertyName + "=" + propertyValue

    def computeOrientation(self, rotation, flip) :
        # Construct orientation
        self.computedOrientation = { 
            "left" : "left",
            "right" : "right",
            "x" : "x",
            "y" : "y",
            Buildings.ORIENTATIONS[0] : Buildings.ORIENTATIONS[0],
            Buildings.ORIENTATIONS[1] : Buildings.ORIENTATIONS[1],
            Buildings.ORIENTATIONS[2] : Buildings.ORIENTATIONS[2],
            Buildings.ORIENTATIONS[3] : Buildings.ORIENTATIONS[3]
        }
        
        # Apply flip to orientation
        if flip == 1 or flip == 3:
            self.computedOrientation["east"] = "west" 
            self.computedOrientation["west"] = "east"

            if flip != 3:
                self.computedOrientation["left"] = "right"
                self.computedOrientation["right"] = "left"
            
        if flip == 2 or flip == 3:
            self.computedOrientation["south"] = "north"
            self.computedOrientation["north"] = "south"


        # Apply rotation to orientation
        for orientation in self.computedOrientation.keys():
            if orientation in Buildings.ORIENTATIONS:
                self.computedOrientation[orientation] = Buildings.ORIENTATIONS[
                    (Buildings.ORIENTATIONS.index(self.computedOrientation[orientation]) + rotation) % len(Buildings.ORIENTATIONS)
                ]

        if rotation == 1 or rotation == 3:
            self.computedOrientation["x"] = "z"
            self.computedOrientation["z"] = "x"

    def getSize(self):
        return self.size
    
    def size_x(self):
        return self.size[0]
        
    def size_y(self):
        return self.size[1]
        
    def size_z(self):
        return self.size[2]