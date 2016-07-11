import utils
import pdb
import numpy as np
import time

st = time.time()

tclst = []
tc_dct = {}
dsdct = {}
peisongs = set()

utils.get_didian()
# pdb.set_trace()
wangdian_dct = utils.wangdian_dct
peisongdian_dct = utils.peisongdian_dct
shanghu_dct = utils.shanghu_dct
o2olst = []

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
        o2olst.append((tm, round(ds[1]), round(3*np.sqrt(int(lst[-1])))))
        tclst.append(tm)

tclst = sorted(tclst)
for tc in tclst:
    if not tc_dct.has_key(tc):
        tc_dct[tc] = 1
    else:
        tc_dct[tc] += 1

tcsrt = sorted(tc_dct.items(), key=lambda x:x[0])
num = 0
for tc in tcsrt:
    print tc[0], tc[1]

    num += 1
print num

num1 = 0
dsort = sorted(dsdct.items(), key=lambda x:x[0])

for ds in dsort:
    # print ds[0], ds[1]
    num1 += 1

print num1
print len(peisongs)
num2 = 0
o2olst = sorted(o2olst, key=lambda x:x[0])
for o2o in o2olst:
    print o2o[0], o2o[1], o2o[2]
    if o2o[0] < 231:
        num2 += 1

ed = time.time()

print num2
print ed - st
