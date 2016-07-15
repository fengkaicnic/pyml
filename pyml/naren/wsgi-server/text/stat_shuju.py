#coding:utf8
import pdb

with open('shujust', 'r') as file:
    lines = file.readlines()

pos_dct = {}
for line in lines:
    lst = line.strip().split(' ')
    # pdb.set_trace()
    if pos_dct.has_key(int(lst[1])):
        pos_dct[int(lst[1])] += 1
    else:
        pos_dct[int(lst[1])] = 1

print len(pos_dct)
for key in pos_dct.keys():
    print key, pos_dct[key]

pos_sort = sorted(pos_dct.items(), key=lambda x:int(x[0]))
# pdb.set_trace()
for pos in pos_sort:
    print pos[0], pos[1]

num = 0
index = 0
for pos in pos_sort:
    if index > 5:
        break
    num += pos[0] * pos[1]
    index += 1

print num
