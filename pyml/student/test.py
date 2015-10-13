import copy
studtet = open('d:/student/test.arff', "r+")
scorelst = studtet.readlines()
perscorelst = []
import pdb
for lne in scorelst:
    scorelst = lne[:-1].split(',')
    score = 0.0118 * float(scorelst[0]) + 0.8857*float(scorelst[1]) + 27.6207
    print score
    perscorelst.append(score)

persortlst = copy.deepcopy(perscorelst)
persortlst.sort()
print perscorelst   
print persortlst

scoredct = {}
i = 1
for score in persortlst:
    scoredct[score] = i
    i += 1

for j in xrange(len(perscorelst)):
    perscorelst[j] = scoredct[perscorelst[j]]

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
studtet.close()