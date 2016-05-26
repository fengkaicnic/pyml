#generate features
#temperature, pm2.5, weekday, traffic, onehot

import utils
import traceback
import copy
import datetime

all_date_splice_dct = {}
all_date_splice_gap_dct = {}
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

            feature[tem[-1][1]-1] += 1
            feature.append(tem[-1][2]);feature.append(tem[-1][3])
            feature = feature + weeklst
            sqltra = 'select * from traffic where district_hash = "%s" and date = "%s" and\
                                                  splice = %d' % (hash_id, key, splice)
            print sqltra
            cur.execute(sqltra)
            tra = cur.fetchall()
            tralst = copy.deepcopy(traffic_hot)
            for tr in tra:
                tralst[int(tr[1].split(':')[0]) - 1] += int(tr[1].split(':')[1])
            feature += tralst
            for i in range(3):
                feature.append(splice_lst[splice+i-4])
                feature.append(splice_gap_lst[splice+i-4])
            feature.append(splice_lst[-1])

            features.append(','.join(map(lambda x:str(x), feature)))

        return features
        conn.close()
    except:
        traceback.print_exc()
        conn.close()


if __name__ == '__main__':
    get_all_splice()
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()

        sql = 'select * from cluster_map'
        cur.execute(sql)
        rst = cur.fetchall()
        district_hash_lst = [rs[0] for rs in rst]
        features = generate_hash_feature(district_hash_lst[0], 118)

        for feature in features:
            print feature
        conn.close()
    except:
        traceback.print_exc()
        conn.close()
