import numpy as np
import xgboost as xgb

dataset = np.loadtxt('d:/jobs/xgboost/data.csv', delimiter=',')

sz = dataset.shape

train = dataset[:int(sz[0] * 0.7), :]
test = dataset[int(sz[0] * 0.7):, :]

train_X = train[:, 0:2]
label_X = train[:, 3]

test_Y = test[:, 0:2]
label_Y = test[:, 3]

xg_train = xgb.DMatrix( train_X, label=label_X)
xg_test = xgb.DMatrix(test_Y, label=label_Y)

param = {}
# use softmax multi-class classification
param['objective'] = 'multi:softmax'
# scale weight of positive examples
param['eta'] = 0.1
param['max_depth'] = 16
param['silent'] = 1
param['nthread'] = 4
param['num_class'] = 123

watchlist = [ (xg_train,'train'), (xg_test, 'test') ]

num_round = 15
bst = xgb.train(param, xg_train, num_round, watchlist );
# get prediction
pred = bst.predict( xg_test );

print ('predicting, classification error=%f' % (sum( int(pred[i]) != label_Y[i] for i in range(len(label_Y))) / float(len(label_Y)) ))

param['objective'] = 'multi:softprob'
bst = xgb.train(param, xg_train, num_round, watchlist );
# Note: this convention has been changed since xgboost-unity
# get prediction, this is in 1D array, need reshape to (ndata, nclass)
yprob = bst.predict( xg_test ).reshape(label_Y.shape[0], 32 )
ylabel = np.argmax(yprob, axis=1)

print ('predicting, classification error=%f' % (sum( int(ylabel[i]) != label_Y[i] for i in range(len(label_Y))) / float(len(label_Y)) ))
