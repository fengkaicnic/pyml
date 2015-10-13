import pandas as pd
from perception import Perception
df = pd.read_csv('https://archive.ics.uci.edu/ml/machine-learning-databases/iris/iris.data', header=None)
 
# setosa and versicolor
y = df.iloc[0:100, 4].values
y = np.where(y == 'Iris-setosa', -1, 1)
 
# sepal length and petal length
X = df.iloc[0:100, [0,2]].values
 
import matplotlib.pyplot as plt
from mlxtend.evaluate import plot_decision_regions
 
ppn = Perceptron(epochs=10, eta=0.1)
 
ppn.train(X, y)
print('Weights: %s' % ppn.w_)
plot_decision_regions(X, y, clf=ppn)
plt.title('Perceptron')
plt.xlabel('sepal length [cm]')
plt.ylabel('petal length [cm]')
plt.show()
 
plt.plot(range(1, len(ppn.errors_)+1), ppn.errors_, marker='o')
plt.xlabel('Iterations')
plt.ylabel('Missclassifications')
plt.show()
 
Weights: [-0.4  -0.68  1.82]