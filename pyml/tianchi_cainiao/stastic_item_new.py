import utils
import traceback

import pdb
import time

start = time.time()

try:
    conn = utils.persist.connection()
    sql = 'select item_id, store_code from config'
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()

    start_date = '20151213'

    num = 0
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        if store_code == 'all':
            psql = 'select sum(qty_alipay_njhs) from item_feature where item_id = %d and date > "%s"' \
                    % (item_id, start_date)
        else:
            psql = 'select sum(qty_alipay_njhs) from item_store_feature where item_id = %d and store_code = "%s"\
                        and date > "%s" order by date desc' % (item_id, store_code, start_date)

        cur.execute(psql)
        prst = cur.fetchall()
        lst = []
        lst.append(item_id)
        lst.append(store_code)

        if prst and prst[0][0] > 1000:
            lst.append(item_id)
            lst.append(store_code)

            for pr in prst:
                # if pr[0] == None:
                #     pdb.set_trace()
                lst.append(pr[0])
            print lst
            num += 1
        # elif prst[0][0] == None:
        #     print lst
        # if not prst:
        #     num += 1
    print num

except:
    traceback.print_exc()


end = time.time()
print end - start
