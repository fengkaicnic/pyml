import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib

from sklearn import metrics

import time

def predict_data(store_code):

    train_path = 'd:/tianchi/model/train_store_%s.csv' % str(store_code)
    test_path = 'd:/tianchi/model/test_store_%s.csv' % str(store_code)
    
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
    
    train_feat=np.genfromtxt(train_path, delimiter=',', dtype=np.float32)
    train_item_ids = train_feat[:, train_feat.shape[1]-1]
    train_id=train_feat[:, train_feat.shape[1]-2]
    train_feat = train_feat[:, :train_feat.shape[1]-2]
    test_feat=np.genfromtxt(test_path, delimiter=',', dtype=np.float32)
    test_item_ids = test_feat[:, test_feat.shape[1]-1]
    test_feat = test_feat[:, :test_feat.shape[1]-1]
    
    gbdt.fit(train_feat, train_id)
    # joblib.dump(gbdt, 'model')
    pred=gbdt.predict(test_feat)
    result_lst = []
    for index, pred_data in enumerate(pred):
        lst = []
        lst.append(int(test_item_ids[index]))
        lst.append(store_code)
        lst.append(int(round(pred_data)))
        result_lst.append(','.join(map(lambda x: str(x), lst)))
    
    return result_lst
