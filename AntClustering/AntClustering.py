import math
import random
import time
from Tkinter import *

datasetSize = 1200		# Determine later
dropThreshold = 0.5		# Determine later
pickupThreshold = 0.5	# Determine later

pickupConst = 1
dropConst = 1
alpha = 1

bLoop = False
bAllAnts = True
speed = 0.03

# Classes
class Ant:
	def __init__(self, x, y):
		self.x = x
		self.y = y
		self.load = None

class DataItem:
	def __init__(self, x, y):
		self.x = x
		self.y = y

# Chance an ant picks up the item on its position: ( Kp / ( Kp + F(i) )^2
def pickupChance(ant):
	math.pow((pickupConst / (pickupConst + localSimilarity(ant))), 2)
	return
	
# Chance an ant drops an item on its current position:
#	if F(i) < Kd	2F(i)
#	else				1
def dropChance(ant):
	locSim = localSimilarity(ant)
	if locSim < dropConst:
		return 2 * locSim
	return 1

# Calculate local similarity
def localSimilarity(ant):
	locality = 1 / math.pow(localDist * 2, 2)
	locSim = 0;
	for cono in antColony:
		if inLocalArea(ant, cono):
			locSim += (1 - similarity(ant, cono) / alpha)
	
	result = locality * locSim;
	return max(result, 0)

# Determine if one ant is in local area of the other
def inLocalArea(ant1, ant2):
	if abs(ant1.x - ant2.x) <= localDist and abs(ant1.y - ant2.y) <= localDist:
		return True 
	return False

# Distance between to items
def similarity(i, j):
	# TODO, depends on data
	return

# Creates ants and places them randomly on grid
def createAnts(nrOfAnts):
	for i in range(1, nrOfAnts):
		antColony.append(Ant(random.randint(0, gridUpperXBound), random.randint(0, gridUpperYBound)))
	return

def loadDataItems():
	# TODO, depends on data
	return

def itemOnLocation(ant):
	for item in dataItems:
		if item.x == ant.x and item.y == ant.y:
			return True
	return False

def iterateAnt(ant):
	if ant.load is not None:
		if dropChance(ant) > dropThreshold:
			dropItem(ant)
	elif itemOnLocation(ant):
		if pickupChance(ant) > pickupThreshold:
			pickupItem(ant)
	
	# Move ant in random direction
	moveAnt(ant)
	return

def moveAnt(ant):
	chance = random.random()
	if chance > 0.75:
		ant.x += 1
	elif chance > 0.5:
		ant.x -= 1
	elif chance > 0.25:
		ant.y += 1
	else:
		ant.y -= 1
	if ant.x > gridUpperXBound:
		ant.x = 0
	if ant.x < gridLowerXBound:
		ant.x = gridUpperXBound
	if ant.y > gridUpperYBound:
		ant.y = 0
	if ant.y < gridLowerYBound:
		ant.y = gridUpperYBound
	return

def drawAnts():
	canvas.delete("all")
	for ant in antColony:
		canvas.create_oval(ant.x-3, ant.y-3, ant.x+3, ant.y+3, fill="#805555")
	canvas.update()
	return

def setSpeed():
	global speed
	global tSpeed
	if speed == 0.0001:
		speed = 0.03
	elif speed == 0.03:
		speed = 0.1
	elif speed == 0.1:
		speed = 1
	else:
		speed = 0.0001
	tSpeed.set("Speed: "+str(1/speed))
	return
	
def setPause():
	global bLoop
	global tPlay
	if bLoop == True:
		bLoop = False
		tPlay.set("Play")
	else:
		bLoop = True
		tPlay.set("Pause")
	return
	
def setAllAnts():
	global bAllAnts
	global tAll
	if bAllAnts == True:
		bAllAnts = False
		tAll.set("Update one ant")
	else:
		bAllAnts = True
		tAll.set("Update all ants")
	return

# Create 2D grid which has a surface of 10N: 10 * sqrt(N) by 10 * sqrt(N)
gridLowerXBound = 0
gridLowerYBound = 0
gridUpperXBound = int(10 * math.sqrt(datasetSize))
gridUpperYBound = int(10 * math.sqrt(datasetSize))

# Define local area size
localDist = 5			#Determine later

#Create N/10 number of ants and place randomly in grid
antColony = []
createAnts(datasetSize/10)

# Load data and place data items randomly in the grid
dataItems = []
loadDataItems()

# Draw main canvas
root = Tk()
root.geometry(str(gridUpperXBound)+"x"+str(gridUpperYBound)+"+100+100")
canvas = Canvas(root, bg='#40DE58')
canvas.pack(expand=YES, fill=BOTH)

# Draw buttons
bSpeed = Button(root, text="Speed", command=setSpeed)
bSpeed.pack(side=LEFT)
tSpeed = StringVar()
tSpeed.set("Speed: "+str(1/speed))
lSpeed = Label(root, textvariable=tSpeed)
lSpeed.pack(side=LEFT)
tPlay = StringVar()
tPlay.set("Play")
bStop = Button(root, textvariable=tPlay, command=setPause)
bStop.pack()
tAll = StringVar()
tAll.set("Update all ants")
bAll = Button(root, textvariable=tAll, command=setAllAnts)
bAll.pack()

while 1:
	if bLoop:
		if bAllAnts:
			for ant in antColony:
				iterateAnt(ant)
		else:
			# Select a random ant
			ant = random.choice(antColony)
			iterateAnt(ant)
		
		drawAnts()
		time.sleep(speed)
	else:
		canvas.update()

root.mainloop()

