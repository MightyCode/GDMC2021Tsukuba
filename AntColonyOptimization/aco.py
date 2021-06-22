import threading
import time
import numpy as np
import lib.interfaceUtils as iu

class AntColonyOptimizer:
	def __init__(self, xmatrix, zmatrix, startingmatrix, startnode, endnode):
		self.map_matrix = np.zeros((xmatrix,zmatrix))
		self.lenx = xmatrix
		self.lenz = zmatrix
		self.startmatrix = startingmatrix
		self.pheromone_matrix = np.zeros((xmatrix, zmatrix))
		self.probability_matrix = np.ones((xmatrix, zmatrix),dtype=int)
		self.available_nodes = np.zeros((xmatrix, zmatrix))
		self.start = startnode
		self.end = endnode
		self.score = None
		self.pheromone_value = 60
		self.pheromone_decrease = 0.8
		self.path_matrix_for_pheromone = np.zeros((xmatrix,zmatrix))
		self.numberofant = 20
		self.numberofiteration = 20

	def print_matrix(matrix):
		print(matrix[0])
		print(matrix[1])
		print(matrix[2])
		print(matrix[3])
		print(matrix[4])
		print(matrix[5])
		print(matrix[6])
		print(matrix[7])
		print(matrix[8])
		print(matrix[9])

	def reinstate(self):
		self.available_nodes = np.zeros((self.lenx, self.lenz))

	def updatepheromone(self):
		self.pheromone_matrix = (self.pheromone_decrease * self.pheromone_matrix) + ((self.pheromone_value / self.score[1]) * self.path_matrix_for_pheromone)
		print("pheromone_matrix is :")
		print(self.pheromone_matrix)

	def updateproba(self):
		self.probability_matrix = np.ones((self.lenx, self.lenz)) + np.ones((self.lenx, self.lenz))*self.pheromone_matrix
		print("proba matrix is :")
		print(self.probability_matrix)

	def getscore(self,index):
		distancebetweennode = abs(self.start[0] - self.end[0]) + abs(self.start[1] - self.end[1])
		print(distancebetweennode,"is the disctance between start and end")
		distancebetweenend = abs(index[0] - self.end[0]) + abs(index[1] - self.end[1])
		print(distancebetweenend,"is the distance between the last node and end")
		print(index[2],"and",distancebetweennode)
		return ( index[2] / distancebetweennode )  + distancebetweenend
		

	def launch(self):
		for j in range(self.numberofiteration):
			for i in range(self.numberofant):
				self.ant(self.start)
				self.reinstate()
				print(self.score)
				print("path_matrix_for_pheromone is :")
				print(self.path_matrix_for_pheromone)
			self.updatepheromone()
			self.updateproba()
		print(self.path_matrix_for_pheromone)
		self.finish()


	def choose_next_node(self,index):
		#print(index)
		listchoice = [[0,1],[1,0],[-1,0],[0,-1]]
		indexlistchoice = [0,1,2,3]
		temp = 0
		indexrow = [0,0]
		
		good = False
		notfound = False
		temp = 0
		while good == False and notfound == False:
			p =	self.getprobabilitiesaround(index)
			#print(p)
			nbriteration = 0
			for i in p:
				if i > 0:
					nbriteration += 1
			direction = np.random.choice(indexlistchoice , nbriteration , False,p)
			temp = 0
			#print("direction is: ",direction)
			#print("with length:" ,len(direction))
			while temp < len(direction):
				indexrow[0] = index[0] + listchoice[direction[temp]][0]
				indexrow[1] = index[1] + listchoice[direction[temp]][1]
				if indexrow[0] < self.lenx and indexrow[1] < self.lenz and self.available_nodes[indexrow[0]][indexrow[1]] == 0 and good == False:
					self.available_nodes[indexrow[0]][indexrow[1]] = 1
					#self.printingpath()
					answer = indexrow.copy()
					good = True
				temp += 1
			if good == False:
				notfound = True
		if good:
			return [answer[0], answer[1]]
		else:
			print("no node found")
			return [-1, -1]

	def ant(self, index):
		self.available_nodes[index[0]][index[1]] = 1
		temp = 1
		test = self.choose_next_node(self.start)
		while [test[0],test[1]] != [-1,-1] and [test[0],test[1]] != self.end:
			temp += 1
			test = self.choose_next_node(test)
			if [test[0],test[1]] != [-1, -1]:
				endcase = test
		scoreant = self.getscore([test[0],test[1],temp])
		print(endcase,"is the endase")
		if self.score == None:
			self.score = [scoreant, temp]
			print(self.score,"is the score")
		elif self.score[0] > scoreant:
			self.score = [scoreant, temp]
			print(self.score,"is the score")
			self.path_matrix_for_pheromone = self.available_nodes.copy()

	def finish(self):
		self.map_matrix[self.start[0]][self.start[1]] = 2
		self.map_matrix[self.end[0]][self.end[1]] = 1
		self.map_matrix = self.map_matrix + self.path_matrix_for_pheromone
		print(self.map_matrix)
		self.printinminecraft()

	def getprobabilitiesaround(self,index):
		listchoice = [[0,1],[1,0],[-1,0],[0,-1]]
		temp = 0
		indexlistchoice = [0,1,2,3]
		listproba = [0,0,0,0]
		for i in indexlistchoice:
			try:

				if (index[0] + listchoice[i][0]) >= 0 and (index[0] + listchoice[i][0]) <= (len(self.probability_matrix) - 1) and (index[1] + listchoice[i][1]) >= 0 and (index[1] + listchoice[i][1]) <= (len(self.probability_matrix[0]) -1):
					#print(index[0] + listchoice[i][0],"and ",index[1] + listchoice[i][1])
					listproba[temp] = self.probability_matrix[index[0] + listchoice[i][0]][index[1] + listchoice[i][1]]
					temp += 1
				else:
					temp += 1
			except IndexError:
				temp += 1
				continue
		if sum(listproba) == 0:
			print("the ant is blocked")
		else:
			sumlist = sum(listproba)
			listproba[0] = listproba[0] / sumlist
			listproba[1] = listproba[1] / sumlist
			listproba[2] = listproba[2] / sumlist
			listproba[3] = listproba[3] / sumlist
		return listproba


	def printinminecraft(self):
		tempx = 0
		tempz = 0
		for arrayx in self.map_matrix:
			tempz = 0
			for block in arrayx:
				if block == 1:
					iu.setBlock(tempx + self.startmatrix[0], 4 , tempz + self.startmatrix[1],"minecraft:bricks")
				elif block == 2:
					iu.setBlock(tempx + self.startmatrix[0], 4 , tempz + self.startmatrix[1],"minecraft:cobblestone")
				elif block == 3:
					iu.setBlock(tempx + self.startmatrix[0], 4 , tempz + self.startmatrix[1],"minecraft:nether_bricks")
				tempz += 1
			tempx += 1
			



	def printingpath(self):
		string = "path is"
		string += "\n"+str(self.available_nodes[0])
		string += "\n"+str(self.available_nodes[1])
		string += "\n"+str(self.available_nodes[2])
		string += "\n"+str(self.available_nodes[3])
		string += "\n"+str(self.available_nodes[4])
		string += "\n"+str(self.available_nodes[5])
		string += "\n"+str(self.available_nodes[6])
		string += "\n"+str(self.available_nodes[7])
		string += "\n"+str(self.available_nodes[8])
		string += "\n"+str(self.available_nodes[9])
		print(string)


