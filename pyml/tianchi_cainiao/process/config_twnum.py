#add last two week num in the config table
#

import time
import utils
import traceback

start = time.time()
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code from config'
    cur.execute(sql)
    rst = cur.fetchall()
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            nm_sql = 'select sum(qty_alipay_njhs) from item_feature where dateid >= 1 and\
                      dateid <= 14 and item_id = %d' % item_id
        else:
            nm_sql = 'select sum(qty_alipay_njhs) from item_store_feature where dateid >= 1 and\
                      dateid <= 14 and store_code = %s and item_id = %d' % (store_code, item_id)

        cur.execute(nm_sql)
        result = cur.fetchall()
        if not result[0][0]:
            num = 0
        else:
            num = int(result[0][0])
        u_sql = 'update config set twnum = %d where item_id = %d and store_code = "%s"'\
                  % (num, item_id, store_code)

        cur.execute(u_sql)

    conn.commit()
    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
