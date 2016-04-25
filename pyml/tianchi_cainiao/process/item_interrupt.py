import time
import utils
import traceback

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code, id from config'
    cur.execute(sql)

    rst = cur.fetchall()

    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            continue
        ID = rs[2]
        p_sql = 'select dateid from item_store_feature where item_id = %d and\
                  store_code = %s' % (item_id, store_code)
        cur.execute(p_sql)
        numlt = []
        result = cur.fetchall()
        for rt in result:
            numlt.append(rt[0])
        if not numlt:
            continue
        numlt = sorted(numlt)
        interrupt = (numlt[-1] - numlt[0] + 1) - len(numlt)

        usql = 'update config set rup = %d, days = %d, eday = %d where id = %d '\
               % (interrupt, len(numlt), numlt[0], ID)
        cur.execute(usql)
        conn.commit()

    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
