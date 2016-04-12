from sklearn.externals import joblib
import numpy as np
from sklearn import metrics
import pdb

import time

start = time.time()

test_feat=np.genfromtxt("d:/naren/recommend/new-data", delimiter=',', dtype=np.float32)

pos_id = test_feat[:, test_feat.shape[1] - 2]
resume_id = test_feat[:, test_feat.shape[1] - 1]
test_id=test_feat[:, test_feat.shape[1] - 3]
test_feat = test_feat[:, :test_feat.shape[1] - 3]

pred_lst = []
pred = []

for i in range(50):
    gbdt = joblib.load('../models/model' + str(i))
    pred_m=gbdt.predict(test_feat)
    pred_lst.append(pred_m)

for i in range(test_id.shape[0]):
    lst = map(lambda tem:tem[i], pred_lst)
    lst = map(lambda x:x > 0.5 and 1 or 0, lst)
    if lst.count(1) >= lst.count(0):
        pred.append(1.0)
    else:
        pred.append(0.0)

num = 0.0

tf_num = 0
tt_num = 0
nf_num = 0
nt_num = 0


for i in range(test_id.shape[0]):
    if pred[i] == 1.0 and test_id[i] == 1.0:
        tt_num += 1
    elif pred[i] == 0.0 and test_id[i] == 0.0:
        nf_num += 1
    elif pred[i] == 1.0 and test_id[i] == 0.0:
        tf_num += 1
    elif pred[i] == 0.0 and test_id[i] == 1.0:
        nt_num += 1

# pred_id = map(lambda x:x>=0.35 and 1.0 or 0.0, pred)
print metrics.accuracy_score(test_id, pred)
print str(tf_num) + '   ' + str(tt_num)
print str(nf_num) + '   ' + str(nt_num)
print 'precision:'
print float(tt_num)/(tt_num + tf_num)
print metrics.precision_score(test_id, pred)
print 'recall:'
# print float(tt_num)/(tt_num + nt_num)

print metrics.recall_score(test_id, pred)
# fpr, tpr, thresholds = metrics.roc_curve(test_id, pred)
# # pdb.set_trace()
# #
# print metrics.auc(fpr, tpr)

end = time.time()

print (end - start)