import random
import utils._math as _math


class Node:
	def __init__(self,point):
		self.point = point
		self.parent = None
		self.cost = 0
		self.H = 0
	def move_cost(self,other):
		return 1



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
	for i in closedlist:
		if node.point == i.point:
			return True
	return False

def isInListWithInferiorCost(node, list):
	for i in list:
		if node.point == i.point:
			if i.H <= node.H:
				return True
	return False

def Astar(startcoord,goalcoord,squarehouse1,squarehouse2):
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
			return path[::-1] #to reverse the path
		#for every neighbourg of current node
		for node in children(current):
			#test here if the children is in a house
			if not(_math.isPointInSquare(node.point, squarehouse1) or _math.isPointInSquare(node.point, squarehouse2)):
				if not(isInClosedList(node, closedlist) or isInListWithInferiorCost(node, openlist)):
					node.cost = current.cost + 1
					node.H = node.cost + manhattan(node,goal)
					node.parent = current
					openlist.append(node)
		closedlist.append(current)
	raise ValueError('No Path Found')




def initRoad(floodFill, settlementData, worldmodif,ws):
	ORIENTATION = {"north" : [ 0, -1 ], "south" : [ 0, 1 ], "west" : [ -1, 0 ], "east" : [ 1, 0 ]}
	#to 
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
			worldmodif.setBlock(entry1[0] + ORIENTATION[facingenfant][0], entry1[1], entry1[2] + ORIENTATION[facingenfant][1],"minecraft:grass_path")
			worldmodif.setBlock(entry1[0] + 2 * ORIENTATION[facingenfant][0], entry1[1], entry1[2] + 2 * ORIENTATION[facingenfant][1],"minecraft:grass_path")
			start = [entry1[0] + 3 * ORIENTATION[facingenfant][0], entry1[2] + 3 * ORIENTATION[facingenfant][1]]
			#house parent
			facingparent = settlementData["structures"][index2]["prebuildingInfo"]["entry"]["facing"]
			print(facingparent)
			entry2 = []
			entry2.append(floodFill.listHouse[index2][0])
			entry2.append(floodFill.listHouse[index2][1]-1)
			entry2.append(floodFill.listHouse[index2][2])
			worldmodif.setBlock(entry2[0] + ORIENTATION[facingparent][0], entry2[1], entry2[2] + ORIENTATION[facingparent][1],"minecraft:grass_path")
			worldmodif.setBlock(entry2[0] + 2 * ORIENTATION[facingparent][0], entry2[1], entry2[2] + 2 * ORIENTATION[facingparent][1],"minecraft:grass_path")
			goal = [entry2[0] + 3 * ORIENTATION[facingparent][0], entry2[2] + 3 * ORIENTATION[facingparent][1]]
			
			#to init square of houses
			square1 = [entry1[0] + floodFill.listHouse[index][3][0], entry1[2] + floodFill.listHouse[index][3][1], entry1[0] + floodFill.listHouse[index][3][2], entry1[2] + floodFill.listHouse[index][3][3]]
			square2 = [entry2[0] + floodFill.listHouse[index2][3][0], entry2[2] + floodFill.listHouse[index2][3][1], entry2[0] + floodFill.listHouse[index2][3][2], entry2[2] + floodFill.listHouse[index2][3][3]]
			print("the start is : ",start)
			print("the end is : ",goal)
			print("the house 1 :",square1)
			print("the house 2 :",square2)
			#generating the path among 2 houses
			try:
				path = Astar(start,goal,square1,square2)
				print("Astar done : ",path)
				temp = 0
				z0 = entry1[1]
				for block in path:
					z = z0
					while not(floodFill.is_air(block[0],z+1,block[1],ws)) or floodFill.is_air(block[0],z,block[1],ws):
						if floodFill.is_air(block[0],z,block[1],ws):
							z -=1
						if not(floodFill.is_air(block[0],z+1,block[1],ws)):
							z += 1


					worldmodif.setBlock(block[0],z - 1,block[1],"minecraft:grass_path")
					if temp%6 == 0:
						worldmodif.setBlock(block[0],z,block[1],"minecraft:torch")
					temp += 1

					z0 = z
			except ValueError:
				print("ValueError, path can't be implemented there")
				continue

