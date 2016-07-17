import time
import numpy as np
import pdb
import math

st = time.time()

wangdian_dct = {}
peisongdian_dct = {}
shanghu_dct = {}
test_sort = []
wangdian1_lst = []
wangdian1 = 'A001'

with open('d:/cainiao/wangdian.csv', 'r') as file:
#     pdb.set_trace()
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        if lst[0] == wangdian1:
            wangdian_dct[lst[0]] = ((lst[1], lst[2]))
            break
        
lan = float(wangdian_dct[wangdian1][0])
lng = float(wangdian_dct[wangdian1][1])
R = 6378137
pie = 3.14

def compute_time(lan, lng, lan1, lng1):
    lan = float(lan)
    lng = float(lng)
    lan1 = float(lan1)
    lng1 = float(lng1)
    S = 2*R*np.arcsin(np.sqrt(np.sin(pie*(lan-lan1)/180)**2 + np.cos(pie*lan/180)*np.cos(pie*lan1/180)*np.sin(pie*(lng-lng1)/180)*np.sin(pie*(lng-lng1)/180)))
    tm = S/250
    return tm

pdb.set_trace()
with open('d:/cainiao/dianshang.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        if lst[2] == wangdian1:
            wangdian_dct[lst[1]] = ''

pdb.set_trace()
with open('d:/cainiao/tongcheng.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        if wangdian_dct.has_key(lst[1]):
            wangdian_dct[lst[2]] = ''

with open('d:/cainiao/peisongdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        if wangdian_dct.has_key(lst[0]):
            wangdian_dct[lst[0]] = (lst[1], lst[2])
        
with open('d:/cainiao/shanghu.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        if wangdian_dct.has_key(lst[0]):
            wangdian_dct[lst[0]] = (lst[1], lst[2])

lst3 = [(x, y) for x in wangdian_dct.keys() for y in wangdian_dct.keys()]
print len(lst3)
print len(wangdian_dct)
print lst3
for lstt in lst3:
    print lstt[0], lstt[1], compute_time(wangdian_dct[lstt[0]][0], wangdian_dct[lstt[0]][1], wangdian_dct[lstt[1]][0], wangdian_dct[lstt[1]][1])
    
# pdb.set_trace()
test_sort = sorted(test_sort, key=lambda x:x[1])


for index, lst in enumerate(test_sort):
    print lst
    if index > 1000:
        break

ed = time.time()

print ed -st
