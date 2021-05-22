import random
import utils._math as _math

class FloodFill:
    
    # Ignoreblockvalue is the list of block that we want to ignore when we read the field
    IGNORED_BLOCKS = [
        'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow',
        'minecraft:dead_bush', "minecraft:cactus"]

    def __init__(self, area):
        self.listHouse = []
        random.seed(a=None, version=2)
        self.area = area
        self.startPosRange = [0.85, 0.85]

        self.distanceFirstHouse = 40
        self.distanceFirstHouseIncrease = 3

        self.size = [area[3] - area[0], area[4] - area[1]]
        self.minDistanceHouse = 4
        self.floodfillHouseSpace = 10

    """
    To get the height of a x,z position
    """
    def getHeight(self, x, z, ws): #
        y = 255
        while self.is_air(x, y, z, ws) and y > 0:
            #print(y)
            y -= 1
        #y-=1
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
        """ and not(ws.getBlockAt((x, y2, z))=='minecraft:water') """
        if self.is_air(x, y2 + 1, z, ws) and not(self.is_air(x, y2, z, ws)) :
            return y2 

        elif self.is_air(x, y1 + 1, z, ws) and not(self.is_air(x, y1, z, ws)):
            return y1
        elif self.is_air(x, y + 1, z, ws) and not(self.is_air(x, y, z, ws)):
            return y 
        else:
            return 0


    def floodfill(self, xi, yi, zi, ws, size):
        #print("initialising floodfill in", xi, yi, zi, "for", taille)
        #print(xi, yi, zi)
        stack = []
        valide = []
        stack.append((xi, yi, zi))
        while stack:
            Node = stack.pop()
            valide.append(Node)
            x = Node[0]
            z = Node[2]
            y = Node[1]
            #print(x,y,z)
            y1 = self.is_ground(x + 1, y, z, ws)
            if y1 and (x + 1, y1, z) not in valide and x < self.area[2]:
                stack.append((x + 1, y1, z))

            #---------------
            y2 = self.is_ground(x, y, z + 1, ws)
            if y2 and (x, y2, z + 1) not in valide and z < self.area[3]:
                stack.append((x, y2, z + 1))
            #---------------
            y3 = self.is_ground(x - 1, y, z, ws)
            if y3 and (x - 1, y3, z) not in valide and x > self.area[0]:
                stack.append((x - 1, y3, z))
            #---------------
            y4 = self.is_ground(x, y , z - 1,ws)
            if y4 and (x, y4 ,z - 1) not in valide and z > self.area[1]:
                stack.append((x, y4 , z - 1))
        return valide
 


    def verifHouse(self, xPos, yPos, zPos, CornerPos, ws):
        for i,j in [[0, 1], [2, 1], [0, 3], [2, 3]]:
            if not self.is_ground(xPos + CornerPos[i], yPos, zPos + CornerPos[j], ws):
                return False
                
        return True


    def takeRandomPosition(self, sizeStructure):
        xRange = 1 - self.startPosRange[0]
        zRange = 1 - self.startPosRange[1]


        lowLimit = int(self.area[0] + abs(self.area[0] * xRange) + sizeStructure )
        upperLimit = int(self.area[3] - abs(self.area[3] * xRange) - sizeStructure)

        xPos = random.randint(lowLimit, upperLimit)

        lowLimit = int(self.area[2] + abs(self.area[2] * zRange) + sizeStructure )
        upperLimit = int(self.area[5] - abs(self.area[5] * zRange) - sizeStructure)

        zPos = random.randint(lowLimit, upperLimit)

        return xPos, zPos 

    def findPosHouse(self, CornerPos, ws):
        sizeStruct = max(abs(CornerPos[0][0]) + abs(CornerPos[0][2]) + 1, abs(CornerPos[0][1]) + abs(CornerPos[0][3]) + 1)

        notfinded = True
        debug = 25 * 12
        debugnohouse = 5
        verifCorners = False
        verifOverlapseHouse = False

        print("there is already", len(self.listHouse), "placed")

        while notfinded and debug and debugnohouse and not verifCorners:
            if len(self.listHouse) == 0:
                xPos, zPos = self.takeRandomPosition(sizeStruct)
                #print("starting position :" ,xPos, zPos)
                yPos = self.getHeight(xPos, zPos, ws)
                #print(yPos)
                if not(ws.getBlockAt(xPos, yPos, zPos) == 'minecraft:water'):

                    fliptest = [0, 1, 2, 3]
                    while fliptest and notfinded:
                        rand1 = fliptest[random.randint(0, len(fliptest) - 1)]

                        fliptest.remove(rand1)
                        rotationtest = [0, 1, 2, 3]
                        while rotationtest and notfinded: 
                            rand2 = rotationtest[random.randint(0, len(rotationtest) - 1)]
                            rotationtest.remove(rand2)

                            choosenCorner = CornerPos[rand1 * 4 + rand2]

                            if self.verifHouse(xPos, yPos, zPos, choosenCorner, ws):
                                notfinded = False
                                # To be sure the place is large enough to build the village
                                FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, self.distanceFirstHouse)   
                                
                                if len(FloodFillValue) > 5000:
                                    FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, sizeStruct + self.floodfillHouseSpace)
                                else:
                                    notfinded = True
                                    debugnohouse -= 1
            else:
                verifOverlapseHouse = False
                verifCorners = False
                while not verifCorners and debug:
                    
                    index = random.randint(0, len(self.listHouse)-1)
                    
                    # Test if new houses position is in build Area
                    if _math.isPointInSquare([self.listHouse[index][0], self.listHouse[index][2]], 
                            [self.area[0] + sizeStruct, self.area[2] + sizeStruct, self.area[3] - sizeStruct, self.area[5] - sizeStruct]):

                        placeindex = random.randint(0, len(self.listHouse[index][4]) - 1)
                        xPos = self.listHouse[index][4][placeindex][0]
                        yPos = self.listHouse[index][4][placeindex][1]
                        zPos = self.listHouse[index][4][placeindex][2]

                        #to get a random flip and rotation and to test if one is possible
                        if not(ws.getBlockAt((xPos, yPos, zPos))=='minecraft:water'):  
                            fliptest = [0, 1, 2, 3]
                            while fliptest and notfinded:
                                rand1 = fliptest[random.randint(0,len(fliptest)-1)]
                                fliptest.remove(rand1)

                                rotationtest = [0, 1, 2, 3]
                                while rotationtest and notfinded: 
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
                                            notfinded = False
                                            if not _math.isPointInSquare([self.listHouse[index][0], self.listHouse[index][2]], 
                                                [self.area[0] + self.size/10, self.area[2] + self.size/10, self.area[3] - self.size/10, self.area[5] - self.size/10]):
                                                FloodFillValue = [xPos, yPos, zPos]
                                            else:
                                                FloodFillValue = self.floodfill(xPos, yPos, zPos, ws, sizeStruct + self.floodfillHouseSpace)
                                        
                                    else:
                                        verifCorners = False
                                        debug -=1

                
        if debug <= 0:
            xPos = self.listHouse[index][0]
            yPos = self.listHouse[index][1]
            zPos = self.listHouse[index][2]
            dictionnary = {"position" : [xPos, yPos, zPos] , "validPosition" : False , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
            
            FloodFillValue = [xPos, yPos, zPos]
            print("debug failed")
        else:
            self.listHouse.append((xPos, yPos, zPos, choosenCorner, FloodFillValue))
            dictionnary = {"position" : [xPos, yPos, zPos],"validPosition" : True , "flip" : rand1 , "rotation" : rand2, "corner" : choosenCorner }
        return dictionnary

                      
