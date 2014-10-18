import urllib
import time

API_KEY = 'API_KEY'

url = 'http://api.rottentomatoes.com/api/public/v1.0/movies/%s.json?apikey=%s' % API_KEY
data_path = 'data/%s.json'
starting_id = 770672122


for i in xrange(9800):
    new_id = starting_id + i
    try:
        urllib.urlretrieve(url % new_id, data_path % new_id)
        print "Retrieved Movie %s" % new_id
    except:
        print "Exception on %s" % new_id
    time.sleep(0.2)