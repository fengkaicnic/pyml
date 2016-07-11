import numpy as np

import time
import pdb

st = time.time()

wangdian_dct = {}
peisongdian_dct = {}
shanghu_dct = {}
num2 = 0

with open('d:/cainiao/wangdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].strip().split('\r')
    for line in lines[1:]:
        lst = line.strip().split(',')
        wangdian_dct[lst[0]] = [(float(lst[1]), float(lst[2]))]

with open('d:/cainiao/peisongdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].strip().split('\r')
    for line in lines[1:]:
        lst = line.strip().split(',')
        peisongdian_dct[lst[0]] = [float(lst[1]), float(lst[2])]

with open('d:/cainiao/shanghu.csv', 'r') as file:
    lines = file.readlines()
    for line in lines[1:]:
        lst = line.strip().split(',')
        shanghu_dct[lst[0]] = [float(lst[1]), float(lst[2])]

with open('d:/cainiao/dianshang.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].strip().split('\r')
    for line in lines[1:]:
        lst = line.strip().split(',')
        wangdian_dct[lst[2]].append((lst[1], peisongdian_dct[lst[1]][0], peisongdian_dct[lst[1]][1], float(lst[3])))
        peisongdian_dct[lst[1]].append(lst[2])

# with open('d:/cainiao/tongcheng.csv', 'r') as file:
#     lines = file.readlines()
#     for line in lines[1:]:
#         lst = line.strip().split(',')
#         wangdian_dct[peisongdian_dct[lst[1]][-1]].append((lst[2], shanghu_dct[lst[2]][0], shanghu_dct[lst[2]][1], float(lst[-1])))
#         shanghu_dct[lst[2]].append(peisongdian_dct[lst[1]][-1])

# pdb.set_trace()

R = 6378137
pie = 3.14
def compute_tm(wangdian, songdian):
    # pdb.set_trace()
    lng = wangdian[0]
    lat = wangdian[1]
    lng1 = songdian[1]
    lat1 = songdian[2]
    deltalat = (lat - lat1)/2
    deltalng = (lng - lng1)/2
    S = 2*R*np.arcsin(np.sqrt(np.sin(pie*deltalat/180)**2 + np.cos(pie*lat/180)*np.cos(pie*lat1/180)*np.sin(pie*deltalng/180)*np.sin(pie*deltalng/180)))
    # pdb.set_trace()
    tm = S/250 + 3*np.sqrt(songdian[-1]) + 5
    return (songdian, tm)

def prim_cmp(lst):
    wangdian = lst[0]
    wanglst = [lst[0]]
    for i in range(len(lst)):
        sort_lst = []
        for index, ls in enumerate(lst):
            if ls in wanglst:
                continue
            tm = compute_tm(wangdian, ls)
            sort_lst.append(tm)
        sort_lst = sorted(sort_lst, key=lambda x:x[1])
        # pdb.set_trace()

        if sort_lst:
            wangdian = sort_lst[0][0][1:3]
            wanglst.append(sort_lst[0][0])
    return wanglst

results = []
num = 0

for key in wangdian_dct.keys():
    result = []
    dst = wangdian_dct[key]
    result.append(key)
    lst = prim_cmp(dst)
    for ls in lst[1:]:
        result.append(ls[0])
    results.append(','.join(result))
    print key, len(lst), len(dst)
    num += len(lst)
    # pdb.set_trace()

for key in wangdian_dct.keys():
    dst = wangdian_dct[key]
    nums = 0
    for ls in dst:
        if len(ls) == 4:
            nums += ls[3]
    print key, nums


with open('d:/cainiao/primtree.csv', 'wb') as file:
    file.writelines('\n'.join(results))

ed = time.time()

print num
print ed - st
