import pygame
import random
import cmath

#from Vector import *
from GridNode import *
from GridEdge import *
from Graph import *
from pygame import *
from Coin import *

#constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CORNFLOWER_BLUE = (100, 149, 237)
CYAN = (0, 255, 255)
SILVER = (192, 192, 192)

class Agent(object):
	"""agent to follow graph path and collect coins"""

	#constructor for agent 
	def __init__(self, pos, vel, image, clock, nodes, numberRows, numberCols, graph, coinList, screen):
		self.vel = vel
		self.searchType = 0 #0 = Breadth 1 = Djikstra 2 = Best 3 = A*
		self.image = image
		self.screen = screen
		self.width, self.height = Surface.get_size(self.image)
		self.clock = clock
		self.nodes = nodes
		self.graph = graph
		#make sure agent does not start on a wall node
		self.start = self.nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]
		if self.start.isWall == True:
				self.start.isWall = False
				self.start.isOccupied = False
		self.end = coinList[0].node
		self.pos = self.start.position
		self.pointRadius = 2 #this may need to be tweeked 
		self.speed = 2
		self.isSearching = False
		self.gotCoin = False
		self.center = self.start.center
		self.closestNode = 0
		self.distToClosest = 1000
		self.closestCoin = coinList[0]
		self.DistClosestCoin = 1000
		coinList[0].distance = (self.center - coinList[0].node.center).length()

	#draw agent at self.pos
	def draw(self, screen):
		screen.blit(self.image, (self.pos.x, self.pos.y))
		return

	def ResetPath(self, path):
		#reset each node in the path
		for node in path:
			node.reset()
			node.isVisited = False
			node.backpath = 0
		return

	#travel along the found path
	def TravelAlongPath(self, path):
		#make all nodes in path black
		for node in path:
			node.color = WHITE

		if len(path) > 0:
			self.vel = (path[0].center - self.center).normalize()
			self.vel = self.vel.scale(self.speed)

			if (path[0].center - self.center).length() <= self.pointRadius:
				# we have reached next node in path, reset the start node
				self.start.reset()
				self.start.isVisited = False
				self.start.backpath = 0
				# make the new start node the node we just reached
				self.start = path.pop(0)
		return

	#sort list of coins by distance to agent
	def sortCoins(self, coinList):
		for coin in coinList:
			distance = (self.center - coin.center).length()
			coin.distance = distance
		return sorted(coinList, key=lambda x: x.distance)

	#finds next coin and resets the path
	def FindNextCoin(self, coinList):

		#sort list of coins based on distance to agent
		coinList = self.sortCoins(coinList)
		
		#find the next closest coin and set it to closestCoin (passed to path finder as end node)
		if len(coinList) > 0:
			self.closestCoin = coinList[0]
			self.end = self.closestCoin.node
		return coinList

	#update agents logic
	def update(self, coinList, path):
		self.center = Vector(self.pos.x + self.width * 0.5, self.pos.y + self.height * 0.5)

		if len(path) > 0:
			self.TravelAlongPath(path)
			self.gotCoin = False
		elif len(coinList) > 0 and self.gotCoin == False:
			#print("POP")
			coinList.pop(0)
			self.gotCoin = True
			self.vel = Vector(0, 0)
			coinList = self.FindNextCoin(coinList)
		else:
			self.vel = Vector(0, 0)

		#set the colors for the start and end node
		self.end.color = RED
		self.start.color = GREEN

		#move the agent
		self.pos += self.vel
		return coinList
