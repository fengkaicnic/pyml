from jobs import utils
import pdb
pdb.set_trace()

test_file = 'd:/jobs/dctree/salary/test.csv'
labels = utils.get_labels(test_file, 6)
plabel = []
# for j in range(10):
#     plabel.append(utils.read_rst('result03' +str(j)+ '.txt'))
# for j in range(10):
#     plabel.append(utils.read_rst('result04' +str(j)+ '.txt'))
for j in range(10):
    plabel.append(utils.read_rst('result08' +str(j)+ '.txt'))
for j in range(10):
    plabel.append(utils.read_rst('result09' +str(j)+ '.txt'))
rst = [0 for j in xrange(20)]
i = 0
for label in labels:
    for j in range(20):
        if plabel[j][i] == label:
            rst[j] += 1
    i += 1
    
print rst