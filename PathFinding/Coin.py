import pygame
import random
import cmath

#from Vector import *
from GridNode import *
from GridEdge import *
from Graph import *
from pygame import *

YELLOW = (255, 255, 0)

class Coin(object):
	"""coin for agent to pickup"""

	def __init__(self, node):
		self.node = node
		self.center = node.center
		self.radius = 12
		self.node.isOccupied = True
		self.distance = 0
	

	def draw(self, screen):
		pygame.draw.circle(screen, YELLOW, (int(self.center.x), int(self.center.y)), self.radius, 0)

		return