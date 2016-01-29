
import urllib2
import time
start = time.time()

def fetch(url):
    return urllib2.urlopen(url).read()

urls = [
       "http://www.google.com/intl/en_ALL/images/logo.gif",
       "http://python.org/images/python-logo.gif",
       "http://us.i1.yimg.com/us.yimg.com/i/ww/beta/y3.gif", 
       ]


for url in urls:
    print('got body', len(urllib2.urlopen(url).read()))

end = time.time()

print (end - start)