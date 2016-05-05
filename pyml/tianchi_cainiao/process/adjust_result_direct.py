import os
import utils
import pdb
import time

start = time.time()

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


def judge_more_less(lst):
    more_s = item_dct[str(lst[0] + '-' + str(lst[1]))]['more']
    less_s = item_dct[str(lst[0] + '-' + str(lst[1]))]['less']
    per = 0.0
    adj = ''
    lst[2] = lst[2].strip()
    more_sum = 0
    less_sum = 0
    if more_s/less_s > 1:
        per = more_s/less_s
        adj = 'less'
    else:
        per = less_s/more_s
        adj = 'more'

    if per > 1.0:
        if adj == 'less':
            more_sum -= round(float(lst[2]) * 0.25)
            lst[2] = round(float(lst[2]) * (1 - 0.25))
            # lst[2] = float(lst[2]) + more_sum
        else:
            # pdb.set_trace()
            less_sum += round(float(lst[2]) * 0.25)
            lst[2] = round(float(lst[2]) * (1 + 0.25))
            # lst[2] = float(lst[2]) + less_sum

    return lst[2], more_sum, less_sum

if __name__ == '__main__':

    fname = 'result_last_two_week'
    
    with open('d:/tianchi/%s.csv' % fname, 'r') as file:
        lines = file.readlines()
    
    rlines = []

    more_sum = 0
    less_sum = 0
    
    for line in lines:
        line = line.replace('\x00', '')
        lst = line.split(',')
    
        num, more_s, less_s = judge_more_less(lst)
        lst[2] = num
        more_sum += more_s
        less_sum += less_s
        rlines.append(','.join(map(lambda x:str(x), lst)))
    
    with open('d:/tianchi/%s.csv' % (fname+'-direct-adj') ,'wb') as fl:
        fl.writelines('\n'.join(rlines))

    print more_sum
    print less_sum

    end = time.time()
    
    print end - start
