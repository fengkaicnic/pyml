from jobs import utils
import pdb
pdb.set_trace()

test_file = 'd:/jobs/dctree/size/test.csv'
labels = utils.get_labels(test_file, 2)
plabel = []
for j in range(10):
    plabel.append(utils.read_rst('result03' +str(j)+ '.txt'))
for j in range(10):
    plabel.append(utils.read_rst('result04' +str(j)+ '.txt'))
for j in range(10):
    plabel.append(utils.read_rst('result05' +str(j)+ '.txt'))
for j in range(6):
    plabel.append(utils.read_rst('result06' +str(j)+ '.txt'))
rst = [0 for j in xrange(36)]
i = 0
for label in labels:
    for j in range(36):
        if plabel[j][i] == label:
            rst[j] += 1
    i += 1
    
print rst