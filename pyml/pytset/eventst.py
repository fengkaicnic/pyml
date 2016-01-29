
import eventlet
from eventlet.green import urllib2
import time
start = time.time()

def fetch(url):
    return urllib2.urlopen(url).read()

urls = [
       "http://www.google.com/intl/en_ALL/images/logo.gif",
       "http://python.org/images/python-logo.gif",
       "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif", 
       ]

pool = eventlet.GreenPool()
for body in pool.imap(fetch, urls):
    print('got body', len(body))

end = time.time()

print (end - start)