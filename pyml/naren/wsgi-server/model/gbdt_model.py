import pdb
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.externals import joblib
import generate_feature

from sklearn import metrics

import time

start = time.time()

def train_model():

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

    train_feat=np.genfromtxt("d:/naren/wsgi-server/data", delimiter=',', dtype=np.float32)
    train_id=train_feat[:, train_feat.shape[1]-1]
    train_feat = train_feat[:, :train_feat.shape[1]-1]
    gbdt.fit(train_feat, train_id)
    joblib.dump(gbdt, 'gbdt-model')


def predict_data(pos_id, resume_id):

    test_feat = generate_feature.generate_test(pos_id, resume_id)
    gbdt = joblib.load('gbdt-model')
    pred=gbdt.predict(test_feat)
    return pred[0]


if __name__ == '__main__':

    train_model()
    score = predict_data(1049420, 20625150)
    print score

end = time.time()
# print end - start