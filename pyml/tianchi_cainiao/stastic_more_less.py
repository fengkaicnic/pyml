import utils
import traceback
import pdb
import time

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select more, less, item_id, store_code from config'

    cur.execute(sql)
    rst = cur.fetchall()
    lst = [(0, 0, 0) for i in range(10)]
    for rs in rst:
        item_id = rs[2]
        store_code = rs[3]
        more = rs[0]
        less = rs[1]
        if store_code == 'all':
            psql = 'select sum(qty_alipay_njhs) from item_feature where dateid < 15\
                    and item_id = %d' % item_id
        else:
            psql = 'select sum(qty_alipay_njhs) from item_store_feature where dateid < 15 \
                      and item_id = %d and store_code = %s' % (item_id, store_code)

        cur.execute(psql)
        result = cur.fetchall()
        # pdb.set_trace()
        if not result[0][0]:
            num = 0
        else:
            num = result[0][0]
        if more > less:
            rss = float(less) * float(num)
        else:
            rss = float(more) * float(num)

        lst = sorted(lst, key=lambda tf:tf[0], reverse=True)

        if lst[-1][0] < rss:
            lst.pop()
            lst.append((rss, item_id, store_code, more, less, num))

    for ls in lst:
        print ls

except:
    pdb.set_trace()
    traceback.print_exc()

end = time.time()

print end -start
