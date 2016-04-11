from sklearn.externals import joblib
import numpy as np
from sklearn import metrics
import pdb

test_feat=np.genfromtxt("d:/naren/recommend/new-data", delimiter=',', dtype=np.float32)

test_id=test_feat[:, test_feat.shape[1] - 1]
test_feat = test_feat[:, :test_feat.shape[1] - 1]


gbdt = joblib.load('../model')

pred=gbdt.predict(test_feat)


num = 0.0

tf_num = 0
tt_num = 0
nf_num = 0
nt_num = 0


for i in range(pred.shape[0]):
    print pred[i], test_id[i]
    if pred[i] >= 0.55 and test_id[i] == 1.0:
        num += 1
        tt_num += 1
    elif pred[i] < 0.55 and test_id[i] == 0.0:
        num += 1
        nf_num += 1
    elif pred[i] >= 0.55 and test_id[i] == 0.0:
        tf_num += 1
    elif pred[i] < 0.55 and test_id[i] == 1.0:
        nt_num += 1

print num / pred.shape[0]
pred_id = map(lambda x:x>=0.55 and 1.0 or 0.0, pred)
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
pdb.set_trace()
#
print metrics.auc(fpr, tpr)
