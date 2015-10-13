import copy
import os







studthr = open('d:/student/threestunr.txt', 'r+')
thrtrult = studthr.readlines()
perscorelst = []
for tru in thrtrult:
    perscorelst.append(int(tru[:-1]))
print perscorelst

studtrue = open('d:/student/tru.txt', 'r+')
trult = studtrue.readlines()
trulst = []
for tru in trult:
    trulst.append(int(tru[:-1]))
print trulst
num = 0
length = len(trulst)
for j in xrange(length):
    num += (trulst[j] - perscorelst[j]) * (trulst[j] - perscorelst[j])
print num
print 1- float((num*6 ))/(length*(length*length - 1))
studtrue.close()
studthr.close()