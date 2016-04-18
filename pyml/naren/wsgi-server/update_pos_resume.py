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

path = 'd:/naren/wsgi-server/resumes/recommend/'
company_lst = []
requrl = 'http://localhost:8000/pos_resume'
confirm = 'hunter_confirm'

start = time.time()

num = 0
for name in os.listdir(path):
    pos_id = name.split('-')[0]
    resume_id = name.split('-')[1].split('.')[0]

    data = {'pos_id':pos_id, 'resume_id':resume_id, 'confirm':confirm}

    req = urllib2.Request(url=requrl, data=str(data))

    res_data = urllib2.urlopen(req)

    res = res_data.read()
    num += 1
    print num

end = time.time()

print (end - start)
