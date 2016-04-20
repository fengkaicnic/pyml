#coding:utf8

import utils
import traceback
import datetime
import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
import time

start = time.time()

period = 7

# period_rst = [4, 5, 6, 7, 8]
period_rst = [0, 3, 4, 7, 8, 9, 10]


def gbdt_item(train_rst, test_rst, store_code):
    
    gbdt=GradientBoostingRegressor(
      loss='ls',
      learning_rate=0.1,
      n_estimators=100,
      subsample=1,
      min_samples_split=2,
      min_samples_leaf=1,
      max_depth=3,
      init=None,
      random_state=None,
      max_features=None,
      alpha=0.9,
      verbose=0,
      max_leaf_nodes=None,
      warm_start=False
    )
    train_feat = np.array(train_rst)
    try:
        train_item_ids = train_feat[:, train_feat.shape[1]-1]
    except:
        pdb.set_trace()
        traceback.print_exc()
    train_id=train_feat[:, train_feat.shape[1]-2]
    train_feat = train_feat[:, :train_feat.shape[1]-2]
    test_feat = test_rst
#     pdb.set_trace()
    test_item_id = test_feat[-1]
    test_feat = test_feat[:-1]
    
    gbdt.fit(train_feat, train_id)
    # joblib.dump(gbdt, 'model')
    pred=gbdt.predict(test_feat)
    result_lst = []
    for index, pred_data in enumerate(pred):
        lst = []
        lst.append(int(test_item_id))
        lst.append(store_code)
        lst.append(int(round(pred_data)) * (14/period))
        result_lst.append(','.join(map(lambda x: str(x), lst)))
    
    return result_lst[0]


def generate_item_test(item_id, store_code):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        start_date = datetime.datetime(2014, 10, 1)
        item_date = datetime.datetime(2015, 12, 27)
        tem_dct = {}
        result_lst = []
        for num in range(1):
            if item_date - datetime.timedelta(num * period) < start_date:
                break
            en_date = (item_date - datetime.timedelta(num * period)).strftime('%Y%m%d')
            st_date = (item_date - datetime.timedelta((num + 1) * period)).strftime('%Y%m%d')
            if store_code == 'all':
                sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv), sum(ss_pv_ipv), sum(ss_pv_uv), sum(qty_alipay_njhs)\
                 from item_feature where date > "%s" and date <= "%s" and item_id = %d' % (st_date, en_date, item_id)
            else:
                sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv), sum(ss_pv_ipv), sum(ss_pv_uv), sum(qty_alipay_njhs)\
                 from item_store_feature where store_code = "%s" and date > "%s" and date <= "%s" and item_id = %d' % (store_code, st_date, en_date, item_id)
            cur.execute(sql)
            f_rst = cur.fetchall()
#             pdb.set_trace()
            result_lst.append(f_rst[0][0])
            result_lst.append(f_rst[0][1])
            result_lst.append(f_rst[0][2])
            result_lst.append(f_rst[0][3])
            result_lst.append(f_rst[0][4])
            result_lst.append(f_rst[0][5])
            result_lst.append(f_rst[0][6])
            result_lst.append(f_rst[0][7])
            result_lst.append(item_id)
            result_lst = [x or 0 for x in result_lst]
        
        return result_lst
                
        conn.commit()
        conn.close()
    
    except Exception as e:
        traceback.print_exc()
        pdb.set_trace()
        conn.close()
        print e


def predict_item(item_id, store_code):
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        start_date = datetime.datetime(2014, 10, 1)
        item_date = datetime.datetime(2015, 12, 27)
        tem_dct = {}
        result_lst = []
        for num in [4, 5, 6, 7, 8]:
            rst_ls = []
            if item_date - datetime.timedelta(num * period) < start_date:
                break
            e_date = (item_date - datetime.timedelta(num * period)).strftime('%Y%m%d')
            s_date = (item_date - datetime.timedelta((num + 1) * period)).strftime('%Y%m%d')
            if store_code == 'all':
                sql_num = 'select sum(qty_alipay_njhs) from item_feature where \
                             date <= "%s" and date > "%s" and item_id = %d' % (e_date, s_date, item_id)
            else:
                sql_num = 'select sum(qty_alipay_njhs) from item_store_feature where \
                             date <= "%s" and date > "%s" and item_id = %d and store_code = "%s"' % (e_date, s_date, item_id, store_code)
            cur.execute(sql_num)
            r_num = cur.fetchall()
            
            en_date = s_date
            st_date = (item_date - datetime.timedelta((num + 2) * period)).strftime('%Y%m%d')
            if store_code == 'all':
                sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv), sum(ss_pv_ipv), sum(ss_pv_uv), sum(qty_alipay_njhs)\
                 from item_feature where date > "%s" and date <= "%s" and item_id = %d' % (st_date, en_date, item_id)
            else:
                sql = 'select sum(pv_ipv), sum(pv_uv), sum(cart_ipv), sum(cart_uv), sum(collect_uv), sum(ss_pv_ipv), sum(ss_pv_uv), sum(qty_alipay_njhs)\
                 from item_store_feature where date > "%s" and date <= "%s" and item_id = %d and store_code = "%s"' % (st_date, en_date, item_id, store_code)
            cur.execute(sql)
            f_rst = cur.fetchall()
            rst_ls.append(f_rst[0][0])
            rst_ls.append(f_rst[0][1])
            rst_ls.append(f_rst[0][2])
            rst_ls.append(f_rst[0][3])
            rst_ls.append(f_rst[0][4])
            rst_ls.append(f_rst[0][5])
            rst_ls.append(f_rst[0][6])
            rst_ls.append(f_rst[0][7])
            rst_ls.append(r_num[0][0])
            rst_ls.append(item_id)
            rst_ls = [x or 0 for x in rst_ls]
            result_lst.append(rst_ls)
        
        conn.close()
        
        return result_lst
    
    except Exception as e:
        traceback.print_exc()
        conn.close()
        print e
    
    
def generate_model():
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select item_id, store_code from config'
        cur.execute(sql)
        result_lst = []
        rst = cur.fetchall()
        nm = 0
        for item in rst:
            nm += 1
            train_lst = predict_item(item[0], item[1])
            test_lst = generate_item_test(item[0], item[1])
            result = gbdt_item(train_lst, test_lst, item[1])
            result_lst.append(result)
            print nm
        
        with open('d:/tianchi/result_item_%d.csv' % period, 'wb') as file:
            file.writelines('\n'.join(result_lst))
    except:
        traceback.print_exc()


if __name__ == '__main__':
    generate_model()

end = time.time()

print (end - start)
