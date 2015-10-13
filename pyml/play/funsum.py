
class FunSum(object):
    n = 0
    sum = 0
    
    def __init__(self):
        FunSum.n += 1
        FunSum.sum += FunSum.n
        
    def getsum(self):
        return FunSum.sum    
    
    def reset(self):
        FunSum.n = 0
        FunSum.sum = 0
    
ns = 102

templst = [FunSum() for i in xrange(ns) ]
print len(templst)
print FunSum.sum
