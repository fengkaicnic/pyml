import os
import utils
import pdb
import time

start = time.time()

fname = 'result_last_two_week'

with open('d:/tianchi/%s.csv' % fname, 'r') as file:
    lines = file.readlines()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code, more, less from config'
    cur.execute(sql)
    item_rst = cur.fetchall()
except:
    conn.close()

item_dct = {}
for item in item_rst:
    item_dct[str(item[0])+'-'+str(item[1])] = {'more':item[2], 'less':item[3]}

print len(item_dct)

rlines = []

for line in lines:
    lst = line.split(',')

    more_s = item_dct[str(lst[0] + '-' + str(lst[1]))]['more']
    less_s = item_dct[str(lst[0] + '-' + str(lst[1]))]['less']
    per = 0.0
    adj = ''
    lst[2] = lst[2].strip()
    if more_s/less_s > 1:
        per = more_s/less_s
        adj = 'less'
    else:
        per = less_s/more_s
        adj = 'more'

    if per > 1.5:
        if adj == 'less':
            lst[2] = round(float(lst[2]) * (1 - 0.25))
        else:
            # pdb.set_trace()
            lst[2] = round(float(lst[2]) * (1 + 0.25))
    rlines.append(','.join(map(lambda x:str(x), lst)))

with open('d:/tianchi/%s.csv' % (fname+'-direct-adj') ,'wb') as fl:
    fl.writelines('\n'.join(rlines))

end = time.time()

print end - start
