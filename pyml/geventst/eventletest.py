import eventlet
from eventlet.green import urllib2


urls = [
    "http://www.google.com/intl/en_ALL/images/logo.gif",
    "http://www.baidu.com",
    "http://www.sina.com.cn",
]


def fetch(url):
    print url
    return urllib2.urlopen(url).read()

pool = eventlet.GreenPool()

for body in pool.imap(fetch, urls):
    print("got body", len(body))