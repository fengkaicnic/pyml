from jobs import utils
import pdb

test_file = 'd:/jobs/dctree/position/test.csv'
labels = utils.get_labels(test_file, 7)
plabel = []
# for j in range(10):
#     plabel.append(utils.read_rst('result03' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result04' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result05' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result06' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result07' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result04' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result08' +str(j)+ '.txt'))
# for j in range(6):
#     plabel.append(utils.read_rst('result3' +str(j + 4)+ '.txt'))
for j in range(10):
    plabel.append(utils.read_rst('result36' +str(j)+ '.txt'))
rst = [0 for j in xrange(10)]
i = 0
for label in labels:
    for j in range(10):
        if plabel[j][i] == label:
            rst[j] += 1
    i += 1
    
print rst