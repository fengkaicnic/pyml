#coding:utf8
import utils
import traceback

try:
    conn = utils.persist.connection()
    sql = 'select name from company_name'
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    namelst = []
    for rs in rst:
        namelst.append(rs[0])
    posql = 'select position_name from work'
    cur.execute(posql)
    rst = cur.fetchall()
    num = 0
    for rs in rst:
        for name in namelst:
            if name in rs[0]:
                print rs[0];num+=1
                print num

    conn.close()
except:
    traceback.print_exc()
    conn.close()
