import time

start = time.time()

path1 = 'd:/tianchi/result_14.csv'
path2 = 'd:/tianchi/result_jhs_14.csv'

with open(path1, 'r') as file:
    lines14 = file.readlines()

with open(path2, 'r') as file:
    lineswk = file.readlines()

line14_dct = {}

result_lst = []
for line in lines14:
    terms = line.split(',')
    item_id = terms[0]
    store_code = terms[1]
    score = terms[2]
    line14_dct[item_id+'_'+store_code] = float(score)

linewk_dct = {}
for line in lineswk:
    terms = line.split(',')
    item_id = terms[0]
    store_code = terms[1]
    score = terms[2]
    linewk_dct[item_id+'_'+store_code] = float(score)

for key in linewk_dct.keys():
    print key, line14_dct[key], linewk_dct[key], line14_dct[key] - linewk_dct[key]
    result_lst.append(key.replace('_', ',') + ',' + str(round((line14_dct[key] + linewk_dct[key])/2)))

# with open('d:/tianchi/mean_14_twoweek.csv', 'wb') as file:
#     file.writelines('\n'.join(result_lst))
