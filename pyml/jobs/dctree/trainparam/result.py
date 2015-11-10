from jobs import utils
import pdb
pdb.set_trace()

test_file = 'd:/jobs/dctree/degree/testparam.csv'
labels = utils.get_labels(test_file, 0)
plabel = []
for j in range(10):
    plabel.append(utils.read_rst('result02' +str(j)+ '.txt'))
plabel.append(utils.read_rst('result030.txt'))
rst = [0 for j in xrange(11)]
i = 0
for label in labels:
    for j in range(11):
        if plabel[j][i] == label:
            rst[j] += 1
    i += 1
    
print rst