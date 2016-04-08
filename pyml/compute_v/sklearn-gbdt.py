import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib

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

train_feat=np.genfromtxt("d:/githubs/feimao/train.csv", delimiter=',', dtype=np.float32)
train_id=train_feat[:, train_feat.shape[1]-1]
train_feat = train_feat[:, 1:train_feat.shape[1]-1]
test_feat=np.genfromtxt("d:/githubs/feimao/test.csv", delimiter=',', dtype=np.float32)
# test_id=test_feat[:, test_feat.shape[1]-1]
test_id = np.genfromtxt('d:/githubs/feimao/result.csv', delimiter=',', dtype=np.float32)
test_id = test_id[:, 1:test_id.shape[1]]
test_feat = test_feat[:, 1:test_feat.shape[1]]
print train_feat.shape, train_id.shape, test_feat.shape, test_id.shape
gbdt.fit(train_feat, train_id)
joblib.dump(gbdt, 'model')
pred=gbdt.predict(test_feat)
total_err=0
num = 0.0
for i in range(pred.shape[0]):
    print pred[i], test_id[i]
    if pred[i] >= 0.5 and test_id[i] == 1.0:
        num += 1
    elif pred[i] < 0.5 and test_id[i] == 0.0:
        num += 1
    # err=(pred[i]-test_id[i])/test_id[i]
    # total_err+=err*err
# print total_err/pred.shape[0]
print num / pred.shape[0]

end = time.time()
print end - start