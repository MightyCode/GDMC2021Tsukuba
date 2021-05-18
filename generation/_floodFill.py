import random
import math

class FloodFill:
    
    # Ignoreblockvalue is the list of block that we want to ignore when we read the field
    IGNORED_BLOCKS = [
        'minecraft:air', 'minecraft:cave_air', 'minecraft:water', 
        'minecraft:oak_leaves',  'minecraft:leaves',  'minecraft:birch_leaves', 'minecraft:spruce_leaves'
        'minecraft:oak_log',  'minecraft:spruce_log',  'minecraft:birch_log',  'minecraft:jungle_log', 'minecraft:acacia_log', 'minecraft:dark_oak_log',
        'minecraft:grass', 'minecraft:snow',
        'minecraft:dead_bush', "minecraft:cactus"]

    def __init__(self):
        self.listHouse = []
        random.seed(a=None, version=2)


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


#a tester : dernier truc sur la derniere map : floodfill()

    def floodfill(self, xi, yi, zi, ws,taille):
        print("initialising floodfill in",xi,yi,zi, "for",taille)
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
        return valide
 


    def verifHouse(self, xPos, yPos, zPos, CornerPos,ws):
        ok=[0,0,0,0]
        print(CornerPos)
        for i in [0,1,2,3]:
            print(CornerPos[i][0],CornerPos[i][2])
            if self.is_ground(xPos + CornerPos[i][0],yPos,zPos + CornerPos[i][2],ws):
                ok[i] = 1
                print(i,"bon")
        if ok[0] == 1 and ok[1] == 1 and ok[2] == 1 and ok[3] == 1:
            print("true")
            return True
        else:
            print("false")
            return False

    def compareHouse(self,xPos,zPos,CornerPos,house):
        print("corner :",xPos,zPos,CornerPos)
        print("house",house[0],house[1],house[2],house[3])
        if xPos + CornerPos[3][0] +4 < house[0]+house[3][0][0] or xPos + CornerPos[0][0] -4 > house[0]+house[3][3][0] or zPos + CornerPos[0][2] -4 > house[2]+house[3][3][2] or zPos + CornerPos[2][2] +4 < house[2]+house[3][0][2] :
            return True
        else:
            return False



    def findPosHouse(self, CornerPos, ws):
        notfinded = True
        debug = 5
        debugnohouse = 5
        verif1 = False
        verif2 = False
        while notfinded and debug and debugnohouse and verif1==False:
            if len(self.listHouse)==0:
                xPos = (-1)**random.randint(0,1) * random.randint(0,90)
                zPos = (-1)**random.randint(0,1) * random.randint(0,90)
                print(xPos, zPos)
                yPos = self.getHeight(xPos,zPos, ws)
                print(yPos)
                if ws.getBlockAt((xPos,yPos,zPos))=='minecraft:water':
                    print("this position is air or water")
                    print("retrying")
                else:
                    #self.floodfill(xPos,yPos,zPos,ws,15)
                    fliptest = [0,1,2,3]
                    while fliptest and notfinded:
                        rand1 = fliptest[random.randint(0,len(fliptest)-1)]
                        fliptest.remove(rand1)
                        rotationtest = [0,1,2,3]
                        while rotationtest and notfinded: 
                            rand2 = rotationtest[random.randint(0,len(rotationtest)-1)]
                            rotationtest.remove(rand2)
                            print("trying flip : ",rand1,"with rotation :", rand2)
                            print(CornerPos)
                            print(CornerPos[rand1*4 + rand2])
                            if self.verifHouse(xPos,yPos,zPos,CornerPos[rand1*4 + rand2],ws):
                                print("trying to find a place large enough")
                                notfinded = False
                                FloodFillValue=self.floodfill(xPos,yPos,zPos,ws,60)
                                if len(FloodFillValue) > 7000:
                                    print(len(FloodFillValue))
                                    print("it's large enough")
                                    FloodFillValue=self.floodfill(xPos,yPos,zPos,ws,35)
                                else:
                                    print("trying to find somewhere larger")
                                    notfinded = True
                                    debugnohouse-=1
                            else:
                                print("neednewposition")   
            else:
                debug = 25
                verif1 = False
                verif2 = False
                print("test")
                while verif1 == False and verif2 == False and debug:
                    print("there is already",len(self.listHouse),"placed")
                    index = random.randint(0,len(self.listHouse)-1)
                    print(abs(self.listHouse[index][0]),abs(self.listHouse[index][2]))
                    if abs(self.listHouse[index][0]) > 110 or abs(self.listHouse[index][2]) > 110:
                        print("out of bound, retrying ...")
                    else:
                        #FloodFillValue = self.floodfill(self.listHouse[index][0],self.listHouse[index][1],self.listHouse[index][2],ws,40)
                        placeindex = random.randint(0,len(self.listHouse[index][4])-1)
                        xPos = self.listHouse[index][4][placeindex][0]
                        yPos = self.listHouse[index][4][placeindex][1]
                        zPos = self.listHouse[index][4][placeindex][2]
                        print(xPos,yPos,zPos, "is the position i want to build on")
                        if ws.getBlockAt((xPos,yPos,zPos))=='minecraft:water':
                            print("it's air")
                        else:
                            print(CornerPos)
                            #FloofFillValue = self.floodfill(xPos,yPos,zPos,ws,20)
                            fliptest = [0,1,2,3]
                            while fliptest and notfinded:
                                rand1 = fliptest[random.randint(0,len(fliptest)-1)]
                                fliptest.remove(rand1)
                                rotationtest = [0,1,2,3]
                                while rotationtest and notfinded: 
                                    rand2 = rotationtest[random.randint(0,len(rotationtest)-1)]
                                    rotationtest.remove(rand2)
                                    print("trying flip : ",rand1,"with rotation :", rand2)
                                    #print(CornerPos)
                                    print(CornerPos[rand1*4 + rand2])
                                    if self.verifHouse(xPos,yPos,zPos,CornerPos[rand1*4 + rand2],ws):
                                        verif1 = True
                                        print("First Verification worked")
                                        listverifhouse=self.listHouse.copy()
                                        house = listverifhouse.pop()
                                        while listverifhouse:
                                            
                                            #print(house)
                                            if self.compareHouse(xPos,zPos,CornerPos[rand1*4 + rand2],house):
                                                print("this place is acceptable to be placed on")
                                                verif2 = True
                                            else:
                                                verif2 = False
                                                verif1 = False
                                                print("need a new position")
                                                debug-=1
                                            house = listverifhouse.pop()
                                        #print(house)
                                        if self.compareHouse(xPos,zPos,CornerPos[rand1*4 + rand2],house):
                                            #print(house)
                                            print("this place is acceptable to be placed on")
                                            verif2 = True
                                        else:
                                            verif2 = False
                                            verif1 = False
                                            print("need a new position")
                                            debug-=1
                                            print(debug,"try left")
                                        #print(listverifhouse)
                                        print(verif1,verif2)
                                        if verif1 and verif2:
                                            notfinded = False
                                            if xPos > 120 or yPos > 120:
                                                FloodFillValue = [xPos,yPos,zPos]
                                            else:
                                                FloodFillValue = self.floodfill(xPos,yPos,zPos,ws,35)
                                        
                                    else:
                                        verif1 = False
                                        debug-=1
                                        print(debug,"try left")
                                        print("first verification echec")


                

        if debug == 0:
            xPos=self.listHouse[index][0]
            yPos=self.listHouse[index][1]
            zPos=self.listHouse[index][2]
            dictionnary = {"position" : [xPos,yPos,zPos] , "validPosition" : False , "flip" : rand1 , "rotation" : rand2}
            
            FloodFillValue = [xPos,yPos,zPos]
            print("debug failed")
        else:
            self.listHouse.append((xPos,yPos,zPos,CornerPos[rand1*4 + rand2],FloodFillValue))
            dictionnary = {"position" : [xPos,yPos,zPos],"validPosition" : True , "flip" : rand1 , "rotation" : rand2}
            print(dictionnary)
        return dictionnary

                      
