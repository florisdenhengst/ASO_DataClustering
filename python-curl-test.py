import pycurl
import StringIO
import re
import os.path

inputfile = open(os.path.abspath('test.txt'), 'r')
inputtext = inputfile.read()
delinput = re.split('/', inputtext)

j = 1
print len(delinput)
for i in range(1, len(delinput)):
	if i%4 == 0:
		buf = StringIO.StringIO()
		
		print "Processing review " + str(j) + " of " + str(len(delinput)/4)

		c = pycurl.Curl()
		c.setopt(c.URL, 'http://ic.vupr.nl:9081/ner-prop-opin')
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.setopt(c.POST, 1)
		
		path = os.path.dirname(os.path.abspath("python-curl-test.py")) + "/KAF/dummy.txt"
				
		d = open(path, 'w')
		d.write(delinput[i])

		c.setopt(c.HTTPPOST, [("stdin", (c.FORM_FILE, path))])
		c.perform()
		c.close()

		f = open((os.path.dirname(os.path.abspath("python-curl-test.py")) + '/KAF/review-' + str(j) + ".xml"), 'w')
		f.write(buf.getvalue())
		f.close()
		j += 1

os.remove(path)