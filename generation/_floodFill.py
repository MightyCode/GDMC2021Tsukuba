import utils._math as _math
import random
import lib.interfaceUtils as iu
import generation.road as road

class FloodFill:
    
    # Ignoreblockvalue is the list of block that we want to ignore when we read the field
    IGNORED_BLOCKS = [
        'minecraft:void_air', 'minecraft:air', 'minecraft:cave_air', 'minecraft:water','minecraft:dark_oak_leaves','minecraft:redstone_lamp','minecraft:cobblestone_wall',
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves','minecraft:vine'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow','minecraft:acacia_leaves','minecraft:tall_grass','minecraft:poppy','minecraft:dandelion','minecraft:brown_mushroom_block','minecraft:mushroom_stem','minecraft:rose_bush','minecraft:red_mushroom_block',
        'minecraft:dead_bush', "minecraft:cactus"]

    def __init__(self, area):
        self.numberOfDecoration = 50
        self.listHouse = []
        random.seed(a=None, version=2)
        self.buildArea = area
        self.startPosRange = [0.89, 0.89]

        self.distanceFirstHouse = 40
        self.distanceFirstHouseIncrease = 3

        self.size = [area[3] - area[0], area[5] - area[2]]
        self.validHouseFloodFillPosition = [ self.buildArea[0] + self.size[0]/10, 
                                    self.buildArea[2] + self.size[1]/10, 
                                    self.buildArea[3] - self.size[0]/10,
                                    self.buildArea[5] - self.size[1]/10]
        self.minDistanceHouse = 4
        self.floodfillHouseSpace = 10
        self.previousStructure = -1

    """
    To get the height of a x,z position
    """
    def getHeight(self, x, z):
        y = 255
        while self.is_air(x, y, z) and y > 0:
            y -= 1
        return y


    """
    to get the height of a x,z posisition and taking water and lava in it
    """
    def getHeightRoad(self, x, z):
        y = 255
        while self.is_air(x, y, z) and y > 0 and not (iu.getBlock(x, y - 1, z)=="minecraft:water" or iu.getBlock(x, y - 1, z) == "minecraft:lava"):
            y -= 1

        return y

    """
    To know if it's a air block (or leaves and stuff)
    """
    def is_air(self, x, y, z):
        try:
            block = iu.getBlock(x, y - 1, z)
            if block in FloodFill.IGNORED_BLOCKS:
                #print("its air")
                return True
            else:
                #print("itsnotair")
                return False
        except IndexError:
            print("indexError")
        return False

        





    def is_ground(self, x, y, z):
        y1 = y + 1
        y2 = y - 1
        #print(is_air(x,y2+1,z,ws) and not(is_air(x,y2,z,ws)))
        """ and not(ws.getBlockAt(x, y2, z)=='minecraft:water') """
        try:
            if iu.getBlock(x,y,z)=='minecraft:lava':
                iu.setBlock(x,y,z,'minecraft:obsidian')
            if iu.getBlock(x,y1,z)=='minecraft:lava':
                iu.setBlock(x,y1,z,'minecraft:obsidian')
            if iu.getBlock(x,y2,z)=='minecraft:lava':
                iu.setBlock(x,y2,z,'minecraft:obsidian')
        except IndexError:
            print("IndexError")

        if self.is_air(x, y2 + 1, z) and not(self.is_air(x, y2, z)) :
            return y2 

        elif self.is_air(x, y1 + 1, z) and not(self.is_air(x, y1, z)):
            return y1
        elif self.is_air(x, y + 1, z) and not(self.is_air(x, y, z)):
            return y 
        else:
            return -1


    def floodfill(self, xi, yi, zi, size):
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
            #iu.setBlock(Node[0],Node[1]-1,Node[2],"minecraft:bricks")
            for add in toAdd:
                x = Node[0] + add[0]
                z = Node[2] + add[1]
                y = Node[1]
                if _math.isPointInCube([x, y, z], self.buildArea):
                    try:
                        groundHeight = self.is_ground(x, y, z)
                    except IndexError:
                        print("indexerror")
                        print(x,y,z)
                    if groundHeight != -1 and (x, groundHeight, z) not in validPositions and _math.isPointInCube([x, y, z], floodFillArea):
                        stack.append((x, groundHeight, z))

        return validPositions
 


    def verifHouse(self, xPos, yPos, zPos, CornerPos):
        for i,j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
            if self.is_ground(xPos + CornerPos[i], yPos, zPos + CornerPos[j]) == -1:
                return False
                
        return True


    def takeRandomPosition(self, sizeStructure):
        xRange = 1 - self.startPosRange[0]
        zRange = 1 - self.startPosRange[1]


        lowLimit = int(self.buildArea[0] + self.size[0] * xRange + sizeStructure )
        upperLimit = int(self.buildArea[3] - self.size[0] * xRange - sizeStructure)
        xPos = random.randint(lowLimit, upperLimit)

        lowLimit = int(self.buildArea[2] + self.size[1] * zRange + sizeStructure )
        upperLimit = int(self.buildArea[5] - self.size[1] * zRange - sizeStructure)
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
                    self.previousStructure = indices[index]
                    return self.listHouse[indices[index]][4][placeindex]
                    
            del indices[index]
            
        return 0, 0, 0

    def isInHouse(self,coord):
        listverifhouse = self.listHouse.copy()
        while listverifhouse:
            house = listverifhouse.pop()
            if _math.isPointInSquare(coord,[house[0] + house[3][0], house[2] + house[3][1], house[0] + house[3][2], house[2] + house[3][3]]):
                return True
        return False


    def decideMinMax(self):
        listverifhouse = self.listHouse.copy()
        if listverifhouse:
            house = listverifhouse.pop()
            xmin = house[0]
            xmax = xmin
            zmin = house[2]
            zmax = zmin
        while listverifhouse:
            house = listverifhouse.pop()
            if house[0] < xmin:
                xmin = house[0]
            if house[2] < zmin:
                zmin = house[2]
            if house[0] > xmax:
                xmax = house[0]
            if house[2] > zmax:
                zmax = house[2]
        print("range of the village is : ", xmin, xmax, zmin, zmax)
        return xmin, xmax, zmin, zmax

    def placeDecorations(self):
        xmin, xmax, zmin,zmax = self.decideMinMax()
        decorationcoord = []
        for i in range(self.numberOfDecoration):
            decoput = False
            debug = 15
            while not decoput and debug > 0:

                xrand = random.randint(xmin,xmax)
                zrand = random.randint(zmin,zmax)
                if not self.isInHouse([xrand,zrand]):
                    if not road.isInRoad([xrand,zrand]):
                        print("deco n :",i, "placed in ",xrand,zrand)
                        iu.setBlock(xrand,self.getHeight(xrand,zrand),zrand,"minecraft:hay_block")
                        decoput = True
                debug -= 1




    def findPosHouse(self, CornerPos):
        sizeStruct = max(abs(CornerPos[0][0]) + abs(CornerPos[0][2]) + 1, abs(CornerPos[0][1]) + abs(CornerPos[0][3]) + 1)

        notFinded = True
        debug = 250 * 16
        debugNoHouse = 250 * 16
        verifCorners = False
        verifOverlapseHouse = False
        print("there is already", len(self.listHouse), "placed")

        while notFinded and (debug>0) and (debugNoHouse>0) and not verifCorners:
            if len(self.listHouse) == 0:
                xPos, zPos = self.takeRandomPosition(sizeStruct)

                yPos = self.getHeight(xPos, zPos)
                if (iu.getBlock(xPos, yPos, zPos) == 'minecraft:water'):
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

                        if self.verifHouse(xPos, yPos, zPos, choosenCorner):
                            notFinded = False
                            # To be sure the place is large enough to build the village
                            FloodFillValue = self.floodfill(xPos, yPos, zPos, self.distanceFirstHouse)   
                                
                            if len(FloodFillValue) > 5000:
                                FloodFillValue = self.floodfill(xPos, yPos, zPos, sizeStruct + self.floodfillHouseSpace)
                            else:
                                notFinded = True
                                debugNoHouse -= 1
            else:
                verifOverlapseHouse = False
                verifCorners = False

                while not verifCorners and (debug>0):
                    xPos, yPos, zPos = self.takeNewPositionForHouse(sizeStruct)
                    #to get a random flip and rotation and to test if one is possible
                    if (iu.getBlock(xPos, yPos, zPos)=='minecraft:water'):  
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
                            if self.verifHouse(xPos, yPos, zPos, choosenCorner):
                                verifCorners = True
                                listverifhouse = self.listHouse.copy()
                                while listverifhouse and verifCorners:
                                    house = listverifhouse.pop()
                                    if not house[6]:
                                        continue

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
                                        FloodFillValue = self.floodfill(xPos, yPos, zPos,  sizeStruct + self.floodfillHouseSpace)
                                        
                                    else:
                                        FloodFillValue = [xPos, yPos, zPos]
                                        
                                
                            else:
                                verifCorners = False
                                debug -=1

                
        if debug <= 0:
            dictionnary = {"position" : [xPos, yPos, zPos] , "validPosition" : False , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
            FloodFillValue = [xPos, yPos, zPos]
            self.listHouse.append((xPos, yPos, zPos, choosenCorner, FloodFillValue, -1, False))
            
            print("debug failed")
        else:
            self.listHouse.append((xPos, yPos, zPos, choosenCorner, FloodFillValue, self.previousStructure, True))
            dictionnary = {"position" : [xPos, yPos, zPos],"validPosition" : True , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
        return dictionnary
