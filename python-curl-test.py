import pycurl
import StringIO
import re
import os.path

inputfile = open(os.path.abspath('test.txt'), 'r')
inputtext = inputfile.read()
delinput = re.split('/', inputtext)

for i in range(1, 10):
	if i%4 == 0:
		buf = StringIO.StringIO()
		
		print delinput[i]

		c = pycurl.Curl()
		c.setopt(c.URL, 'http://ic.vupr.nl:9081/ner-prop-opin')
		c.setopt(c.WRITEFUNCTION, buf.write)
		c.setopt(c.POST, 1)
		
		path = os.path.dirname(os.path.abspath("text.txt")) + "/KAF/dummy.txt"
		print path
		
		d = open(path, 'w')
		d.write(delinput[i])

		c.setopt(c.HTTPPOST, [("stdin", (c.FORM_FILE, path))])
		c.perform()
		c.close()

		f = open((os.path.dirname(os.path.abspath("text.txt")) + '/KAF/' + str(i) + ".xml"), 'w')
		f.write(buf.getvalue())
		f.close()

os.remove(path)