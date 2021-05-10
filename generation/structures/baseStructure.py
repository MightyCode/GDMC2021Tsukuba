import math
import utils._math as _math

class BaseStructure:

    ORIENTATIONS = ["west", "north" , "east", "south"]

    def __init__(self):
        pass

    def setInfo(self, info):
        self.info = info
        self.size = [0, 0]
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
            BaseStructure.ORIENTATIONS[0] : BaseStructure.ORIENTATIONS[0],
            BaseStructure.ORIENTATIONS[1] : BaseStructure.ORIENTATIONS[1],
            BaseStructure.ORIENTATIONS[2] : BaseStructure.ORIENTATIONS[2],
            BaseStructure.ORIENTATIONS[3] : BaseStructure.ORIENTATIONS[3]
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
        if flip == 1 or flip == 3 :
            referencePosition[0] = self.size[0] - 1 - referencePosition[0]

        if flip == 2 or flip == 3 :
            referencePosition[2] = self.size[2] - 1 - referencePosition[2]

        positions = [[- referencePosition[0],                        - referencePosition[2]], 
                     [self.size[0] - 1 - referencePosition[0],       - referencePosition[2]], 
                     [- referencePosition[0],                       self.size[2] - 1 - referencePosition[2]], 
                     [self.size[0] - 1 - referencePosition[0],       self.size[2] - 1 - referencePosition[2]]]
        toReturn = []

        for position in positions :
            temp = _math.rotatePointAround([0, 0], 
                position , math.pi / 2 * rotation)
            
            toReturn.append([int(temp[0]), referencePosition[1], int(temp[1])])
        
        # Sort corner
        for dimension in (0, 2):
            for i in range(1):
                for j in range(3):
                    if toReturn[3 - j][dimension] < toReturn[2 - j][dimension]:
                        temp = toReturn[3 - j]
                        toReturn[3 - j] = toReturn[2 - j]
                        toReturn[2 - j] = temp
        
        return toReturn


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