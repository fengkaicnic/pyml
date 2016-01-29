from sklearn.preprocessing import OneHotEncoder
import xgboost
import numpy as np
import pandas as pd
import csv
import pdb

# train_x = np.loadtxt('d:/credit/train_x5.csv', delimiter=',')
# test_x = np.loadtxt('d:/credit/test_x5.csv', delimiter=',')
# train_label = np.loadtxt('d:/credit/train_y.csv', delimiter=',')
# train_type = np.loadtxt('d:/credit/features_type.csv', dtype={'names':('feature', 'type'), 'formats':('S15', 'S15')}, delimiter=',')
train_x = pd.read_csv('d:/credit/train_x.csv')
test_x = pd.read_csv('d:/credit/test_x.csv')
train_label = pd.read_csv('d:/credit/train_y.csv')
train_type = pd.read_csv('d:/credit/features_type.csv')

typelst = []
train_type.groupby(train_type['type'])
for name, group in train_type:
    print name
    typelst.append(group)
    
# for traintype in train_type[1:,]:
#     name = traintype[0].replace('"', '')
#     type = traintype[1].replace('"', '')
#     typelst.append(type)

pdb.set_trace()
# train_temp_num = np.zeros((train_x.shape[0], typelst.count('numeric')))
# test_temp_num = np.zeros((test_x.shape[0], typelst.count('numeric')))
# train_cat = np.zeros((train_x.shape[0], typelst.count('category')), dtype=int)
# test_cat = np.zeros((test_x.shape[0], typelst.count('category')), dtype=int)
train_temp_num = pd.DataFrame(np.zeros(train_x.shape[0], len(typelst[1])))
test_temp_num = pd.DataFrame(np.zeros(test_x.shape[0], len(typelst[1])))
train_cat = pd.DataFrame(np.zeros(train_x.shape[0], len(typelst[0])))
test_cat = pd.DataFrame(np.zeros(test_x.shape[0], len(typelst[0])))
numindex = 0
catindex = 0
mn = 0
for index, type in enumerate(typelst):
    if type == 'numeric':
        train_temp_num[:,numindex] = train_x[:,index+1]
        test_temp_num[:,numindex] = test_x[:,index+1]
        numindex += 1
    else:
        if train_x[:,index].min() < mn:
            mn = train_x[:,index].min()
        train_cat[:,catindex] = train_x[:,index+1] + 2
        test_cat[:,catindex] = test_x[:,index+1] + 2
        catindex += 1

enc = OneHotEncoder()

enc.fit(train_cat)
train_temp_cat = np.zeros((train_x.shape[0], enc.transform(train_cat[0]).toarray().shape[1]))
test_temp_cat = np.zeros((test_x.shape[0], enc.transform(train_cat[0]).toarray().shape[1]))

for index in range(train_cat.shape[0]):
    train_temp_cat[index] = enc.transform(train_cat[index]).toarray()

for index in range(test_cat.shape[0]):
    test_temp_cat[index] = enc.transform(test_cat[index]).toarray()

train_new = np.column_stack((train_temp_num, train_temp_cat))
test_new = np.column_stack((test_temp_num, test_temp_cat))

print train_new.shape
print test_new.shape

pdb.set_trace()
dtrain = xgboost.DMatrix(data=train_new, label=1-train_label[:,1])
dtest = xgboost.DMatrix(data=test_new)

param = {'bst:max_depth':8, 'bst:eta':0.02, 'objective':'binary:logistic'}
param['nthread'] = 2
param['eval_metric'] = 'auc'
param['scale_pos_weight'] = 8.7
param['gamma'] = 0
param['lambda'] = 700
param['subsample'] = 0.7
param['colsample_bytree'] = 0.3
param['min_child_weight'] = 5
param['booster'] = 'gbtree'
plst = param.items()

nround = 1520
bst = xgboost.train(plst, dtrain, nround)

pred = 1 - bst.predict(dtest)

result = np.zeros((test_x.shape[0], 2))
result[:,0] = test_x[:,0]
result[:,1] = pred

resultfle = file('d:/credit/result.csv', 'wb')
writer = csv.writer(resultfle)
writer.writerows(result)

resultfle.close()
