import time
import utils
import traceback
import pdb

start_time = time.time()

path = 'd:/tianchi/result_item_14_zero.csv'

with open(path, 'r') as file:
    lines = file.readlines()


try:
    conn = utils.persist.connection()
    cur = conn.cursor()

    start = '20151213'
    end = '20151227'

    result_ln = []

    for line in lines:
        lst = line.split(',')
        item_id = lst[0]
        store_code = lst[1]
        result = lst[2].strip()
        if int(result) == 0:
            if store_code == 'all':
                sql = 'select sum(qty_alipay_njhs) from item_feature where date <= "%s"\
                    and date > "%s" and item_id = %s' % (end, start, item_id)
            else:
                sql = 'select sum(qty_alipay_njhs) from item_store_feature where date <= "%s"\
                    and date > "%s" and item_id = %s and store_code = %s' % (end, start, item_id, store_code)

            cur.execute(sql)
            rst = cur.fetchall()
            # pdb.set_trace()
            result = str(rst[0][0])

        result_ln.append(','.join([item_id, store_code, result]))

    conn.close()
except:
    traceback.print_exc()
    conn.close()

# pdb.set_trace()
with open(path, 'wb') as file:
    file.writelines('\n'.join(result_ln))

end_time = time.time()

print end_time - start_time
