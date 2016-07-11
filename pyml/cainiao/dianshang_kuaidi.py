import utils
import numpy as np
import pdb
import traceback

utils.get_didian()
# pdb.set_trace()
wangdian_dct = utils.wangdian_dct
peisongdian_dct = utils.peisongdian_dct
shanghu_dct = utils.shanghu_dct
dianshang_dct = {}
wangdiannum_dct = {}
kuaidiyuan_dct = {}

kdcount = 671

for i in range(669):
    kuaidiyuan_dct[i] = []

with open('d:/cainiao/dianshang.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0].split('\r')
    for line in lines[1:]:
        lst = line.split(',')
        dianshang_dct[lst[1]] = int(lst[-1])
        if not wangdiannum_dct.has_key(lst[2]):
            wangdiannum_dct[lst[2]] = int(lst[-1])
        else:
            wangdiannum_dct[lst[2]] += int(lst[-1])
num2 = 0
for key in wangdiannum_dct.keys():
    num = wangdiannum_dct[key]
    tfp = num*kdcount/229780.0
    print key, num*kdcount/229780.0
    if tfp < 1:
        num2 += 1
        wangdiannum_dct[key] = [num, 1]
    else:
        num2 += round(num*kdcount/229780.0)
        wangdiannum_dct[key] = [num, round(num*kdcount/229780.0)]

print num2
prim_dct = {}

with open('d:/cainiao/primtree.csv', 'r') as file:
    lines = file.readlines()
    for line in lines:
        lst = line.strip().split(',')
        prim_dct[lst[0]] = lst[1:]

kuaidinum = 0

handles = []
# pdb.set_trace()
huowucount = 0
for key in prim_dct.keys():

    num = int(wangdiannum_dct[key][1])
    lst = prim_dct[key]
    for i in range(num):
        total = 0
        kuaidiyuan_dct[kuaidinum].append(key)
        for ls in lst[1:]:
            if ls in handles:
                continue
            total += dianshang_dct[ls]
            if total < 140:
                kuaidiyuan_dct[kuaidinum].append((ls, dianshang_dct[ls]))
                handles.append(ls)
                huowucount += dianshang_dct[ls]
            else:
                break
        kuaidinum += 1
        print kuaidinum

kuaidis = []
timecount = 0
try:
    for key in kuaidiyuan_dct.keys():
        kuaidiyuanm = 0
        # print key, kuaidiyuan_dct[key]
        lst = kuaidiyuan_dct[key]
        stpot = wangdian_dct[lst[0]][0]
        for ls in lst[1:]:
            edpot = peisongdian_dct[ls[0]]
            # pdb.set_trace()
            tm = utils.compute_tm(stpot, edpot)
            tm = tm[-1]
            tm += 3*np.sqrt(ls[1]) + 5
            stpot = edpot
            kuaidiyuanm += tm
        # print key, kuaidiyuanm
        kuaidis.append([key, kuaidiyuanm])
        timecount += kuaidiyuanm
except:
    pdb.set_trace()
    traceback.print_exc()

kuaidis = sorted(kuaidis, key=lambda x:x[1])

for kd in kuaidis:
    print kd

print timecount
print huowucount
