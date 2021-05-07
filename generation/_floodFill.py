import random
import math

class FloodFill:
    
    # Ignoreblockvalue is the list of block that we want to ignore when we read the field
    IGNORED_BLOCKS = ['minecraft:air', 'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves',
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log',
        'minecraft:dark_oak_log','minecraft:water','minecraft:grass','minecraft:cave_air','minecraft:snow']

    def __init__(self):
        self.lists = []
        self.listHouse = []

    def getHeight(self, x, z, ws): #to get the height of a x,z position
        y = 255
        while self.is_air(x, y, z, ws):
            #print(y)
            y -= 1
        #y-=1
        return y


    def is_air(self, x, y, z, ws):   #to know if it's a air block (or leaves and stuff)
        block = ws.getBlockAt((x, y-1, z))
        if block in FloodFill.IGNORED_BLOCKS:
            #print("its air")
            return True
        else:
            #print("itsnotair")
            return False


    def is_ground(self,x,y,z, ws):
        y1 = y+1
        y2 = y-1
        #print(is_air(x,y2+1,z,ws) and not(is_air(x,y2,z,ws)))
        if self.is_air(x, y2 + 1, z, ws) and not(self.is_air(x, y2, z, ws)) and not(ws.getBlockAt((x, y2, z))=='minecraft:water'):
            return y2 

        elif self.is_air(x, y1+1, z, ws) and not(self.is_air(x, y1, z, ws)) and not(ws.getBlockAt((x, y1, z))=='minecraft:water'):
            return y1
        elif self.is_air(x, y+1, z, ws) and not(self.is_air(x, y, z, ws)) and not(ws.getBlockAt((x, y, z))=='minecraft:water'):
            return y 
        else:
            return 0


    def floodfill(self, xi, yi, zi, ws,taille):
        print("initialising floodfill")
        print(xi,yi,zi)
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
            y1 = self.is_ground(x+1,y,z,ws)
            if y1 and (x+1,y1,z) not in valide and x <xi+taille:
                stack.append((x+1,y1,z))

            #---------------
            y2 = self.is_ground(x,y,z+1,ws)
            if y2 and (x,y2,z+1) not in valide and z<zi+taille:
                stack.append((x,y2,z+1))
            #---------------
            y3 = self.is_ground(x-1,y,z,ws)
            if y3 and (x-1,y3,z) not in valide and x>xi-taille:
                stack.append((x-1,y3,z))
            #---------------
            y4 = self.is_ground(x,y,z-1,ws)
            if y4 and (x,y4,z-1) not in valide and z>zi-taille:
                stack.append((x,y4,z-1))
        #print(valide)
        self.lists = valide
        #for z in valide:
        #    self.setBlock(z[0],z[1] -1,z[2],"minecraft:bricks")
        #it's recursive and not working in python atm because there is too much recursion
#        if ([x,y,z] in self.lists) != 1 and (abs(x)<40 and abs(z)<40):
#            self.setBlock(x,y,z,"minecraft:bricks")
#            self.lists = self.lists + [[x, y, z]]
#            #------------------
#            y1 = is_ground(x+1, y, z, ws)
#            if y1:
#                self.floodfill(x+1, y1, z,ws)
#            #---------------------
#            y2 = is_ground(x, y, z+1, ws)
#            if y2:
#                self.floodfill(x, y2, z+1,ws)
#            #---------------------
#            y3 = is_ground(x-1, y, z, ws)
#            if y3:
#                self.floodfill(x-1, y3, z,ws)
#            #---------------------
#            y4 = is_ground(x, y, z-1, ws)
#            if y4:
#                self.floodfill(x, y4, z-1,ws) 


    def verifHouse(self, xPos, yPos, zPos, CornerPos):
        ok=[0,0,0,0]

        for i in [0,1,2,3]:
            print(CornerPos[i][0],CornerPos[i][1])
            if (xPos + CornerPos[i][0], yPos ,  zPos + CornerPos[i][1]) in self.lists or (xPos + CornerPos[i][0], yPos -1 ,  zPos + CornerPos[i][1]) in self.lists or (xPos + CornerPos[i][0], yPos +1 ,  zPos + CornerPos[i][1]) in self.lists or (xPos + CornerPos[i][0], yPos +2 ,  zPos + CornerPos[i][1]) in self.lists or (xPos + CornerPos[i][0], yPos -2 ,  zPos + CornerPos[i][1]) in self.lists:
                ok[i] = 1
                print(i,"bon")
        if ok[0] == 1 and ok[1] == 1 and ok[2] == 1 and ok[3] == 1:
            print("true")
            return True
        else:
            print("false")
            return False

    def compareHouse(self,xPos,zPos,CornerPos,house):
        ok = [[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]]
        #for i in [0,1,2,3]:
        #    for j in [0,1,2,3]:

                #if (xPos+CornerPos[i][0])>(house[j][0]+house[j][3][1][0]) and (xPos+CornerPos[i][0]) A FINIR
            
        if True:
            return True
        else:
            return False



    def findPosHouse(self, CornerPos, ws):
        notfinded = True
        debug = 5
        debugnohouse = 5
        verif1 = False
        verif2 = False
        while notfinded and debug and debugnohouse:
            if len(self.listHouse)==0:
                xPos = -1**random.randint(0,1) * random.randint(0,150)
                zPos = xPos = -1**random.randint(0,1) * random.randint(0,150)
                yPos = self.getHeight(xPos,zPos, ws)
                if self.is_air(xPos,yPos,zPos,ws):
                    print("this position is air or water")
                    print("retrying")
                else:
                    self.floodfill(xPos,yPos,zPos,ws,15)
                    if self.verifHouse(xPos,yPos,zPos,CornerPos):
                        print("trying to find a place large enough")
                        notfinded = False
                        self.floodfill(xPos,yPos,zPos,ws,60)
                        if len(self.lists) > 6000:
                            print(len(self.lists))
                            print("it's large enough")
                        else:
                            print("trying to find somewhere larger")
                            notfinded = True
                            debugnohouse-=1
                    else:
                        print("neednewposition")
                    
            else:
                while verif1 == False and verif2 == False and debug:
                    print("there is already",len(self.listHouse),"placed")
                    index = random.randint(0,len(self.listHouse)-1)
                    self.floodfill(self.listHouse[index][0],self.listHouse[index][1],self.listHouse[index][2],ws,15)
                    placeindex = random.randint(0,len(self.lists)-1)
                    xPos = self.lists[placeindex][0]
                    yPos = self.lists[placeindex][1]
                    zPos = self.lists[placeindex][2]
                    print(xPos,yPos,zPos, "is the position i want to build on")

                    if self.verifHouse(xPos,yPos,zPos,CornerPos):
                        verif1 = True
                        print("First Verification worked")
                        listverifhouse=self.listHouse.copy()
                        print(listverifhouse)
                        while listverifhouse:
                            house = listverifhouse.pop()
                            print(house)
                            if self.compareHouse(xPos,zPos,CornerPos,house):
                                print("this place is acceptable to be placed on")
                                verif2 = True
                            else:
                                verif2 = False
                                verif1 = False
                                print("need a new position")
                                debug-=1
                            print(listverifhouse)
                        if verif1 and verif2:
                            notfinded = False
                        
                    else:
                        verif1 = False
                        print("first verification echec")


                

        if debug == 0:
            xPos=0
            yPos=0
            zPos=0
            print("debug failed")
        else:
            self.listHouse.append((xPos,yPos,zPos,CornerPos))
        return [xPos,yPos,zPos]



"""        notfinded = True
        debug = 3
        while notfinded and debug:  #pour sortir de la boucle une fois qu'on a trouvé
            if len(self.listHouse)==0 and debug>0:
                print("no house already placed or new location needed")
                yPos = self.getHeight(0, 0, ws)
                self.floodfill(0, yPos, 0, ws, 40)
                notfinded2 = True
                while notfinded2 and debug:
                    start = random.randint(0, len(self.lists) - 1)
                    print(start)
                    print(self.lists[start])
                    if self.verifHouse(self.lists[start][0],self.lists[start][1],self.lists[start][2],CornerPos):
                        print("need another position")
                        notfinded2 = False
                    else:
                        debug-=1
                        print(debug, "try left")
                    xPos = self.lists[start][0]
                    yPos = self.lists[start][1]
                    zPos = self.lists[start][2]
                    self.listHouse.append((xPos,yPos,zPos))

            else:
                print("there is already " , len(self.listHouse) ,  "placed")
                index = random.randint(0,len(self.listHouse)-1)
                print(index)
                Away = random.randint(10,20)
                print(Away)
                angle = random.randint(0,359)
                print(angle)
                xPos = self.listHouse[index][0] + math.floor(Away * math.cos(angle))
                zPos = self.listHouse[index][2] + math.floor(Away * math.sin(angle))
                yPos = self.getHeight(xPos, zPos, ws)
                print((xPos,yPos,zPos))

                if self.is_air(xPos,yPos,zPos,ws):
                    notfinded = True
                    print("its air, new house position needed")
                else:
                    print("checking position")
                    NewHousePos = [xPos , yPos,  zPos]
                    self.floodfill(xPos,yPos,zPos,ws,10)
                    if self.verifHouse(xPos,yPos,zPos,CornerPos):
                        print("verified")
                        notfinded = False
                        for i in range(len(self.listHouse)):
                            if abs(xPos - self.listHouse[i][0]) < 8 and abs(zPos - self.listHouse[i][2]) <8:
                                notfinded = True
                                print("error")
                    else:
                        print("new position required")
                        debug -=1
                    #    print(debug , "try left")
        self.listHouse.append((xPos,yPos,zPos))

        print(xPos,yPos,zPos)
        return [xPos,yPos,zPos]
"""

                        
