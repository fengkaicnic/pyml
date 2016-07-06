#coding:utf8
import utils
import sys
import extrace_company
import pdb
import traceback
reload(sys)
import time
sys.setdefaultencoding('utf8')

st = time.time()

conn = utils.persist.connection()

cur = conn.cursor()

sql = 'select latestsalary, latesttitle, latestdegree, latestcollege, dessalary, \
                              resume_id from profile where latesttitle like "%java%"'

cur.execute(sql)

rst = cur.fetchall()
work_lst = []
for rs in rst:
    works = [x for x in rs[:-1]]
    resume_id = rs[5]
    sqlw = 'select unit_name, start_time, end_time from work where resume_id = "%s"' % resume_id
    cur.execute(sqlw)
    rstw = cur.fetchall()

    for rsw in rstw:
        works.append(rsw[0])
        days = extrace_company.computem(rsw)
        works.append(days)

    work_lst.append(works)

print len(work_lst)

for index, work in enumerate(work_lst):
    try:
        print ','.join(map(lambda x:str(x), work))
    except:
        pdb.set_trace()
        traceback.print_exc()
    if index > 10:
        break

ed = time.time()

print ed - st
