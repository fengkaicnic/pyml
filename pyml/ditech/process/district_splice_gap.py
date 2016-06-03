#district splice gap

import pdb
import datetime

workdays = [3, 4, 5, 6, 9, 10, 11, 12, 13, 16, 17, 18, 19, 20]
weekdays = [0, 1, 2, 7, 8, 14, 15]

with open('d:/ditech/all_date_gap_id_splice.csv', 'r') as file:
    lines = file.readlines()

results = {}
for i in range(1, 67):
    results[i] = {}
    for j in range(9):
        results[i][46 + j*12] = []

for line in lines:
    line = line.strip()
    lst = line.split(',')
    for j in range(9):
        results[int(lst[1])][46 + j*12].append(int(lst[46+2+j*12]))

print len(results)
print len(results[46])

rst = []
for key in results.keys():
    # for key1 in results[key].keys():
    #     rs = [key, key1] + results[key][key1]
    #     rst.append(','.join(map(lambda x:str(x), rs)))
    # pdb.set_trace()
    items = sorted(results[key].items(), key=lambda item:item[0])
    for item in items:
        rs = [key, item[0]] + item[1]
        rst.append(','.join(map(lambda x:str(x), rs)))

rst_work = []
rst_weekend = []
for key in results.keys():
    # for key1 in results[key].keys():
    #     rs = [key, key1] + results[key][key1]
    #     rst.append(','.join(map(lambda x:str(x), rs)))
    # pdb.set_trace()
    items = sorted(results[key].items(), key=lambda item:item[0])
    for index, item in enumerate(items):
        rst_w = [key, item[0]]
        rst_e = [key, item[0]]
        for index, term in enumerate(item[1]):
            if index in workdays:
                rst_w.append(term)
            else:
                rst_e.append(term)
        rst_work.append(','.join(map(lambda x:str(x), rst_w)))
        rst_weekend.append(','.join(map(lambda x:str(x), rst_e)))

with open('d:/ditech/district_splice_gap.csv', 'wb') as file:
    file.writelines('\n'.join(rst))

with open('d:/ditech/district_splice_work_gap.csv', 'wb') as file:
    file.writelines('\n'.join(rst_work))

with open('d:/ditech/district_splice_week_gap.csv', 'wb') as file:
    file.writelines('\n'.join(rst_weekend))
