import math
import utils._math as _math

class BaseStructure:

    ORIENTATIONS = ["west", "north" , "east", "south"]

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


    def getNextBuildingInformation(self):
        return

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