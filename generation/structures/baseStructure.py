import math
import utils._math as _math
import lib.interfaceUtils as interfaceUtils

class BaseStructure:

    ORIENTATIONS = ["west", "north" , "east", "south"]
    LIST_ALL_FACING = ["south", "south-southwest", "southwest",
                    "west-southwest",  "west", "west-northwest", 
                    "northwest", "north-northwest", "north",
                    "north-northeast", "northeast", "east-northeast",
                    "east", "east-southeast", "southeast", "south-southeast"]

    def __init__(self):
        pass

    def setInfo(self, info):
        self.info = info
        self.size = [0, 0, 0]
        self.computedOrientation = {}


    def returnWorldPosition(self, localPoint, flip, rotation, referencePoint, worldStructurePosition) :
        worldPosition = [0, 0, 0]
        
        # Position in building local spacereplacements
        if flip == 1 or flip == 3 :
            worldPosition[0] = self.size[0] - 1 - localPoint[0]
        else : 
            worldPosition[0] = localPoint[0]

        if flip == 2 or flip == 3 :
            worldPosition[2] = self.size[2] - 1 - localPoint[2]
        else :
           worldPosition[2] = localPoint[2]

        worldPosition[1] = localPoint[1]

        # Take rotation into account, apply to building local positions
        worldPosition[0], worldPosition[2] = _math.rotatePointAround(
            [worldStructurePosition[0] + referencePoint[0], worldStructurePosition[2] + referencePoint[2]], 
            [worldStructurePosition[0] + worldPosition[0], worldStructurePosition[2] + worldPosition[2]], 
            rotation *  math.pi / 2)

        # Position in real world
        
        worldPosition[0] = int(worldPosition[0])                        - referencePoint[0]
        worldPosition[1] = worldStructurePosition[1] + worldPosition[1] - referencePoint[1] 
        worldPosition[2] = int(worldPosition[2])                        - referencePoint[2]
        return worldPosition 


    def convertProperty(self, propertyName, propertyValue):
        if propertyValue in self.computedOrientation.keys():
            propertyValue = self.computedOrientation[propertyValue]

        return propertyName + "=" + propertyValue


    def returnRotationFromFacing(self, facing):
        for i in [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]:
            if BaseStructure.LIST_ALL_FACING[i] == facing:
                return i
        
        return -1


    def computeOrientation(self, rotation, flip) :
        # Construct orientation
        self.computedOrientation = { 
            "left" : "left",
            "right" : "right",
            "x" : "x",
            "y" : "y",
            BaseStructure.ORIENTATIONS[0] : BaseStructure.ORIENTATIONS[0],
            BaseStructure.ORIENTATIONS[1] : BaseStructure.ORIENTATIONS[1],
            BaseStructure.ORIENTATIONS[2] : BaseStructure.ORIENTATIONS[2],
            BaseStructure.ORIENTATIONS[3] : BaseStructure.ORIENTATIONS[3]
        }
        
        # Apply flip to orientation
        if flip == 1 or flip == 3:
            self.computedOrientation["east"] = "west" 
            self.computedOrientation["west"] = "east"
            
        if flip == 2 or flip == 3:
            self.computedOrientation["south"] = "north"
            self.computedOrientation["north"] = "south"

        if flip == 1 or flip == 2:
            self.computedOrientation["left"] = "right"
            self.computedOrientation["right"] = "left"

        # Apply rotation to orientation
        for orientation in self.computedOrientation.keys():
            if orientation in BaseStructure.ORIENTATIONS:
                self.computedOrientation[orientation] = BaseStructure.ORIENTATIONS[
                    (BaseStructure.ORIENTATIONS.index(self.computedOrientation[orientation]) + rotation) % len(BaseStructure.ORIENTATIONS)
                ]

        if rotation == 1 or rotation == 3:
            self.computedOrientation["x"] = "z"
            self.computedOrientation["z"] = "x"


    """
    Return position where reference position is the center of the local space
    """
    def getCornersLocalPositions(self, referencePosition, flip, rotation):
        refPos = referencePosition.copy()
        if flip == 1 or flip == 3 :
            refPos[0] = self.size[0] - 1 - refPos[0]

        if flip == 2 or flip == 3 :
            refPos[2] = self.size[2] - 1 - refPos[2]

        temp = _math.rotatePointAround([0, 0], [- refPos[0], - refPos[2]] , math.pi / 2 * rotation)

        temp1 = _math.rotatePointAround([0, 0], [self.size[0] - 1 - refPos[0], self.size[2] - 1 - refPos[2]] , math.pi / 2 * rotation)
        
        return [int(min(temp[0], temp1[0])), 
                int(min(temp[1], temp1[1])), 
                int(max(temp[0], temp1[0])), 
                int(max(temp[1], temp1[1]))]

    
    def getCornersLocalPositionsAllFlipRotation(self, referencePosition):
        corners = []
        for flip in [0, 1, 2, 3]:
            for rotation in [0, 1, 2, 3]:
                corners.append(self.getCornersLocalPositions(referencePosition, flip, rotation))

        return corners


    def generateSignatureSign(self, position, worldModification, woodType, people):
        worldModification.setBlock(position[0], position[1], position[2], "minecraft:air", placeImmediately=True)
        worldModification.setBlock(position[0], position[1], position[2], 
            "minecraft:" + woodType + "_wall_sign[facing=" + self.computedOrientation[self.info["sign"]["facing"]] + "]", 
            placeImmediately=True)
    
        lines = ["", "", "", "", "", "", "", ""]
        lines[0] = "Tier " + str(self.info["sign"]["tier"])
        lines[1] = self.info["sign"]["name"]

        currentLine = 2
        for person in people:
            partss = ("-" + person + "\n").split(" ")
            parts = []

            for i in range(len(partss)):
                if len(partss[i]) > 15:
                    parts.append(partss[i][0:14])
                    parts.append(partss[i][15:])
                else:
                    parts.append(partss[i])

            i = 0
            while i < len(parts) and currentLine < len(lines):
                jumpLine = False
                if len(lines[currentLine]) > 0 :
                    if len(parts[i]) + 1  <= 15 - len(lines[currentLine]):
                        if "\n" in parts[i]:
                            jumpLine = True
                        lines[currentLine] += " " + parts[i].replace("\n", "")
                        i += 1
                    else :
                        jumpLine = True

                else :
                    if len(parts[i])  <= 15 - len(lines[currentLine]):
                        if "\n" in parts[i]:
                            jumpLine = True
                        lines[currentLine] += parts[i].replace("\n", "")
                        i += 1
                    else :
                        jumpLine = True
                
                if jumpLine :
                    currentLine += 1

        interfaceUtils.setSignText(
            position[0], position[1], position[2], 
            lines[0], lines[1], lines[2], lines[3])

        if len(lines[4]) > 0:
            worldModification.setBlock(position[0], position[1] - 1, position[2], "minecraft:air", placeImmediately=True)
            worldModification.setBlock(position[0], position[1] - 1, position[2], 
                "minecraft:" + woodType + "_wall_sign[facing=" + self.computedOrientation[self.info["sign"]["facing"]] + "]", 
                placeImmediately=True)

            interfaceUtils.setSignText(
                position[0], position[1] - 1, position[2], 
                lines[4], lines[5], lines[6], lines[7])


    def getFacingMainEntry(self, flip, rotation):
        self.computeOrientation(rotation, flip)
        return self.computedOrientation[self.info["mainEntry"]["facing"]]


    def setupInfoAndGetCorners(self):
        return {}


    def getNextBuildingInformation(self, flip, rotation):
        return {}


    def setSize(self, size):
        self.size = size


    def getSize(self):
        return self.size
    

    def size_x(self):
        return self.size[0]
        

    def size_y(self):
        return self.size[1]
        

    def size_z(self):
        return self.size[2]


    def getRotateSize(self):
        return [self.size[2], self.size[1], self.size[0]]

    
    def propertyCompatible(self, blockName, property):
        if property == "snowy":
            if blockName != "minecraft:grass_block":
                return False
        
        return True


    def createBuildingCondition():
        return {
            "size" : [0, 0, 0],
            "position" : [0, 0, 0],
            "referencePoint" : [0, 0, 0],
            "flip" : 0,
            "rotation" : 0,
            "replaceAllAir" : 0,
            "replacements" : {},
            "villager" : [],
            "prebuildingInfo" : {}
        }