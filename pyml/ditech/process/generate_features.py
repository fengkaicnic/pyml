#generate features
#temperature, pm2.5, weekday, traffic, onehot

import utils
import traceback
import copy
import datetime
import pdb
import time

start = time.time()

all_date_splice_dct = {}
all_date_splice_gap_dct = {}
all_date_splice_test_dct = {}
all_date_gap_test_dct = {}

tem_one_hot = [0, 0, 0, 0, 0, 0, 0, 0, 0]
week_hot = [0, 0, 0, 0, 0, 0, 0]
skip_day = ['2016-01-01', '2016-01-02', '2016-01-03']
traffic_hot = [0, 0, 0, 0]

def get_all_splice():
    with open('d:/ditech/all_date_splice.csv', 'r') as file:
        lines = file.readlines()
    with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
        tlines = file.readlines()

    for i in range(len(lines)):
        lst = lines[i].strip().split(',')
        if all_date_splice_dct.has_key(lst[0]):
            all_date_splice_dct[lst[0]][lst[1]] = lst[2:]
        else:
            all_date_splice_dct[lst[0]] = {lst[1]:lst[2:]}

        lst2 = tlines[i].strip().split(',')
        if all_date_splice_gap_dct.has_key(lst2[0]):
            all_date_splice_gap_dct[lst2[0]][lst2[1]] = lst2[2:]
        else:
            all_date_splice_gap_dct[lst2[0]] = {lst2[1]:lst2[2:]}

def get_all_test_splice():
    with open('d:/ditech/result_3_inter', 'r') as file:
        lines = file.readlines()

    for i in range(len(lines)):
        lst = lines[i].strip().split(',')
#         pdb.set_trace()
        if not all_date_splice_test_dct.has_key(lst[0]):
            all_date_splice_test_dct[lst[0]] = {lst[2]:lst[3:]}
        else:
            all_date_splice_test_dct[lst[0]][lst[2]] = lst[3:]


def generate_hash_feature(hash_id, splice):
    try:
        features = []

        hash_dct = all_date_splice_dct[hash_id]
        hash_gap_dct = all_date_splice_gap_dct[hash_id]
        conn = utils.persist.connection()
        cur = conn.cursor()
        for key in hash_dct.keys():
            if key in skip_day:
                continue
            splice_lst = hash_dct[key]
            splice_gap_lst = hash_gap_dct[key]
            feature = copy.deepcopy(tem_one_hot) # add temp onehot
            weeklst = copy.deepcopy(week_hot) # add week day one hot
            weeklst[datetime.datetime.strptime(key, '%Y-%m-%d').weekday()] += 1

            sqltem = 'select * from weather where date = "%s" and splice = %d' % (key, splice)
            print sqltem
            cur.execute(sqltem)
            tem = cur.fetchall()
#             pdb.set_trace()
            feature[tem[-1][2]-1] += 1
            feature.append(tem[-1][3]);feature.append(tem[-1][4])
            feature = feature + weeklst
            #############################################
            sqltra = 'select * from traffic where district_hash = "%s" and date = "%s" and\
                                                  splice = %d' % (hash_id, key, splice)
            print sqltra
            cur.execute(sqltra)
            tra = cur.fetchall()
            tralst = copy.deepcopy(traffic_hot)
            if tra:
                total = int(tra[0][2].split(':')[1]) + int(tra[1][2].split(':')[1]) + int(tra[2][2].split(':')[1]) + int(tra[3][2].split(':')[1])
            else:
                total = 1
            for tr in tra:
                tralst[int(tr[2].split(':')[0]) - 1] += round(float(tr[2].split(':')[1])/total, 3)
            feature += tralst
            ##############################################
            # pdb.set_trace()
            for i in range(3):
                # feature.append(float(splice_lst[splice+i-4]))
                feature.append(float(splice_gap_lst[splice+i-4]))
                # feature.append(float(splice_gap_lst[splice+i-4]) - float(splice_gap_lst[splice+i-5]))
            feature.append(float(splice_gap_lst[splice-1]))

            features.append(feature)

        return features
        conn.close()
    except:
        traceback.print_exc()
        conn.close()
        

def generate_test_feature(hash_id, splice, date):
    try:
        features = []

        hash_dct = all_date_splice_test_dct[hash_id]

        conn = utils.persist.connection()
        cur = conn.cursor()
        key = date + '-' + str(splice)
        
#         pdb.set_trace()
        splice_lst = hash_dct[key]

        feature = copy.deepcopy(tem_one_hot) # add temp onehot
        weeklst = copy.deepcopy(week_hot) # add week day one hot
        weeklst[datetime.datetime.strptime(date, '%Y-%m-%d').weekday()] += 1

        sqltem = 'select * from weather_test where date = "%s" and splice < %d and splice > %d' % (date, splice+30, splice-30)
        print sqltem
        cur.execute(sqltem)
        tem = cur.fetchall()
            
#         pdb.set_trace()
        feature[tem[-1][2]-1] += 1
        feature.append(tem[-1][3]);feature.append(tem[-1][4])
        feature = feature + weeklst
        #######################################################
        sqltra = 'select * from traffic_test where district_hash = "%s" and date = "%s" and\
                                              splice = %d' % (hash_id, date, splice-1)
        print sqltra
        cur.execute(sqltra)
        tra = cur.fetchall()
        tralst = copy.deepcopy(traffic_hot)
        # pdb.set_trace()
        if tra:
            total = int(tra[0][2].split(':')[1]) + int(tra[1][2].split(':')[1]) + int(tra[2][2].split(':')[1]) + int(tra[3][2].split(':')[1])
        else:
            total = 1
        for tr in tra:
            tralst[int(tr[2].split(':')[0]) - 1] += round(float(tr[2].split(':')[1])/total, 3)
        feature += tralst
        #################################################
        splice_lst = splice_lst[::-1]
        # splice_lst = splice_lst[:2][::-1] + splice_lst[2:4][::-1] + splice_lst[4:][::-1]
        splice_lst = splice_lst[::2]
        # splice_lst
        feature = feature + map(lambda x:float(x), splice_lst)

        features.append(feature)

        # return features
        return feature
        conn.close()
    except:
        traceback.print_exc()
        conn.close()

if __name__ == '__main__':
    get_all_splice()
    get_all_test_splice()
    hash_id = '4725c39a5e5f4c188d382da3910b3f3f'
    splice = 94
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()

        sql = 'select * from cluster_map'
        cur.execute(sql)
        rst = cur.fetchall()
        district_hash_lst = [rs[0] for rs in rst]
        # features = generate_hash_feature(hash_id, splice)
        features = []
        for hash in district_hash_lst:
            feature = generate_test_feature(hash, splice, '2016-01-28')
            features.append(feature)
        feature_result = []
        for feature in features:
            print feature
            feature = map(lambda x:float(x), feature)
            feature_result.append(','.join(map(lambda x:str(x), feature)))

        with open('d:/ditech/feature_result', 'wb') as file:
            file.writelines('\n'.join(feature_result))
        conn.close()
    except:
        traceback.print_exc()
        conn.close()

end = time.time()
print end - start

