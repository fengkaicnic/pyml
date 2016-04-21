import os
import utils
import pdb
import traceback
import time

start = time.time()

start_date = '20151213'
end_date = '20151227'

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code from config'
    cur.execute(sql)
    items = cur.fetchall()
    result = []
    for item in items:
        item_id = item[0]
        store_code = item[1]
        if store_code == 'all':
            item_sql = 'select sum(qty_alipay_njhs) from item_feature where item_id = %d\
                    and date <= "%s" and date > "%s"' % (item_id, end_date, start_date)
        else:
            item_sql = 'select sum(qty_alipay_njhs) from item_store_feature where item_id = %d \
                        and store_code = %s and date <= "%s" and date > "%s"' % (item_id, \
                        store_code, end_date, start_date)

        cur.execute(item_sql)
        rst = cur.fetchall()
        qty_num = rst[0][0]
        result.append(','.join([str(item_id), str(store_code), str(qty_num)]))

    conn.close()

    with open('d:/tianchi/result_last_two_week.csv', 'wb') as file:
        file.writelines('\n'.join(result))

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start
