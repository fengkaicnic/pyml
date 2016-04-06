from sklearn.externals import joblib
import numpy as np

test_feat=np.genfromtxt("d:/naren/recommend/test_model_mail", delimiter=',', dtype=np.float32)

test_id=test_feat[:, test_feat.shape[1] - 3]
test_feat = test_feat[:, :test_feat.shape[1] - 3]

gbdt = joblib.load('../model')

pred=gbdt.predict(test_feat)

num = 0.0

for i in range(pred.shape[0]):
    print pred[i], test_id[i]
    if pred[i] >= 0.50 and test_id[i] == 1.0:
        num += 1
    elif pred[i] < 0.50 and test_id[i] == 0.0:
        num += 1


print num / pred.shape[0]
