import urllib2
import os.path
import re
 
from xml.dom.minidom import parseString
 
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
		print "Number of subjects: "+str(len(subjects))
		print "Total number  of subjects: "+str(subject_count)
		print ""
		print "Processing hotel: "+str(hotel)+", review: "+str(review)
		file = open(os.path.abspath('KAF/review-'+str(hotel)+"-"+str(review)+'.xml'), 'r')
		data = file.read()
		file.close()
		
		dom = parseString(data)
		
		opinions = dom.getElementsByTagName('opinion')
		for opinion in opinions:
			oTargetTag = opinion.getElementsByTagName('target')[0]
			oTarget = oTargetTag.attributes['id'].value
			
			terms = dom.getElementsByTagName('term')
			for term in terms:
				tTarget = ''
				if term.attributes['tid'].value == oTarget:
					tTargetTag = term.getElementsByTagName('target')[0]
					tTarget = tTargetTag.attributes['id'].value
		
				words = dom.getElementsByTagName('wf')
				for word in words:
					if word.attributes['wid'].value == tTarget:
						word = re.sub('<.*?>', "", word.toxml())
						if word not in subjects:
							subjects.append(word)
							print "Toegevoegd: "+word
						else:
							print "Dubbel: "+word
						subject_count += 1
		review += 1
		review_count += 1
	else:
		print "Hotel: "+str(hotel)
		hotel += 1
		review = 1