#coding:utf8

import os
import json
import sys
import ConfigParser
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import traceback
import urllib2
import pdb

import time


if __name__ == '__main__':

    cf = ConfigParser.ConfigParser()

    cf.read('insert_company.ini')

    secs = cf.sections()
    print 'setction:', secs
    sec = secs[0]

    path = cf.get(sec, 'path')
    requrl = cf.get(sec, 'requrl')

    # path = 'd:/naren/new-data/positions/'
    # company_lst = []
    # requrl = 'http://localhost:8000/position'
    # requrl = 'http://121.40.183.7:9801/position'

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
