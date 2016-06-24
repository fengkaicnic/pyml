#coding:utf8
import utils
import traceback
import datetime
import time
import pdb

stm = time.time()

try:
    conn = utils.persist.connection()
    sql = 'select name from company_name'
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    namelst = []
    pdb.set_trace()
    for rs in rst:
        namelst.append(rs[0])
    posql = 'select unit_name, start_time, end_time from work'
    cur.execute(posql)
    rst = cur.fetchall()
    now_day = datetime.datetime.now()
    stfp1 = '%Y-%m-%d'
    stfp2 = '%Y/%m'

    num = 0
    for rs in rst:
        for name in namelst:
            if name in rs[0].replace(u'北京', ''):
                num += 1
                try:
                    if '-' in rs[1]:
                        st = datetime.datetime.strptime(rs[1], stfp1)
                    else:
                        st = datetime.datetime.strptime(rs[1], stfp2)
                    if '-' in rs[2]:
                        ed = datetime.datetime.strptime(rs[2], stfp1)
                    else:
                        ed = datetime.datetime.strptime(rs[2], stfp2)
                    days = (ed - st).days

                    if not days:
                        days = (now_day - st).days
                    print rs[0], rs[1], rs[2], days
                except:
                    traceback.print_exc()
    print num
    conn.close()
except:
    traceback.print_exc()
    conn.close()

edm = time.time()

print edm - stm
