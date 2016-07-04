import time
import pickle
import numpy as np
import pdb

st = time.time()
R = 6378137
pie = 3.14

def compute_tm(lat, lng, lat1, lng1):
    # pdb.set_trace()
    deltalat = (lat - lat1)/2
    deltalng = (lng - lng1)/2
    S = 2*R*np.arcsin(np.sqrt(np.sin(pie*deltalat/180)**2 + np.cos(pie*lat/180)*np.cos(pie*lat1/180)*np.sin(pie*deltalng/180)*np.sin(pie*deltalng/180)))
    return S/250

wangdian_lst = []
peisong_lst = []
shanghu_lst = []
# pdb.set_trace()
with open('d:/cainiao/wangdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines[1:]:
        wangdian_lst.append(line.strip().split(','))

with open('d:/cainiao/peisongdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines[1:]:
        peisong_lst.append(line.strip().split(','))

with open('d:/cainiao/shanghu.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines[1:]:
        shanghu_lst.append(line.strip().split(','))

# pdb.set_trace()
test_lat = float(wangdian_lst[0][1])
test_lng = float(wangdian_lst[0][2])

test_lst = []

for wangdian in wangdian_lst:
    test_lst.append((wangdian[0], compute_tm(test_lat, test_lng, float(wangdian[1]), float(wangdian[2]))))

for peisong in peisong_lst:
    test_lst.append((peisong[0], compute_tm(test_lat, test_lng, float(peisong[1]), float(peisong[2]))))

for shanghu in shanghu_lst:
    test_lst.append((shanghu[0], compute_tm(test_lat, test_lng, float(shanghu[1]), float(shanghu[2]))))

test_lst = sorted(test_lst, key=lambda x:x[1])

# pdb.set_trace()

file = open('d:/cainiao/test_lst', 'wb')

pickle.dump(test_lst, file)

ed = time.time()

print ed - st
