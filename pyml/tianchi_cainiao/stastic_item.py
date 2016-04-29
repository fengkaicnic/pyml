#coding:utf8
#this program is to generate two week data
#two week datas amt_alipay
#but the result is some week the amt_alipay
#is 0, maybe periodicity but can not prove
#the conclusion

import os
import json
import sys
import re
reload(sys)
sys.setdefaultencoding('utf8')
import utils
import types
import traceback
import datetime
import pdb
import time

start = time.time()

period = 14
try:

    conn = utils.persist.connection()
    cur = conn.cursor()
    cur.execute('set character_set_client=utf8')
    cur.execute('set character_set_connection=utf8')
    cur.execute('set character_set_database=utf8')
    cur.execute('set character_set_results=utf8')
    cur.execute('set character_set_server=utf8')
    conn.commit()
    sql = 'select distinct(item_id) from config'
    cur.execute(sql)
    rst = cur.fetchall()
    start_date = datetime.datetime(2014, 10, 1)
    item_date = datetime.datetime(2015, 12, 27)
    tem_dct = {}
    for num in range(70):
        if item_date - datetime.timedelta(num * period) < start_date:
            break
        e_date = (item_date - datetime.timedelta(num * period)).strftime('%Y%m%d')
        s_date = (item_date - datetime.timedelta((num + 1) * period)).strftime('%Y%m%d')
        for tid in rst:
            if not tem_dct.has_key(tid[0]):
                tem_dct[tid[0]] = [[] for i in range(5)]
            for lst in tem_dct[tid[0]]:
                lst.append(0)
                # lst.append(0)
            termsql = 'select amt_alipay, store_code, num_alipay, date, amt_alipay_njhs, qty_alipay_njhs, pv_uv from \
                         item_store_feature where item_id = %d and date > %s and date < %s \
                         ' % (tid[0], s_date, e_date)
            cur.execute(termsql)
            termrst = cur.fetchall()
            for term in termrst:
                tem_dct[tid[0]][term[1]-1][num] += term[5]
                # tem_dct[tid[0]][term[1]-1][(num * 2) + 1] += round(term[5]/(term[6]+0.001), 5)
        # pdb.set_trace()

    # print tem_dct
    lines = []
    for key in tem_dct.keys():
        tems = tem_dct[key]
        lines.append(str(key))
        for tem in tems:
            for index, x in enumerate(tem[::-1]):
                if type(x) is types.IntType:
                    tem.pop()
                else:
                    break
            lines.append(','.join(map(lambda x:str(x), tem)))

    with open('d:/tianchi/test_tem_%d' % period, 'wb') as file:
        file.writelines('\n'.join(lines))


    conn.commit()
    conn.close()

except Exception as e:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
    print e

end = time.time()

print (end - start)