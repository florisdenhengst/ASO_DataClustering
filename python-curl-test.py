import pycurl
import StringIO
import re
import os.path

# Open ratings file
inputfile = open(os.path.abspath('hotelratings.txt'), 'r')
inputtext = inputfile.read()

# Use '/' as delimiter
delinput = re.split('/', inputtext)

# Keep a list of known hotels
hotellist = []

# Keep a list of review counts
reviewcount = []

# Each review consists of 6 items.
# Only items 2 (hotel name) and 3 (review) are relevant.

j = 1
print len(delinput)
for i in range(1, len(delinput)):

    if i%5 == 1: # = hotel name
        print "Processing review " + str(j) + " of " + str(len(delinput)/5)

        if delinput[i] in hotellist:
            hotelID = hotellist.index(delinput[i])
            reviewcount[hotelID] += 1
            print "Hotel was al bekend op index " + str(hotelID)

        else:
            hotellist.append(delinput[i])
            hotelID = len(hotellist) - 1
            reviewcount.append(1) # Index corresponds with hotellist index, first review (= 1) 
            print "Hotel toegevoegd op index " + str(hotelID)

    if i%5 == 2: # = review
        buf = StringIO.StringIO()

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

        f = open((os.path.dirname(os.path.abspath("python-curl-test.py")) + '/KAF/review-' + str(hotelID) + '-' + str(reviewcount[hotelID]) + ".xml"), 'w')
        f.write(buf.getvalue())
        f.close()
        j += 1

print "Hotels in hotel list:"
k = 0
for hotel in hotellist:
    print str(k) + ": " + hotel + ", " + str(reviewcount[k]) + " review(s)"
    k += 1

os.remove(path)
