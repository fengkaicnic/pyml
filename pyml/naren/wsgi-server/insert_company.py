#coding:utf8

import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import traceback
import urllib2
import pdb

import time

path = 'd:/naren/new-data/positions/'
company_lst = []
requrl = 'http://localhost:8000/position'

start = time.time()

for name in os.listdir(path):
    with open(path + name) as file:
        lines = file.readlines()
        com_dct = eval(''.join(lines))
        data = {'company':com_dct}
        req = urllib2.Request(url=requrl, data=str(data))

        res_data = urllib2.urlopen(req)

        res = res_data.read()

        print res

end = time.time()

print (end - start)
