
from sklearn.ensemble import GradientBoostingRegressor
from sklearn import cross_validation
import numpy as np
from sklearn import svm 
import traceback
import pdb
import generate_features
import utils
import time

start = time.time()

def gbdt_model(trains):

    trains = np.array(trains)

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

#     pdb.set_trace()
    train_set = trains[:, :-1]
    label_set = trains[:, -1]

    gbdt.fit(train_set, label_set)
    return gbdt

if __name__ == '__main__':
    with open('d:/ditech/citydata/read_me_1.txt', 'r') as file:
        lines = file.readlines()
    generate_features.get_all_splice()
    generate_features.get_all_test_splice()
    date_splice = {}
    for line in lines:
        line = line.strip()
#         pdb.set_trace()
        if not date_splice.has_key(int(line.split('-')[-1])):
            date_splice[int(line.split('-')[-1])] = ['-'.join(line.split('-')[:-1])]
        else:
            date_splice[int(line.split('-')[-1])].append('-'.join(line.split('-')[:-1]))
    results = []
    try:
        conn = utils.persist.connection()
        cur = conn.cursor()
        sql = 'select * from cluster_map'
        cur.execute(sql)
        rst = cur.fetchall()
        hash_dct = {}
        for rs in rst:
            hash_dct[rs[0]] = rs[1]
        
        for hash_id in hash_dct.keys():
            for splice in date_splice.keys():
                features = generate_features.generate_hash_feature(hash_id, splice)
                gbdt = gbdt_model(features)
                for date in date_splice[splice]:
                    test_features = generate_features.generate_test_feature(hash_id, splice, date)
                    pred = gbdt.predict(test_features)
                    if pred[0] < 1:
                        num = 1
                    else:
                        num = round(pred[0])
                    results.append(','.join([str(hash_dct[hash_id]), date+'-'+str(splice), str(num)]))
                    
        with open('d:/ditech/gbdt_model_result.csv', 'wb') as file:
            file.writelines('\n'.join(results))
        conn.close()
    except:
        traceback.print_exc()
        conn.close()
    
end = time.time()
print end - start
