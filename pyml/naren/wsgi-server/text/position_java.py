#coding:utf8
import utils
import sys
import extrace_company
import pdb
import traceback
reload(sys)
import re
import time
sys.setdefaultencoding('utf8')

st = time.time()

salaryp = re.compile(r'\d+')
conn = utils.persist.connection()

cur = conn.cursor()

sql = 'select id, latestsalary, latesttitle, latestdegree, latestcollege, dessalary, \
                              resume_id from profile where latesttitle like "%java%"'

pdb.set_trace()
cur.execute(sql)

rst = cur.fetchall()
work_lst = []
salary_dct = {}
# pdb.set_trace()
for rs in rst:
    if not salary_dct.has_key(rs[1]):
        salary_dct[rs[1]] = 1
    else:
        salary_dct[rs[1]] += 1
    works = [x for x in rs[:-1]]
    resume_id = rs[-1]
    sqlw = 'select unit_name, start_time, end_time from work where resume_id = "%s"' % resume_id
    # pdb.set_trace()
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
    # if index > 90:
    #     break
# for key in salary_dct.keys():
#     print key, salary_dct[key]
    # incomes = salaryp.findall(key)
    # print incomes
    # if incomes:
    #     # pdb.set_trace()
    #     low_income = incomes.group(0)
    #     print low_income
ed = time.time()

print ed - st
