import numpy

class Perception(object):
    def __init__(self, eta=0.01, epochs=50):
        self.eta = eta
        self.epochs = epochs
        
    def train(self, x, y):
        self.wi = numpy.zeros(1 + x.shape[1])
        self.errors = []
        for _ in xrange(self.epochs):
            errors = 0
            for xi, target in zip(x, y):
                update = self.eta * (target - self.predict(xi))
                self.wi[1:] +=  update * xi
                self.wi[0] +=  update
                errors += int(update != 0.0)
            self.errors_.append(errors)
        return self
 
    def net_input(self, X):
        return numpy.dot(X, self.w_[1:]) + self.w_[0]
 
    def predict(self, X):
        return numpy.where(self.net_input(X) >= 0.0, 1, -1)

