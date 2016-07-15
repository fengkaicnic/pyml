#coding:utf8
import pdb

with open('shujust', 'r') as file:
    lines = file.readlines()

pos_dct = {}
for line in lines:
    lst = line.strip().split(' ')
    # pdb.set_trace()
    if pos_dct.has_key(lst[1]):
        pos_dct[lst[1]] += 1
    else:
        pos_dct[lst[1]] = 1

print len(pos_dct)
for key in pos_dct.keys():
    print key, pos_dct[key]

pos_sort = sorted(pos_dct.items(), key=lambda x:int(x[0]))
pdb.set_trace()
for pos in pos_sort:
    print pos[0], pos[1]
