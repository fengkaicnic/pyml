import numpy as np
import utils
import pdb

utils.get_didian()
# pdb.set_trace()
wangdian_dct = utils.wangdian_dct
peisongdian_dct = utils.peisongdian_dct
shanghu_dct = utils.shanghu_dct
o2olst = []

tclst = []
tc_dct = {}
dsdct = {}
peisongs = set()

kuaidiyuan_dct = {}

for i in range(11):
    kuaidiyuan_dct[i] = ['B4596', 0]

with open('d:/cainiao/tongcheng.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines[1:]:
        lst = line.strip().split(',')
        peisongdian = lst[1]
        shanghu = lst[2]
        peisongs.add(peisongdian)
        ds = utils.compute_tm(shanghu_dct[shanghu], peisongdian_dct[peisongdian])
        if dsdct.has_key(round(ds[1])):
            dsdct[round(ds[1])] += 1
        else:
            dsdct[round(ds[1])] = 1
        tm = (int(lst[3].split(':')[0]) - 8) * 60 + int(lst[3].split(':')[1])
        o2olst.append([tm, round(ds[1]), round(3*np.sqrt(int(lst[-1]))), shanghu, peisongdian, 0])
        tclst.append(tm)

o2olst = sorted(o2olst, key=lambda x:x[0])
for o2o in o2olst:
    print o2o[0], o2o[1], o2o[2]

# pdb.set_trace()
for tme in range(210, 630):
    for o2o in o2olst:
        flag = 0
        if o2o[0] > tme:
           break
        if o2o[0] < tme:
            continue
        o2oshanghu = o2o[-3]
        o2osong = o2o[-2]
        for key in kuaidiyuan_dct.keys():
            kdy = kuaidiyuan_dct[key]
            peisong = kdy[0]
            peisongtm = kdy[1]
            distance = utils.compute_tm(shanghu_dct[o2oshanghu], peisongdian_dct[peisong])
            if peisongtm + distance[-1] < tme:
                kuaidiyuan_dct[key] = [o2osong, tme + o2o[1] + o2o[2]]
                flag = 1
                break
        # pdb.set_trace()
        if flag:
            continue
        kuaidiyuan_dct[max(kuaidiyuan_dct.keys()) + 1] = [o2osong, tme + o2o[1] + o2o[2]]

for key in kuaidiyuan_dct.keys():
    print key
