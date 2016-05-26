import utils
import traceback
import pdb

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select * from weather where date = "%s" order by splice' % '2016-01-21'
    cur.execute(sql)
    rst = cur.fetchall()
    gaped_splice = []
    splice = 1
    pdb.set_trace()
    for rs in rst:
        if splice == rs[5]:
            splice += 1
            continue
        num = rs[5] - splice
        # pdb.set_trace()
        while num > 0:
            sql = 'insert into weather(date, splice) values ("2016-01-21", %d)' % int(splice)
            cur.execute(sql)
            num -= 1
            splice += 1

    conn.commit()
    conn.close()
except:
    traceback.print_exc()
    conn.close()
