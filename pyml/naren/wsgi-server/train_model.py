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

path = 'd:/naren/new-data/company/'
rpath = 'D:/naren/new-data/read/'
company_lst = []

# requrl = 'http://121.40.183.7:9801/position'

start = time.time()

def model_predict():

    requrl = 'http://localhost:8000/model'

    for name in os.listdir(path):
        with open(path + name) as file:
            lines = file.readlines()
            com_dct = eval(''.join(lines))
            data = {'company':com_dct}
        break
            # data = com_dct

    for name in os.listdir(rpath):
        with open(rpath + name) as file:
            pos_id = name.split('-')[0]
            resume_id = name.split('-')[1].split('.')[0]
            lines = file.readlines()
            resume_dct = eval(''.join(lines))
            # data = {'profile':resume_dct, 'pos_id':pos_id}
            data['profile'] = resume_dct
        break

    data['action'] = 'predict'
    req = urllib2.Request(url=requrl, data=str(data))

    res_data = urllib2.urlopen(req)
    res = res_data.read()

    print res


def model_train():
    data = {}
    data['action'] = 'train'
    requrl = 'http://localhost:8000/model'

    req = urllib2.Request(url=requrl, data=str(data))
    res_data = urllib2.urlopen(req)
    res = res_data.read()

    print res

if __name__ == '__main__':
    #model_train()
    model_predict()

end = time.time()

print (end - start)
