import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib
from collections import Counter
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

train_feat=np.genfromtxt("d:/naren/recommend/train-data", delimiter=',', dtype=np.float32)
test_feat=np.genfromtxt("d:/naren/recommend/test-data", delimiter=',', dtype=np.float32)
test_id=test_feat[:, test_feat.shape[1]-1]
test_feat = test_feat[:, :test_feat.shape[1]-1]

cnt = Counter(train_feat[:, -1])
p_num = cnt[1.0]
n_num = cnt[0.0]
train_p = train_feat[:p_num, :]
train_f = train_feat[p_num:, :]

pred_lst = []
pred = []

for i in range(50):
    train_set = get_sample(train_f, n_num, p_num)
    train_data = np.vstack((train_p, train_set))
    train_id=train_data[:, train_data.shape[1]-1]
    train_data = train_data[:, :train_data.shape[1]-1]
    gbdt.fit(train_data, train_id)
    joblib.dump(gbdt, 'models/model'+str(i))
    pred_lst.append(gbdt.predict(test_feat))

for i in range(test_id.shape[0]):
    lst = map(lambda tem:tem[i], pred_lst)
    lst = map(lambda x:x > 0.55 and 1 or 0, lst)
    if lst.count(1) >= lst.count(0):
        pred.append(1.0)
    else:
        pred.append(0.0)

tf_num, tt_num, nf_num, nt_num = 0, 0, 0, 0

for i in range(test_id.shape[0]):
    if pred[i] == 1.0 and test_id[i] == 1.0:
        tt_num += 1
    elif pred[i] == 0.0 and test_id[i] == 0.0:
        nf_num += 1
    elif pred[i] == 1.0 and test_id[i] == 0.0:
        tf_num += 1
    elif pred[i] == 0.0 and test_id[i] == 1.0:
        nt_num += 1

print str(tf_num) + '   ' + str(tt_num)
print str(nf_num) + '   ' + str(nt_num)

print 'accuracy:'
print metrics.accuracy_score(test_id, pred)
print 'precision:'
print metrics.precision_score(test_id, pred)
print 'recall:'
print metrics.recall_score(test_id, pred)

end = time.time()
print end - start