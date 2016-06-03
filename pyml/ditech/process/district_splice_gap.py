#district splice gap

import pdb

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

with open('d:/ditech/district_splice_gap.csv', 'wb') as file:
    file.writelines('\n'.join(rst))
