import pygame
import random
import cmath

from Vector import *
from GridNode import *
from GridEdge import *
from Graph import *
from Agent import *
from Coin import *
import os, sys

# Functions
def Distance(n1, n2):
	return (n1.position - n2.position).length()

# Draw the graph by rendering the nodes and edges
def DrawGraph(screen, nodes):
	for nodeRow in nodes:
		for node in nodeRow:
			node.draw(screen)
			for edge in node.neighborEdges:
				edge.draw(screen)
	return

# Constants
screenWidth = 800
screenHeight = 600
gridCellSize = 25
numberRows = int(screenWidth / gridCellSize)
numberCols = int(screenHeight / gridCellSize)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
CORNFLOWER_BLUE = (100, 149, 237)
CYAN = (0, 255, 255)
coinTimer = 60
coinTimerReset = 60
#define intial search type 
searchType = 0
isSearching = False
#initialize a path
path = []
wallPercent = 30

# Init the game
pygame.init()
screen = pygame.display.set_mode((screenWidth, screenHeight))
done = False
angle = 1
clock = pygame.time.Clock()
coinTimer = 50

#create list of coins
coins = []

# Create the list of gridCells (nodes)
nodes = []
breadthGraph = Graph()
for i in range(0, numberRows):
	nodeRow = []
	for j in range(0, numberCols):
		node = GridNode(CYAN, BLACK, Vector(i * gridCellSize,j * gridCellSize), gridCellSize, i, j)
		nodeRow.append(node)
		breadthGraph.addNode(node)
	nodes.append(nodeRow)

# Create the edges between neighbors
for i in range(0, numberRows):
	for j in range(0, numberCols):
		for m in range(i - 1, i + 2):
			for n in range(j - 1, j + 2):
				if m >= 0 and n >= 0 and m < numberRows and n < numberCols \
					and (i != m or j != n):
					edge = GridEdge(nodes[i][j], nodes[m][n], 
								    Distance(nodes[i][j], nodes[m][n]), RED, WHITE)
					nodes[i][j].addNeighborEdge(edge)

#spawn coin and add to list
def spawnCoin():
	#coin object
	coinSpawnNode = nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]
	while coinSpawnNode.isOccupied == True:
		coinSpawnNode = nodes[random.randint(0, numberRows - 1)][random.randint(0, numberCols - 1)]
	coin = Coin(coinSpawnNode)
	coins.append(coin)
	return 

#spawn initial coin 
spawnCoin()

#create agent 
truckImage = pygame.image.load(os.path.join("sprites", "truck.png"))
agent = Agent(Vector(0, 0), Vector(0, 0), truckImage, clock, nodes, numberRows, numberCols, breadthGraph, coins, screen)
# Assume the system starts in non-searching mode
isSearching = False

# tell if a position is in a node 
def isPosInNode(node, x, y):
	if x <= node.position.x + node.size  and x > node.position.x and y <= node.position.y + node.size and y > node.position.y:
		return True 
	else: 
		return False

# Game loop
while not done:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			done = True
			
		# user input 
		if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # spawn wall 
			mouseX, mouseY = pygame.mouse.get_pos()
			for x in nodes:
				for n in x:
					if isPosInNode(n, mouseX, mouseY) == True:
						if n.isOccupied == False:
							n.isOccupied = True
							n.isWall = True
						elif n.isWall == True:							# despawn wall
							n.isOccupied = False
							n.isWall = False				
		elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: #spawn coin 
			mouseX, mouseY = pygame.mouse.get_pos()
			for x in nodes:
				for node in x:
					if isPosInNode(node, mouseX, mouseY) == True:
						if node.isOccupied == False:
							node.isOccupied = True
							coins.append(Coin(node))

	# Clear the background
	screen.fill(CORNFLOWER_BLUE)


	#set search type based on user input 
	if pygame.key.get_pressed()[pygame.K_b] != 0: # Breadth
		searchType = 0
	elif pygame.key.get_pressed()[pygame.K_d] != 0: # Djikstra
		searchType = 1
	elif pygame.key.get_pressed()[pygame.K_s] != 0: # Best
		searchType = 2
	elif pygame.key.get_pressed()[pygame.K_a] != 0: # A* 
		searchType = 3

	# Runs breadth first search
	if len(path) == 0 and isSearching == False and searchType == 0: # BREADTH
		breadthGraph.setupSearch(agent.start, agent.end, SearchType.BREADTH)
		isSearching = True
		path = breadthGraph.RunBreadthFirstStep()
	elif len(path) == 0 and isSearching == False and searchType == 1: # Djikstra
		breadthGraph.setupSearch(agent.start, agent.end, SearchType.DJIKSTRA)
		path = breadthGraph.RunDjikstraStep()
		isSearching = True
	elif len(path) == 0 and isSearching == False and searchType == 2: # Best
		breadthGraph.setupSearch(agent.start, agent.end, SearchType.BEST)
		path = breadthGraph.RunBestFirstStep()
		isSearching = True
	elif len(path) == 0 and isSearching == False and searchType == 3: # A*
		breadthGraph.setupSearch(agent.start, agent.end, SearchType.A_STAR)
		path = breadthGraph.RunA_StarStep()
		isSearching = True
	else:
		isSearching = False

	#spawn coins 
	#create a new coin every second 
	if coinTimer > 0:
		coinTimer -= 1
	else:
		spawnCoin()
		coinTimer = coinTimerReset

	DrawGraph(screen, nodes)

	#update and draw agent
	agent.draw(screen)
	coins = agent.update(coins, path)

	#draw coins
	for coin in coins:
		coin.draw(screen)

	pygame.display.flip()
	clock.tick(60)

