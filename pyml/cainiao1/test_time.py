import time
import numpy as np
import pdb

st = time.time()

wangdian_lst = []
peisongdian_lst = []
shanghu_lst = []
test_sort = []

with open('d:/cainiao/wangdian.csv', 'r') as file:
#     pdb.set_trace()
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        wangdian_lst.append(lst)
        
lan = float(wangdian_lst[0][1])
lng = float(wangdian_lst[0][2])
R = 6378137
pie = 3.14

def compute_time(lan1, lng1):
    lan1 = float(lan1)
    lng1 = float(lng1)
    S = 2*R*np.arcsin(np.sqrt(np.sin(pie*(lan-lan1)/180)**2 + np.cos(pie*lan/180)*np.cos(pie*lan1/180)*np.sin(pie*(lng-lng1)/180)*np.sin(pie*(lng-lng1)/180)))
    tm = S/250
    return tm

with open('d:/cainiao/peisongdian.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        peisongdian_lst.append(lst)
        
with open('d:/cainiao/shanghu.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.split('\r')[1:]:
        lst = line.strip().split(',')
        shanghu_lst.append(lst)
        
for lst in wangdian_lst:
    test_sort.append((lst[0], compute_time(lst[1], lst[2])))
    
for lst in peisongdian_lst:
    test_sort.append((lst[0], compute_time(lst[1], lst[2])))

for lst in shanghu_lst:
    test_sort.append((lst[0], compute_time(lst[1], lst[2])))
    
# pdb.set_trace()
test_sort = sorted(test_sort, key=lambda x:x[1])


for index, lst in enumerate(test_sort):
    print lst
    if index > 1000:
        break

ed = time.time()

print ed -st
