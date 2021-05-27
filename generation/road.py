import random
import utils._math as _math
import lib.interfaceUtils as iu

NODE_IN_ROAD = []


class Node:
	def __init__(self,point):
		self.point = point
		self.parent = None
		self.cost = 0
		self.H = 0
	def move_cost(self,other):
		return 1

class logNode:
	def __init__(self,point):
		self.point = point
		self.child = None

def manhattan(point,point2):
	return abs(point.point[0] - point2.point[0]) + abs(point.point[1]-point2.point[1])

def children(point):
	x,z=point.point
	links = []
	for d in [(x-1,z),(x, z-1),(x, z + 1),(x+1,z)]:
		links.append(Node([d[0],d[1]]))

	return links

#house is : [x,y,z,CornerPos]
def squareOfHouse(house):
	return False


def comparenode(node1,node2):
	if node1.H < node2.H:
		return 1
	elif node1.H == node2.H:
		return 0
	else:
		return -1

def isInClosedList(node, closedlist):
	print("testing : ",node.point)
	for i in closedlist:
		print(i.point)
		if node.point == i.point:
			return True
	return False

def isInListWithInferiorCost(node, list):
	for i in list:
		if node.point == i.point:
			if i.H < node.H:
				return True
	return False

def isInRoad(coord):
	for index in NODE_IN_ROAD:
		if coord in index:
			return True
	return False


def Astar(startcoord,goalcoord,squarelist, floodFill):
	#the open and close set
	start = Node(startcoord)
	goal = Node(goalcoord)
	openlist = []
	closedlist = []
	#current point at start is the starting point
	current = start
	current.H = manhattan(current, goal)
	#add it to the openset
	openlist.append(current)

	while openlist:
		#find the item in the open set with the lowest G+H score
		temp = openlist[0].H
		for i in openlist:
			if i.H <= temp:
				temp = i.H
				current = i
		openlist.remove(current)
		#if we are at the goal

		if current.point == goal.point:
			path = [current.point]
			while current.parent:
				path.append(current.parent.point)
				current = current.parent
			NODE_IN_ROAD.append(path)
			return path[::-1] #to reverse the path
		#for every neighbourg of current node
		for node in children(current):
			#test here if the children is in a house
			notinsquare = True
			for squarehouse in squarelist:
				if _math.isPointInSquare(node.point, squarehouse):
					notinsquare = False
			#if abs(floodFill.getHeight(node.point[0],node.point[1],ws) - floodFill.getHeight(current.point[0],current.point[1],ws)) > 2:
			#	notinsquare = False

			if notinsquare:
				if not(isInClosedList(node, closedlist) or isInListWithInferiorCost(node, openlist)):
					print(node.point)
					node.cost = current.cost + 1
					node.H = node.cost + manhattan(node,goal)
					node.parent = current
					openlist.append(node)
		closedlist.append(current)
	raise ValueError('No Path Found')

LOGNAME = ['minecrat:oak_log','minecraft:spruce_log','minecraft:jungle_log','minecraft:acacia_log','minecraft:dark_oak_log','minecraft:birch_log']


def initRoad(floodFill, settlementData, worldmodif,  materials):
	ORIENTATION = {"north" : [ 0, -1 ], "south" : [ 0, 1 ], "west" : [ -1, 0 ], "east" : [ 1, 0 ]}
	#to 
	squarelist= []
	for index in range(0, len(settlementData["structures"])):
		entrytemp = []
		entrytemp.append(floodFill.listHouse[index][0])
		entrytemp.append(floodFill.listHouse[index][1]-1)
		entrytemp.append(floodFill.listHouse[index][2])
		squarelist.append([entrytemp[0] + floodFill.listHouse[index][3][0] , entrytemp[2] + floodFill.listHouse[index][3][1], 
			entrytemp[0] + floodFill.listHouse[index][3][2], entrytemp[2] + floodFill.listHouse[index][3][3]])
	#print(squarelist)
	for index in range(0,len(settlementData["structures"])):
		#to knwo if the house doesn't have parent...
		print("building path for house n :",index)
		start=[0, 0]
		goal=[0, 0]
		index2 = floodFill.listHouse[index][5]
		if not index2 == -1:
			facingenfant = settlementData["structures"][index]["prebuildingInfo"]["entry"]["facing"]
			entry1 = []
			entry1.append(floodFill.listHouse[index][0])
			entry1.append(floodFill.listHouse[index][1]-1)
			entry1.append(floodFill.listHouse[index][2])
			x = entry1[0] + ORIENTATION[facingenfant][0]
			y = entry1[1]
			z = entry1[2] + ORIENTATION[facingenfant][1]
			while not(floodFill.is_air(x, y+2, z)) or floodFill.is_air(x, y+1, z):
						if floodFill.is_air(x, y + 1, z):
							y -=1
						if not(floodFill.is_air(x, y + 2, z)):
							y += 1
			worldmodif.setBlock(x, y, z, "minecraft:grass_path")
			x += ORIENTATION[facingenfant][0]
			z += ORIENTATION[facingenfant][1]
			while not(floodFill.is_air(x, y+2, z)) or floodFill.is_air(x, y + 1, z):
						if floodFill.is_air(x, y + 1, z):
							y -=1
						if not(floodFill.is_air(x, y + 2, z)):
							y += 1
			worldmodif.setBlock(x, y, z, "minecraft:grass_path")
			x += ORIENTATION[facingenfant][0]
			z += ORIENTATION[facingenfant][1]
			start = [x, z]



			#house parent
			facingparent = settlementData["structures"][index2]["prebuildingInfo"]["entry"]["facing"]
			#print(facingparent)
			entry2 = []
			entry2.append(floodFill.listHouse[index2][0])
			entry2.append(floodFill.listHouse[index2][1]-1)
			entry2.append(floodFill.listHouse[index2][2])
			x = entry2[0] + ORIENTATION[facingparent][0]
			y = entry2[1]
			z = entry2[2] + ORIENTATION[facingparent][1]
			while not(floodFill.is_air(x, y+2, z)) or floodFill.is_air(x, y+1, z):
						if floodFill.is_air(x, y+1, z):
							y -=1
						if not(floodFill.is_air(x, y+2, z)):
							y += 1
						#print("stuck1")
			worldmodif.setBlock(x, y, z, "minecraft:grass_path")
			x += ORIENTATION[facingparent][0]
			z += ORIENTATION[facingparent][1]
			while not(floodFill.is_air(x, y+2, z)) or floodFill.is_air(x, y+1, z):
						if floodFill.is_air(x, y+1, z):
							y -=1
						if not(floodFill.is_air(x, y+2, z)):
							y += 1
						#print("stuck2")
			worldmodif.setBlock(x, y, z, "minecraft:grass_path")
			x += ORIENTATION[facingparent][0]
			z += ORIENTATION[facingparent][1]
			while not(floodFill.is_air(x, y+2, z)) or floodFill.is_air(x, y+1, z):
						if floodFill.is_air(x, y+1, z):
							y -=1
						if not(floodFill.is_air(x, y+2, z)):
							y += 1
						#print("stuck3")
			worldmodif.setBlock(x, y, z, "minecraft:grass_path")
			x += ORIENTATION[facingparent][0]
			z += ORIENTATION[facingparent][1]
			goal = [x, z]



			#generating the path among 2 houses
			try:
				path = Astar(start, goal, squarelist,floodFill)
				print("Astar done : ", path)
				temp = 1
				z0 = entry1[1]
				zgoal = entry2[1]
				print("start is :", start)
				print("end is : ", goal)
				print("house1 is : ", squarelist[index])
				print("house2 is : ", squarelist[index2])
				for block in path:
					z = z0
					material = 'minecraft:grass_path'
					while not(floodFill.is_air(block[0], z+1, block[1])) or floodFill.is_air(block[0], z, block[1]):
						if floodFill.is_air(block[0], z, block[1]):
							z -=1
						if not(floodFill.is_air(block[0], z+1, block[1])):
							z += 1
					while iu.getBlock(block[0], z, block[1]) == 'minecraft:water':
						z = z + 1
						material = "minecraft:"+materials["woodType"]+"_planks"

					while iu.getBlock(block[0], z, block[1]) == 'minecraft:lava':
						z = z + 1
						material = "minecraft:nether_bricks"
					#here, we need to check if there is a tree above the path, and if yes, we want to remove it
					#if 
					worldmodif.setBlock(block[0],z, block[1],"minecraft:air")
					worldmodif.setBlock(block[0],z + 1, block[1],"minecraft:air")
					worldmodif.setBlock(block[0],z - 1, block[1], material)
					z0 = z
				z0 = entry1[1]
				for block in path:
					#print(block)
					z = z0
					while not(floodFill.is_air(block[0], z+1, block[1])) or floodFill.is_air(block[0], z, block[1]):
						if floodFill.is_air(block[0], z, block[1]):
							z -=1
						if not(floodFill.is_air(block[0], z+1, block[1])):
							z += 1
					if temp%12 == 0 and (temp )<(len(path)-3):
						if not([block[0]-1, block[1]] in path):
							worldmodif.setBlock(block[0]-1, z-1, block[1], 'minecraft:cobblestone')
							worldmodif.setBlock(block[0]-1, z, block[1], 'minecraft:cobblestone_wall')
							worldmodif.setBlock(block[0]-1, z+1, block[1], 'minecraft:redstone_lamp[lit=true]')
						elif not([block[0], block[1] - 1] in path):
							worldmodif.setBlock(block[0], z-1, block[1] - 1, 'minecraft:cobblestone')
							worldmodif.setBlock(block[0], z, block[1] - 1, 'minecraft:cobblestone_wall')
							worldmodif.setBlock(block[0], z+1, block[1] - 1, 'minecraft:redstone_lamp[lit=true]')
						elif not([block[0] + 1, block[1]] in path):
							worldmodif.setBlock(block[0] + 1, z-1, block[1], 'minecraft:cobblestone')
							worldmodif.setBlock(block[0] + 1, z, block[1], 'minecraft:cobblestone_wall')
							worldmodif.setBlock(block[0] + 1, z+1, block[1], 'minecraft:redstone_lamp[lit=true]')
						elif not([block[0], block[1] + 1] in path):
							worldmodif.setBlock(block[0], z-1, block[1] + 1, 'minecraft:cobblestone')
							worldmodif.setBlock(block[0], z, block[1] + 1, 'minecraft:cobblestone_wall')
							worldmodif.setBlock(block[0], z+1, block[1] + 1, 'minecraft:redstone_lamp[lit=true]')
						
					temp += 1
					z0 = z
					
			except ValueError:
				print("ValueError, path can't be implemented there")
				continue

