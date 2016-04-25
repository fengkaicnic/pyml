# mod item store

with open('d:/tianchi/result_jhs_14-direct-adj.csv', 'r') as file:
    lines = file.readlines()
    
result_lst = []
    
item_dct = {}
for line in lines:
    lst = line.split(',')
    item_id = lst[0]
    store_code = lst[1]
    score = lst[2]
    if store_code != 'all':
        result_lst.append(line.strip())
        if not item_dct.has_key(item_id):
            item_dct[item_id] = float(score)
        else:
            item_dct[item_id] += float(score)

for key in item_dct.keys():
    line = key + ',all,' + str(item_dct[key])
    result_lst.append(line)

with open('d:/tianchi/result_jhs_14_mod-direct-adj.csv', 'wb') as file:
    file.writelines('\n'.join(result_lst))        
