import os

with open('d:/tianchi/result_item_14-adj.csv', 'r') as file:
    lines = file.readlines()

store = 0.0
all = 0.0

for line in lines:
    resut = line.split(',')
    if resut[1] == 'all':
        all += float(resut[2])
    else:
        store += float(resut[2])

print 'store:', str(store)
print 'all', str(all)