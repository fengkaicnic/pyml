#test git
#coding:utf8
import os
import json
import re
import MySQLdb
import sys
reload(sys)

mode = re.compile(r'\d+')
sys.setdefaultencoding('utf8')
def get_pos():
    position_dct = {}
    with open('position.properties') as file:
        lines = file.readlines()
        print lines
        for line in lines:
            linelst = line.split(',')
            for key in linelst[:-3]:
                #linelst[-1] = linelst[-1][:-1]
                linelst[-1] = linelst[-1].replace('\n', '')
                position_dct[key] = linelst[-3:]
    return position_dct

if __name__ == '__main__':
    lct = get_pos()
    for items in lct.items():
        print items
