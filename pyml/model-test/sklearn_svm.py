from sklearn import svm
import numpy as np

import pdb

C = 1.0

rbf_svm = svm.SVC(kernel='rbf', gamma=0.7, C=C)

train_set = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [5, 6, 7, 8, 9]])
train_set = np.vstack((train_set, train_set))
train_set = np.vstack((train_set, train_set))
train_set = np.vstack((train_set, train_set))
label_set = np.array([2, 4, 6, 8, 10]) 
label_set = np.hstack((label_set, label_set))
label_set = np.hstack((label_set, label_set))
label_set = np.hstack((label_set, label_set))

pdb.set_trace()

rbf_svm.fit(train_set, label_set)

pred = rbf_svm.predict([2, 3, 5, 6, 7])

print pred
