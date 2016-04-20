import numpy as np
from sklearn import linear_model
clf = linear_model.LinearRegression()

N = 10
x = np.random.rand(N)
y = np.random.rand(N)
z = 0.2*x - 0.5*y + 1.2 + np.random.rand(N)*0.02

clf.fit(np.c_[x, y], z)
print clf.coef_, clf.intercept_