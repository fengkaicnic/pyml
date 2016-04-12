import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib

from sklearn import metrics

import time

start = time.time()
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
train_id=train_feat[:, train_feat.shape[1]-1]
train_feat = train_feat[:, :train_feat.shape[1]-1]
test_feat=np.genfromtxt("d:/naren/recommend/test-data", delimiter=',', dtype=np.float32)
test_id=test_feat[:, test_feat.shape[1]-1]
test_feat = test_feat[:, :test_feat.shape[1]-1]
print train_feat.shape, train_id.shape, test_feat.shape, test_id.shape
gbdt.fit(train_feat, train_id)
joblib.dump(gbdt, 'model')
pred=gbdt.predict(test_feat)
total_err=0
num = 0.0
tf_num = 0
tt_num = 0
nf_num = 0
nt_num = 0

for i in range(pred.shape[0]):
    print pred[i], test_id[i]
    if pred[i] >= 0.5 and test_id[i] == 1.0:
        num += 1
        tt_num += 1
    elif pred[i] < 0.5 and test_id[i] == 0.0:
        num += 1
        nf_num += 1
    elif pred[i] >= 0.5 and test_id[i] == 0.0:
        tf_num += 1
    elif pred[i] < 0.5 and test_id[i] == 1.0:
        nt_num += 1
    # err=(pred[i]-test_id[i])/test_id[i]
    # total_err+=err*err
# print total_err/pred.shape[0]
print num / pred.shape[0]

pred_id = map(lambda x:x>=0.5 and 1.0 or 0.0, pred)
print metrics.accuracy_score(test_id, pred_id)
print str(tf_num) + '   ' + str(tt_num)
print str(nf_num) + '   ' + str(nt_num)
print 'precision:'
print float(tt_num)/(tt_num + tf_num)
print metrics.precision_score(test_id, pred_id)
print 'recall:'
# print float(tt_num)/(tt_num + nt_num)

print metrics.recall_score(test_id, pred_id)
fpr, tpr, thresholds = metrics.roc_curve(test_id, pred)
# pdb.set_trace()
#
print metrics.auc(fpr, tpr)

end = time.time()
print end - start