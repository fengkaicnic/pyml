import utils
import numpy as np
from scipy import stats
import pdb
import time
import traceback

start = time.time()

def generate_result(start_date, end_date):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        
        sql = 'select item_id, store_code, doublet from config '
        cur.execute(sql)
        rst = cur.fetchall()
        
        result_lst = []
        for rs in rst:
            item_id = rs[0]
            store_code = rs[1]
            doublee = rs[2]
            if store_code == 'all':
                p_sql = 'select qty_alipay_njhs from item_feature where date > "%s" and date <= "%s" and item_id = %d' % (start_date, end_date, item_id)
            else:
                p_sql = 'select qty_alipay_njhs from item_store_feature where date > "%s" and date <= "%s" and item_id = %d and store_code = "%s"' % \
                                                (start_date, end_date, item_id, store_code)
            item_lst = []
            cur.execute(p_sql)            
            item_rst = cur.fetchall()
            termary = []
            for item in item_rst:
                termary.append(item[0])
            termary = np.array(termary)
            mean = termary.mean()
            std = termary.std()
            item_lst.append(item_id)
            item_lst.append(store_code)
            nums = termary.sum()
            if doublee == 1:
                nums = nums * 1.1

            item_lst.append(nums)
            
            result_lst.append(','.join(map(lambda x:str(x), item_lst)))
        conn.close()
        
        with open('d:/tianchi/December_last_two_week10.csv', 'wb') as file:
            file.writelines('\n'.join(result_lst))
        
    except:
        traceback.print_exc()
        
if __name__ == '__main__':
    start_date = '20151213'
    end_date = '20151227'
    generate_result(start_date, end_date)
        
end = time.time()

print end - start
