import math
import random
import time
import urllib2
import os.path
import re
import sys
import time
import datetime
from Tkinter import *
from xml.dom.minidom import parseString

nHotels = 469			# Later nog effe een en dezelfde var van maken
datasetSize = nHotels		# 1200 earlier
dropThreshold = 0.01		# Determine later
pickupThreshold = 0.5		# Determine later

bCooling = False
modCooling = 10000
rateCooling = 0.98

allSubjects = ["room", "sleeping_comfort", "staff", "facilities", "restaurant", "value_for_money", "swimming_pool", "location", "bathroom", "parking", "noise", "cleanliness", "breakfast", "internet"]

pickupConst = 1
dropConst = 1
alpha = 1

bLoop = False
bAllAnts = True
bAntsVisible = True
speed = 0.1
modSpeed = 1
generation = 0

# Classes
class Ant:
	def __init__(self, x, y, load = None):
		self.x = x
		self.y = y
		self.load = load

class DataItem:
	def __init__(self, x, y, hotel, data = []):
		self.x = x
		self.y = y
		self.hotel = hotel
		self.data = data
		
class Subject(object):
    def __init__(self, sub=None, polarity=None, counter=1): # counter = aantal opinions over dat subject
		self.sub = sub
		self.polarity = polarity
		self.counter = counter

# Chance an ant picks up the item on its position: ( Kp / ( Kp + F(i) )^2
def pickupChance(ant):
	return math.pow((pickupConst / (pickupConst + localSimilarity(ant))), 2)
	
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
	if ant.load is not None:
	    dataItemAnt = ant.load
	else:
	    dataItemAnt = itemOnLocation(ant)
	
	locality = 1 / math.pow(localDist * 2, 2)
	locSim = 0;
	for dataItem in dataItems:
		if inLocalArea(ant, dataItem):
			locSim += (1 - similarity(dataItemAnt, dataItem) / alpha)
	
	result = locality * locSim;
	return max(result, 0)

# Determine if one ant is in local area of the other
def inLocalArea(ant, dataItem):
	if abs(ant.x - dataItem.x) <= localDist and abs(ant.y - dataItem.y) <= localDist:
		return True 
	return False

# Distance between two items
def similarity(dataItem1, dataItem2):
	diff = 0
	for iItem in dataItem1.data:
	    for jItem in dataItem2.data:
		if iItem.sub == jItem.sub:
		    diff += math.pow(float(iItem.polarity) - float(jItem.polarity), 2)
	diff = math.sqrt(diff)
	return diff

# Creates ants and places them randomly on grid
def createAnts(nrOfAnts):
	for i in range(1, nrOfAnts):
		antColony.append(Ant(random.randint(0, gridUpperXBound), random.randint(0, gridUpperYBound)))
	return

def itemOnLocation(ant):
	for item in dataItems:
		if item.x == ant.x and item.y == ant.y:
			return item
	return False

def itemOnCoord(xCoord, yCoord):
    for item in dataItems:
	if item.x == xCoord and item.y == yCoord:
	    return True
    return False

def iterateAnt(ant):
	if ant.load is not None:
		d = dropChance(ant)
		if d > dropThreshold:
			dropItem(ant)
	else:
		item = itemOnLocation(ant)
		if item is not False and pickupChance(ant) > pickupThreshold:
			pickupItem(ant, item)
	
	# Move ant in random direction
	moveAnt(ant)
	return
	
def dropItem(ant):
	ant.load.x = ant.x
	ant.load.y = ant.y
	ant.load = None
	return
	
def pickupItem(ant, item):
	ant.load = item
	return

def moveAnt(ant):
    chance = random.random()
    if chance > 0.75:
        dummyX = min(ant.x + 1, gridUpperXBound)
	dummyY = ant.y
    elif chance > 0.5:
        dummyX = max(ant.x - 1, gridLowerXBound)
	dummyY = ant.y
    elif chance > 0.25:
        dummyY = min(ant.y + 1, gridUpperYBound)
	dummyX = ant.x
    else:
        dummyY = max(ant.y - 1, gridLowerYBound)
	dummyX = ant.x
    
    if ant.load is None:
	ant.x = dummyX
	ant.y = dummyY
    elif not itemOnCoord(dummyX, dummyY):
	ant.x = dummyX
	ant.y = dummyY
	ant.load.x = dummyX
        ant.load.y = dummyY
    return

def setAntVisibility():
	global bAntsVisible
	global sAntsVisible

	if bAntsVisible == True:
		bAntsVisible = False
		sAntsVisible.set(value="Toggle visible ants")
	else:
		bAntsVisible = True
		sAntsVisible.set(value="Toggle invisible ants")
	return

def exportResult():
    tijd = datetime.datetime.now()
    f = open(os.path.dirname(os.path.abspath("AntClustering.py")) + "/results/" + tijd.strftime("%Y-%m-%d--%Hu%M") + ".txt", 'w')
    f.write("Result export, created at " + tijd.strftime("%Y-%m-%d %H:%M:%S") + "\n")
    f.write("Dataset size: " + str(datasetSize) + "\n")
    f.write("Alpha: " + str(alpha) + "\n")
    f.write("dropThreshold: " + str(dropThreshold) + "\n")
    f.write("pickupThreshold: " + str(pickupThreshold) + "\n")
    f.write("dropConst: " + str(dropConst) + "\n")
    f.write("pickupConst: " + str(pickupConst) + "\n")
    f.write("All ants updated at the same time: " + str(bAllAnts) + "\n")
    f.write("Generations used: " + str(generation) + "\n")
    f.write("---------------------------------------\n")
    f.write("Syntax: HotelID / X / Y\n\n")
    
    for dataItem in dataItems:
	f.write(str(dataItem.hotel) + "/" + str(dataItem.x) + "/" + str(dataItem.y) + "\n")

    return


def drawAnts():
	sCooling.set(value=str(bCooling)+", value: "+str(pickupThreshold))
	canvas.delete("all")
	
	if bAntsVisible:
		for ant in antColony:
			canvas.create_oval(ant.x-1, ant.y-1, ant.x+1, ant.y+1, fill="#805555")
			#canvas.create_line(ant.x, ant.y, ant.x+1, ant.y+1, fill="#805555")
	
	for dataItem in dataItems:
		canvas.create_oval(dataItem.x-1, dataItem.y-1, dataItem.x+1, dataItem.y+1, fill="#fff")
		#canvas.create_line(dataItem.x, dataItem.y, dataItem.x+1, dataItem.y+1, fill="#000")
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
		sAll.set("Toggle simultaneous ant updates")
	else:
		bAllAnts = True
		sAll.set("Toggle single ant updates")
	return
	
def setCoolingDown():
	global bCooling
	if bCooling:
		bCooling = False
		sCooling.set("False, value: "+str(pickupThreshold))
	else:
		bCooling = True
		sCooling.set("True, value: "+str(pickupThreshold))
	return

# Create 2D grid which has a surface of 10N: 10 * sqrt(N) by 10 * sqrt(N)
gridLowerXBound = 0
gridLowerYBound = 0
gridUpperXBound = int(10 * math.sqrt(datasetSize))
gridUpperYBound = int(10 * math.sqrt(datasetSize))

# Define local area size
localDist = 20			#Determine later

#Create N/10 number of ants and place randomly in grid
antColony = []
createAnts(datasetSize/10)

# Load data and place data items randomly in the grid
dataItems = []

# Draw main canvas
root = Tk()
root.title("Incredibly realistic ant colony")
root.geometry(str(gridUpperXBound+150)+"x"+str(gridUpperYBound+250)+"+100+100")
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

sAll = StringVar(value="Toggle single ant updates")
butAll = Button(root, textvariable=sAll, command=setAllAnts)
butAll.grid(row=4, column=0, columnspan=2)

sAntsVisible = StringVar(value="Toggle invisible ants")
butAntsVisible = Button(root, textvariable=sAntsVisible, command=setAntVisibility)
butAntsVisible.grid(row=5, column=0, columnspan=2)

sCoolingDown = StringVar(value="Cooling down")
butCoolingDown = Button(root, textvariable=sCoolingDown, command=setCoolingDown)
butCoolingDown.grid(row=6, column=0, sticky=E)
sCooling = StringVar(value="True, value: "+str(pickupThreshold))
lCoolingDown = Label(root, textvariable=sCooling)
lCoolingDown.grid(row=6, column=1, sticky=W)

sExportResult = StringVar(value="Export results to file")
butExportResult = Button(root, textvariable=sExportResult, command=exportResult)
butExportResult.grid(row=7, column=0, columnspan=2)


### Process data ###
hotel = 1
review = 1
subjects = []

print "Loading data..."
 
while hotel < nHotels:
	filename = 'KAF/review-'+str(hotel)+"-"+str(review)+'.xml'
	if os.path.exists(filename):
		
		file = open(os.path.abspath('KAF/review-'+str(hotel)+"-"+str(review)+'.xml'), 'r')
		data = file.read()
		file.close()
		
		dom = parseString(data)
		properties = dom.getElementsByTagName('property')
		opinions = dom.getElementsByTagName('opinion')
		
		for opinion in opinions:
			oTargetTag = opinion.getElementsByTagName('target')[0]
			oTarget = oTargetTag.attributes['id'].value
			oExpressionTag = opinion.getElementsByTagName('opinion_expression')[0]
			polarity = oExpressionTag.attributes['strength'].value
			
			for prop in properties:
				pTargetTags = prop.getElementsByTagName('target')
				for pTargetTag in pTargetTags:
					if pTargetTag.attributes['id'].value == oTarget:
						pSubject = prop.attributes['type'].value
						unique = True
						for subject in subjects:
							if subject.sub == pSubject:
								unique = False
								subjectIndex = subjects.index(subject)
						if unique == True:
							subjects.append(Subject(pSubject, polarity))
						else:
							oldSum = float(subjects[subjectIndex].polarity) * subjects[subjectIndex].counter
							subjects[subjectIndex].counter += 1
							newSum = oldSum + float(polarity)
							subjects[subjectIndex].polarity = str(round(newSum / subjects[subjectIndex].counter, 2))
		
		review += 1
	else:
		# Add zero values for all other subjects
		for otherSubject in allSubjects:
			found = False
			for foundsubject in subjects:
				    if otherSubject == foundsubject.sub:
					    found = True
			if not found:
				subjects.append(Subject(otherSubject, 0))
		
		dataItems.append(DataItem(random.randint(0, gridUpperXBound), random.randint(0, gridUpperYBound), hotel, subjects))
		subjects = []
		hotel += 1
		review = 1

### Ant clustering ###
while 1:
	# Do one generation if not paused
	if bLoop:
		generation += 1
		if bCooling and generation%modCooling == 0:
			pickupThreshold *= rateCooling
				
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
