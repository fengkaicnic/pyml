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
import ConfigParser
import pdb

import time

if __name__ == '__main__':
    cf = ConfigParser.ConfigParser()

    cf.read('update_pos_resume.ini')

    secs = cf.sections()
    print 'setction:', secs
    sec = secs[0]

    path = cf.get(sec, 'path')
    requrl = cf.get(sec, 'requrl')
    # confirm = cf.get(sec, 'confirm')

    # path = 'd:/naren/new-data/recommend/'
    # company_lst = []
    # requrl = 'http://localhost:8000/pos_resume'
    # confirm = 'hunter_confirm'

    start = time.time()

    num = 0
    for resume_type in os.listdir(path):
        for name in os.listdir(path+resume_type):
            pos_id = name.split('-')[0]
            resume_id = name.split('-')[1].split('.')[0]

            data = {'pos_id':pos_id, 'resume_id':resume_id, 'confirm':resume_type}

            req = urllib2.Request(url=requrl, data=str(data))

            res_data = urllib2.urlopen(req)

            res = res_data.read()
            num += 1
            print num

    end = time.time()

    print (end - start)
