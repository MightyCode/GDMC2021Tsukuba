import random
import utils._math as _math

class FloodFill:
    
    # Ignoreblockvalue is the list of block that we want to ignore when we read the field
    IGNORED_BLOCKS = [
        'minecraft:void_air', 'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow',
        'minecraft:dead_bush', "minecraft:cactus"]

    def __init__(self, area):
        self.listHouse = []
        random.seed(a=None, version=2)
        self.buildArea = area
        self.startPosRange = [0.85, 0.85]

        self.distanceFirstHouse = 40
        self.distanceFirstHouseIncrease = 3

        self.size = [area[3] - area[0], area[4] - area[1]]
        self.validHouseFloodFillPosition = [ self.buildArea[0] + self.size[0]/10, 
                                    self.buildArea[2] + self.size[1]/10, 
                                    self.buildArea[3] - self.size[0]/10,
                                    self.buildArea[5] - self.size[1]/10]
        self.minDistanceHouse = 4
        self.floodfillHouseSpace = 10

    """
    To get the height of a x,z position
    """
    def getHeight(self, x, z, ws):
        y = 255
        while self.is_air(x, y, z, ws) and y > 0:
            y -= 1
        return y

    """
    To know if it's a air block (or leaves and stuff)
    """
    def is_air(self, x, y, z, ws):   
        block = ws.getBlockAt(x, y - 1, z)
        if block in FloodFill.IGNORED_BLOCKS:
            #print("its air")
            return True
        else:
            #print("itsnotair")
            return False


    def is_ground(self, x, y, z, ws):
        y1 = y + 1
        y2 = y - 1
        #print(is_air(x,y2+1,z,ws) and not(is_air(x,y2,z,ws)))
        """ and not(ws.getBlockAt(x, y2, z)=='minecraft:water') """
        if self.is_air(x, y2 + 1, z, ws) and not(self.is_air(x, y2, z, ws)) :
            return y2 

        elif self.is_air(x, y1 + 1, z, ws) and not(self.is_air(x, y1, z, ws)):
            return y1
        elif self.is_air(x, y + 1, z, ws) and not(self.is_air(x, y, z, ws)):
            return y 
        else:
            return -1


    def floodfill(self, xi, yi, zi, ws, size):
        validPositions = []
        # if floodfill start is in building area
        if not _math.isPointInCube([xi, yi, zi], self.buildArea):
            print("Out of build area i ", xi, yi, zi)
            return validPositions

        stack = []
        stack.append((xi, yi, zi))

        toAdd = [[1, 0], [0, 1], [-1, 0], [0, -1]]
        floodFillArea = [xi - size, 0, zi - size, xi + size, 255, zi + size]

        while stack:
            Node = stack.pop()
            validPositions.append(Node)

            for add in toAdd:
                x = Node[0] + add[0]
                z = Node[2] + add[1]
                y = Node[1]
                if _math.isPointInCube([x, y, z], self.buildArea):
                    groundHeight = self.is_ground(x, y, z, ws)
                    if groundHeight != -1 and (x, groundHeight, z) not in validPositions and _math.isPointInCube([x, y, z], floodFillArea):
                        stack.append((x, groundHeight, z))

        return validPositions
 


    def verifHouse(self, xPos, yPos, zPos, CornerPos, ws):
        for i,j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
            if self.is_ground(xPos + CornerPos[i], yPos, zPos + CornerPos[j], ws) == -1:
                return False
                
        return True


    def takeRandomPosition(self, sizeStructure):
        xRange = 1 - self.startPosRange[0]
        zRange = 1 - self.startPosRange[1]


        lowLimit = int(self.buildArea[0] + abs(self.buildArea[0] * xRange) + sizeStructure )
        upperLimit = int(self.buildArea[3] - abs(self.buildArea[3] * xRange) - sizeStructure)

        xPos = random.randint(lowLimit, upperLimit)

        lowLimit = int(self.buildArea[2] + abs(self.buildArea[2] * zRange) + sizeStructure )
        upperLimit = int(self.buildArea[5] - abs(self.buildArea[5] * zRange) - sizeStructure)

        zPos = random.randint(lowLimit, upperLimit)

        return xPos, zPos 


    def takeNewPositionForHouse(self, sizeStruct):
        indices = list(range(0, len(self.listHouse)))

        while len(indices) > 0:
            index = random.randint(0, len(indices)-1)
        
            # Test if new houses position is in build Area
            if _math.isPointInSquare([self.listHouse[indices[index]][0], self.listHouse[indices[index]][2]], 
                [self.buildArea[0] + sizeStruct, self.buildArea[2] + sizeStruct, self.buildArea[3] - sizeStruct, self.buildArea[5] - sizeStruct]):
                placeindex = random.randint(0, len(self.listHouse[indices[index]][4]) - 1)

                if not isinstance(self.listHouse[indices[index]][4][placeindex], int):
                    return self.listHouse[indices[index]][4][placeindex]
                    
            del indices[index]
            
        return 0, 0, 0

    def findPosHouse(self, CornerPos, ws):
        sizeStruct = max(abs(CornerPos[0][0]) + abs(CornerPos[0][2]) + 1, abs(CornerPos[0][1]) + abs(CornerPos[0][3]) + 1)

        notFinded = True
        debug = 25 * 12
        debugNoHouse = 5
        verifCorners = False
        verifOverlapseHouse = False

        print("there is already", len(self.listHouse), "placed")

        while notFinded and debug and debugNoHouse and not verifCorners:
            if len(self.listHouse) == 0:
                xPos, zPos = self.takeRandomPosition(sizeStruct)

                yPos = self.getHeight(xPos, zPos, ws)
                if (ws.getBlockAt(xPos, yPos, zPos) == 'minecraft:water'):
                    continue

                print("starting position :" ,xPos, yPos, zPos)

                fliptest = [0, 1, 2, 3]
                while fliptest and notFinded:
                    rand1 = fliptest[random.randint(0, len(fliptest) - 1)]

                    fliptest.remove(rand1)
                    rotationtest = [0, 1, 2, 3]
                    while rotationtest and notFinded: 
                        rand2 = rotationtest[random.randint(0, len(rotationtest) - 1)]
                        rotationtest.remove(rand2)

                        choosenCorner = CornerPos[rand1 * 4 + rand2]

                        if self.verifHouse(xPos, yPos, zPos, choosenCorner, ws):
                            notFinded = False
                            # To be sure the place is large enough to build the village
                            FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, self.distanceFirstHouse)   
                                
                            if len(FloodFillValue) > 5000:
                                FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, sizeStruct + self.floodfillHouseSpace)
                            else:
                                notFinded = True
                                debugNoHouse -= 1
            else:
                verifOverlapseHouse = False
                verifCorners = False
                while not verifCorners and debug:
                    xPos, yPos, zPos = self.takeNewPositionForHouse(sizeStruct)

                    #to get a random flip and rotation and to test if one is possible
                    if (ws.getBlockAt(xPos, yPos, zPos)=='minecraft:water'):  
                        continue
                        
                    fliptest = [0, 1, 2, 3]
                    while fliptest and notFinded:
                        rand1 = fliptest[random.randint(0,len(fliptest)-1)]
                        fliptest.remove(rand1)
                        rotationtest = [0, 1, 2, 3]
                        while rotationtest and notFinded: 
                            rand2 = rotationtest[random.randint(0,len(rotationtest)-1)]
                            choosenCorner = CornerPos[rand1 * 4 + rand2]
                            rotationtest.remove(rand2)
                            if self.verifHouse(xPos, yPos, zPos, choosenCorner, ws):
                                verifCorners = True
                                listverifhouse = self.listHouse.copy()
                                while listverifhouse and verifCorners:
                                    house = listverifhouse.pop()
                                    if not _math.isTwoRectOverlapse([xPos, zPos], choosenCorner, [house[0], house[2]], house[3], self.minDistanceHouse):
                                        verifOverlapseHouse = True
                                    else:
                                        """print("N " + str(xPos) + " " + str(zPos) + " " + str(choosenCorner) +  " : flip " + str(rand1) + 
                                             ", rot " + str(rand2) + " ::" + str(house[0]) + " " + str(house[2]))"""
                                        verifOverlapseHouse = False
                                        verifCorners = False
                                        debug -= 1

                                if verifCorners and verifOverlapseHouse:
                                    print("Y " + str(xPos) + " " + str(zPos) + " " + str(choosenCorner) + " : flip " + str(rand1) + 
                                        ", rot " + str(rand2) + " ::" + str(house[0]) + " " + str(house[2]))
                                    notFinded = False

                                    # If house is valid to create a floodfill
                                    if _math.isPointInSquare([xPos, zPos], self.validHouseFloodFillPosition):
                                        FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, sizeStruct + self.floodfillHouseSpace)
                                        
                                    else:
                                        FloodFillValue = [xPos, yPos, zPos]
                                        
                                
                            else:
                                verifCorners = False
                                debug -=1

                
        if debug <= 0:
            dictionnary = {"position" : [xPos, yPos, zPos] , "validPosition" : False , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
            
            FloodFillValue = [xPos, yPos, zPos]
            print("debug failed")
        else:
            self.listHouse.append((xPos, yPos, zPos, choosenCorner, FloodFillValue))
            dictionnary = {"position" : [xPos, yPos, zPos],"validPosition" : True , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
        return dictionnary
