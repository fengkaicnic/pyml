import numpy as np
import pdb

from sklearn import linear_model

logistic = linear_model.LogisticRegression()
train_set = np.array([[1, 2, 3, 4, 5], [2, 3, 4, 5, 6], [3, 4, 5, 6, 7], [4, 5, 6, 7, 8], [5, 6, 7, 8, 9]])
train_set = np.vstack((train_set, train_set))
train_set = np.vstack((train_set, train_set))
train_set = np.vstack((train_set, train_set))
label_set = np.array([2, 4, 6, 8, 10])
label_set = np.hstack((label_set, label_set))
label_set = np.hstack((label_set, label_set))
label_set = np.hstack((label_set, label_set))
logistic.fit(train_set, label_set)

pred = logistic.predict([80, 30, 40, 50, 60])

print pred
