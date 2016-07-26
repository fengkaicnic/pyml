#coding:utf8

import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import ConfigParser
import utils
import traceback
import urllib2
import pdb

import time

if __name__ == '__main__':

    cf = ConfigParser.ConfigParser()

    cf.read('insert_profile.ini')

    secs = cf.sections()
    print 'setction:', secs
    sec = secs[0]

    path = cf.get(sec, 'path')
    requrl = cf.get(sec, 'requrl')

    # path = 'd:/naren/wsgi-server/resumes/read/'
    # path = 'D:/naren/new-data/read/'
    # company_lst = []
    # requrl = 'http://localhost:8000/profile'
    # requrl = 'http://121.40.183.7:9801/profile'

    start = time.time()

    num = 0
    for name in os.listdir(path):
        with open(path + name) as file:
            pos_id = name.split('-')[0]
            resume_id = name.split('-')[1].split('.')[0]
            lines = file.readlines()
            resume_dct = eval(''.join(lines))
            data = {'profile':resume_dct, 'pos_id':pos_id}
            # data = resume_dct
            try:
                req = urllib2.Request(url=requrl, data=str(data))
                res_data = urllib2.urlopen(req)
                #
                # res = res_data.read()
            except:
                traceback.print_exc()
            num += 1

            print num

    end = time.time()

    print (end - start)
