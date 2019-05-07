import pygame

from pygame import Rect
from Vector import *
from Node import *

#colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CORNFLOWER_BLUE = (100, 149, 237)
CYAN = (0, 255, 25)
GREY = (105, 105, 105)
MAGENTA = (255, 0, 255)
YELLOW = (255, 255, 0)

class GridNode(Node):
	"""Node in a grid"""

	# Initialize the nodes colors, position, size, and identifiers
	def __init__(self, color, borderColor, position, size, row, col):
		super().__init__()
		self.color = color
		self.originalColor = color
		self.borderColor = borderColor
		self.position = position
		self.size = size
		self.center = Vector(self.position.x + size * 0.5, self.position.y + size * 0.5)
		self.row = row
		self.col = col
		self.wallColor = GREY
		self.wallSpawnPercent = 30

		if random.randint(0, 100) < self.wallSpawnPercent:
			self.isWall = True
			self.isOccupied = True
		else:
			self.isWall = False
		
		return

	# Reset the node colors to their original colors
	def reset(self):
		self.color = self.originalColor
		self.actualCost = 0
		self.estimatedCost = 0
		self.cost = 0
		return

	def poppedNodeColor(self):
		self.color = MAGENTA
		return

	# Set the visited status of the node and change its color
	def setVisited(self, isVisited):
		super().setVisited(isVisited)
		self.color = (0, 0, 255)
		return

	# Get the visited status
	def getVisited(self):
		return super().getVisited()

	# Print the node's data for debugging
	def print(self):
		print("Node: [" + str(self.row) + "][" + str(self.col) + "]")
		super().print()
		return

	# Draw the node and its rectangular boundary
	def draw(self, screen):
		# draw the filled rectangle
		if self.isWall == True:
			pygame.draw.rect(screen, self.wallColor, Rect(self.position.x, self.position.y, 
												  self.size, self.size))
		else:
			pygame.draw.rect(screen, self.color, Rect(self.position.x, self.position.y, 
												  self.size, self.size))

		# draw the boarder for the rectangle
		pygame.draw.rect(screen, self.borderColor, Rect(self.position.x, self.position.y, 
												        self.size, self.size), 1)
		return
