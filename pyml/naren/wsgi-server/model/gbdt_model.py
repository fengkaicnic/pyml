import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from collections import Counter
from sklearn.externals import joblib
import generate_feature
import random

from sklearn import metrics

import time

start = time.time()

def get_sample(train_data, num1, num2):
    train_lst = []
    for i in xrange(train_data.shape[0]):
        if random.randint(1, num1) <= num2:
            train_lst.append(train_data[i, :])
        # if train_data[i,:][-1] == 1.0:
        #     train_lst.append(train_data[i, :])
        # else:
        #     if random.randint(num1) <= num2:
        #         train_lst.append(train_data[i, :])

    return np.array(train_lst)


def train_model(path=None):

    data_path = 'data/traindata'
    if path:
        data_path = path
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

    train_feat=np.genfromtxt(data_path, delimiter=',', dtype=np.float32)
    train_id=train_feat[:, train_feat.shape[1]-1]
    cnt = Counter(train_feat[:, -1])
    p_num = cnt[1.0]
    n_num = cnt[0.0]
    train_p = train_feat[:p_num, :]
    train_f = train_feat[p_num:, :]
    # train_feat = train_feat[:, :train_feat.shape[1]-1]
    for i in range(50):
        train_set = get_sample(train_f, n_num, p_num)
        train_data = np.vstack((train_p, train_set))
        train_id=train_data[:, train_data.shape[1]-1]
        train_data = train_data[:, :train_data.shape[1]-1]
        gbdt.fit(train_data, train_id)
        joblib.dump(gbdt, 'gbdt-model'+str(i))

    # gbdt.fit(train_feat, train_id)
    # joblib.dump(gbdt, 'gbdt-model')


def predict_data(pos_id, resume_id):
    # pdb.set_trace()
    test_feat = generate_feature.generate_test(pos_id, resume_id)
    pred_lst = []

    for i in range(50):
        gbdt = joblib.load('gbdt-model' + str(i))
        pred=gbdt.predict(test_feat)
        pred_lst.append(pred)
    lst = map(lambda tem:tem[0], pred_lst)
    lst = map(lambda x:x > 0.55 and 1 or 0, lst)
    if lst.count(1) >= lst.count(0):
        return float(lst.count(1))/len(lst)
    else:
        return float(lst.count(0))/len(lst)


if __name__ == '__main__':

    train_model()
    score = predict_data(1049420, '20625150')
    print score

end = time.time()
# print end - start
