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
speed = 0.1
modSpeed = 1
generation = 0

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
	global sSpeed
	
	speed = speed/10
	if speed < 0.0001:
		speed = 1.0
	sSpeed.set(str(1/speed)+" ant (colony) updates/s")
	return
	
def setModSpeed():
	global modSpeed
	global sModSpeed
	modSpeed *= 10
	if modSpeed > 1000:
		modSpeed = 1
	sModSpeed.set(value="Canvas updated after "+str(modSpeed)+" generations")
	return
	
def setPause():
	global bLoop
	global sPlay
	if bLoop == True:
		bLoop = False
		sPlay.set("Play")
	else:
		bLoop = True
		sPlay.set("Pause")
	return
	
def setAllAnts():
	global bAllAnts
	global sAll
	if bAllAnts == True:
		bAllAnts = False
		sAll.set("Update one ant")
	else:
		bAllAnts = True
		sAll.set("Update all ants")
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
root.title("Incredibly realistic ant colony")
root.geometry(str(gridUpperXBound)+"x"+str(gridUpperYBound+150)+"+100+100")
canvas = Canvas(root, width=str(gridUpperXBound), height=str(gridUpperYBound), bg='#40DE58')
canvas.grid(row=0, column=0, columnspan=2)

# Draw buttons
sPlay = StringVar(value="Play")
butPlay = Button(root, textvariable=sPlay, command=setPause)
butPlay.grid(row=1, column=0, sticky=E)

sGeneration = StringVar(value="Generation = "+str(generation))
lGeneration = Label(root, textvariable=sGeneration)
lGeneration.grid(row=1, column=1, sticky=W)

butSpeed = Button(root, text="Speed", command=setSpeed)
butSpeed.grid(row=2, column=0, sticky=E)
sSpeed = StringVar(value=str(1/speed)+" ant (colony) updates/s")
lSpeed = Label(root, textvariable=sSpeed)
lSpeed.grid(row=2, column=1, sticky=W)

butModSpeed = Button(root, text="Fast forward", command=setModSpeed)
butModSpeed.grid(row=3, column=0, sticky=E)
sModSpeed = StringVar(value="Canvas updated after "+str(modSpeed)+" generations")
lModSpeed = Label(root, textvariable=sModSpeed)
lModSpeed.grid(row=3, column=1, sticky=W)

sAll = StringVar(value="Update all ants")
butAll = Button(root, textvariable=sAll, command=setAllAnts)
butAll.grid(row=4, column=0, columnspan=2)

while 1:
	# Do one generation if not paused
	if bLoop:
		generation += 1
		sGeneration.set("Generation = "+str(generation))
		if bAllAnts:
			# Iterate all ants
			for ant in antColony:
				iterateAnt(ant)
		else:
			# Select a random ant and iterate
			ant = random.choice(antColony)
			iterateAnt(ant)
		
		# Every modSpeed-steps the canvas is drawn(for FastForwarding)
		if (generation%modSpeed == 0):
			drawAnts()
		# Sleep 'speed'-time units to make the speed variable
		time.sleep(speed)
	
	# Update the canvas each loop to make sure the buttons still work
	canvas.update()

root.mainloop()

