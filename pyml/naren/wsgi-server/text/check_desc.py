#coding:utf8
import time
import utils
import traceback
import pdb

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    # sql = 'select low_income, high_income, low_workage, high_workage, description, \
               # position_name, naren_created from company where id > %d' % 459
    sql = 'select id, dessalary from profile where id > %d ' % 803208
    cur.execute(sql)

    rst = cur.fetchall()
    pdb.set_trace()
    for rs in rst:
        # print utils.discrement_unicode(rs[1])
        print rs[0]
        try:
            usql = '''update profile set dessalary = "%s" where id = %d''' % (utils.discrement_unicode(rs[1]), rs[0])
            cur.execute(usql)
        except:
            pdb.set_trace()
            traceback.print_exc()


    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()

lu = time.time()

print lu - start
