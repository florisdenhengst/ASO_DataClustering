import urllib2
import os.path
import re
 
from xml.dom.minidom import parseString

class Subject(object):
    def __init__(self, sub=None, quantity=None):
        self.sub = sub
        self.quantity = quantity

hotel = 1
review = 1
review_count = 0
subjects = []
subject_count = 0

path, dirs, files = os.walk("KAF").next()
file_count = len(files)
print file_count
 
while hotel < 500:
	filename = 'KAF/review-'+str(hotel)+"-"+str(review)+'.xml'
	if os.path.exists(filename):
		os.system( [ 'clear', 'cls' ][ os.name == 'nt' ] )
		print "Processed: "+str(review_count)+" of "+str(file_count)+" reviews."
		print ""
		print "Total number  of subjects: "+str(subject_count)
		print ""
		print "Processing hotel: "+str(hotel)+", review: "+str(review)
		for subject in subjects:
			print(subject.sub+": "+str(subject.quantity))
		file = open(os.path.abspath('KAF/review-'+str(hotel)+"-"+str(review)+'.xml'), 'r')
		data = file.read()
		file.close()
		
		dom = parseString(data)
		properties = dom.getElementsByTagName('property')
		opinions = dom.getElementsByTagName('opinion')
		
		for opinion in opinions:
			oTargetTag = opinion.getElementsByTagName('target')[0]
			oTarget = oTargetTag.attributes['id'].value
			
			for prop in properties:
				pTargetTags = prop.getElementsByTagName('target')
				for pTargetTag in pTargetTags:
					if pTargetTag.attributes['id'].value == oTarget:
						pSubject = prop.attributes['type'].value
						unique = True
						for subject in subjects:
							if subject.sub == pSubject:
								unique = False
								subject.quantity += 1
						
						if unique == True:
							subjects.append(Subject(pSubject, 1))
						subject_count += 1
		
		review += 1
		review_count += 1
	else:
		hotel += 1
		review = 1