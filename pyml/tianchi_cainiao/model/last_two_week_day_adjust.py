#adjust last two week num

import utils
import traceback

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select item_id, store_code, count(*) from item_store_feature where date <= "20151227" and date > "20151213" group by item_id, store_code\
             having count(*) < 14'
    cur.execute(sql)
    rst = cur.fetchall()
    
    result_lst = []
    item_store_dct = {}
    for rs in rst:
        item_id = rs[0]
        store_code = rs[1]
        item_store_dct[str(item_id) + ',' + str(store_code)] = rs[2]
        
    sql1 = 'select item_id, store_code from config'
    cur.execute(sql1)
    
    item_rst = cur.fetchall()
    
    result_dct = {}
    for rt in item_rst:
        item_id = rt[0]
        store_code = rt[1]
        if store_code == 'all':
            n_sql = 'select sum(qty_alipay_njhs) from item_feature where date <= "20151227" and date > "20151213" and item_id = %d ' % (item_id)
        else:
            n_sql = 'select sum(qty_alipay_njhs) from item_store_feature where date <= "20151227" and date > "20151213" and item_id = %d and store_code = "%s"' % (item_id, store_code)
        cur.execute(n_sql)
        result = cur.fetchall()
        result_dct[str(item_id) + ',' + str(store_code)] = result[0][0]

    for key in item_store_dct.keys():
        num = item_store_dct[key]
        result_dct[key] = round(result_dct[key] * (14.0/num))
    
    for key in result_dct.keys():
        result_lst.append(key + ',' + str(result_dct[key]))
    
    with open('d:/tianchi/last_two_week_day_adjust.csv', 'wb') as file:
        file.writelines('\n'.join(result_lst))
    
    conn.close()

except:
    traceback.print_exc()
    conn.close()
    