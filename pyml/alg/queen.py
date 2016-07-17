# coding:utf8
import pdb

class EightQueen:
    # define const  queen number
    queenNum = 8
    def __init__(self):
        self.qiPan = []
        self.num = 0
        # init a n*n  list[][] as qi pan
        for i in range(self.queenNum):
            rows = []
            for j in range(self.queenNum):
                xy = [i, j]
                rows.append(xy)
            self.qiPan.append(rows)

    # param rowNum
    def getNext(self, e8, rowNum):
         if len(e8) == self.queenNum:
            self.num += 1
            print "method " + str(self.num) + "is:" + str(e8)
            return
         if rowNum > len(self.qiPan):
             return
         for d in self.qiPan[rowNum]:
             if self.matchAllE8(e8, d):
                 e8copy = e8[:]
                 e8copy.append(d)
                 self.getNext(e8copy, rowNum + 1)

    def calcNum(self):
        pdb.set_trace()
        for i in self.qiPan[0]:

            self.getNext([i], 1)
        print "all method is:" + str(self.num)

    def matchAllE8(self, e8, left0):
        for i in e8:
            if not self.isMatch(i, left0):
                return False
        return True

    def isMatch(self, f, g):
        return (f[0] + f[1] != g[0] + g[1]) and\
               (f[0] - f[1] != g[0] - g[1])  and\
               (f[0] != g[0]) and (f[1] != g[1])

e = EightQueen()

e.calcNum()
