import pygame

from Node import *
from Edge import *
from Vector import *
from enum import Enum

# Define the possible search types that are supported by this graph
class SearchType(Enum):
	BREADTH = 1
	DJIKSTRA = 2
	A_STAR = 3
	BEST = 4

class Graph(object):
	"""Generic Graph class that can be used with any type of Nodes and Edges"""

	# Initialize the graph as empty and default search of breadth-first
	def __init__(self):
		self.nodes = []
		self.path = []
		self.toVisit = []
		self.searchType = SearchType.BREADTH
		return

	# Add a node to the graph (neighbors are accessed through the nodes)
	def addNode(self, node):
		self.nodes.append(node)
		return

	# Initialize the search - this resets the graph
	def setupSearch(self, start, end, searchType):
		self.start = start
		self.end = end
		self.searchType = searchType

		# Reset the graph for the search
		# TODO
		#set everynode in the grid to not visited, reset the color, and set traveled to false
		for nodes in self.nodes:
			nodes.reset()
			nodes.backpath = 0
			nodes.isVisited = False
			nodes.traveled = False  

		#clear the path and to visit list for next search
		self.path = []
		self.toVisit.clear()

		# Identify the starting node as visited and add
		# to the toVisit queue
		# TODO
		self.start.isVisited = True
		self.toVisit.append(self.start)
		return

	# Perform a Breadth-first search, one step at a time
	def RunBreadthFirstStep(self):
		print("BREADTH")
		# TODO
		while len(self.toVisit) > 0: 
			currNode = self.toVisit.pop(0)
			currNode.poppedNodeColor()
			for neighbor in currNode.neighborEdges:
				if neighbor.n2.isVisited == False and neighbor.n2.isWall == False:
					neighbor.n2.setVisited(True)
					self.toVisit.append(neighbor.n2)
					neighbor.n2.backpath = currNode
					if neighbor.n2 == self.end: #we found the end node, build and return the path 
						self.path.append(neighbor.n2)
						while currNode.backpath != 0:
							self.path.append(currNode)
							currNode = currNode.backpath
						self.path.reverse()
						return self.path			
		return self.path

	# Perform a Djikstra's search, one step at a time
	def RunDjikstraStep(self):
		print("DJIKSTRA")
		# TODO
		while len(self.toVisit) > 0:
			self.toVisit = sorted(self.toVisit, key=lambda x: x.cost)
			currNode = self.toVisit.pop(0)
			currNode.poppedNodeColor()
			if currNode == self.end: #if start node is the end node
				while currNode.backpath != 0:
					self.path.append(currNode)
					currNode = currNode.backpath
					#path is created from end to start so reverse the order for agents path traversal 					
				self.path.reverse()
				return self.path
			for neighbor in currNode.neighborEdges:
				currDistance = neighbor.weight
				if neighbor.n2.isVisited == False and neighbor.n2.isWall == False:# or neighbor.n2.cost < currNode.cost:
					neighbor.n2.setVisited(True)
					neighbor.n2.actualCost = currDistance + currNode.actualCost
					neighbor.n2.estimatedCost = 0
					neighbor.n2.cost = neighbor.n2.actualCost + neighbor.n2.estimatedCost #change neighbor.weight to currDistance
					neighbor.n2.backpath = currNode
					self.toVisit.append(neighbor.n2)
				elif neighbor.n2.isWall == False: #node has been visited 
					if currDistance + currNode.cost < neighbor.n2.cost:
						neighbor.n2.cost = currDistance + currNode.cost
						neighbor.n2.backpath = currNode
		return self.path

	# Perform a Best-first search, one step at a time
	def RunBestFirstStep(self):
		print("BEST")
		# TODO
		while len(self.toVisit) > 0:
			self.toVisit = sorted(self.toVisit, key=lambda x: x.cost)
			currNode = self.toVisit.pop(0)
			currNode.poppedNodeColor()
			if currNode == self.end: #if start node is the end node
				while currNode.backpath != 0:
					self.path.append(currNode)
					currNode = currNode.backpath
					#path is created from end to start so reverse the order for agents path traversal 					
				self.path.reverse()
				return self.path
			for neighbor in currNode.neighborEdges:
				currDistance = neighbor.weight
				if neighbor.n2.isVisited == False and neighbor.n2.isWall == False:# or neighbor.n2.cost < currNode.cost:
					neighbor.n2.setVisited(True)
					neighbor.n2.actualCost = 0
					neighbor.n2.estimatedCost = (neighbor.n2.position - self.end.position).length()
					neighbor.n2.cost = neighbor.n2.actualCost + neighbor.n2.estimatedCost #change neighbor.weight to currDistance
					neighbor.n2.backpath = currNode
					self.toVisit.append(neighbor.n2)
				elif neighbor.n2.isWall == False: #node has been visited 
					if currDistance + currNode.cost < neighbor.n2.cost:
						neighbor.n2.cost = currDistance + currNode.cost
						neighbor.n2.backpath = currNode
		return self.path

	# Perform an A-star search, one step at a time
	def RunA_StarStep(self):
		print("A*")
		# TODO
		while len(self.toVisit) > 0:
			self.toVisit = sorted(self.toVisit, key=lambda x: x.cost)
			currNode = self.toVisit.pop(0)
			currNode.poppedNodeColor()
			if currNode == self.end: #if start node is the end node
				while currNode.backpath != 0:
					self.path.append(currNode)
					currNode = currNode.backpath
					#path is created from end to start so reverse the order for agents path traversal 					
				self.path.reverse()
				return self.path
			for neighbor in currNode.neighborEdges:
				currDistance = neighbor.weight
				if neighbor.n2.isVisited == False and neighbor.n2.isWall == False:# or neighbor.n2.cost < currNode.cost:
					neighbor.n2.setVisited(True)
					neighbor.n2.actualCost = currDistance + currNode.actualCost
					neighbor.n2.estimatedCost = (neighbor.n2.position - self.end.position).length()
					neighbor.n2.cost = neighbor.n2.actualCost + neighbor.n2.estimatedCost #change neighbor.weight to currDistance
					neighbor.n2.backpath = currNode
					self.toVisit.append(neighbor.n2)
				elif neighbor.n2.isWall == False: #node has been visited 
					if currDistance + currNode.cost < neighbor.n2.cost:
						neighbor.n2.cost = currDistance + currNode.cost
						neighbor.n2.backpath = currNode
		return self.path

	# Call the next step for the current search type
	def update(self):
		return