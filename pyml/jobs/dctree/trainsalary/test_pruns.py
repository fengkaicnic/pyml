from jobs import utils
import pdb
# pdb.set_trace()

test_file = 'd:/jobs/dctree/salary/test.csv'
labels = utils.get_labels(test_file, 5)
plabel = utils.read_rst('salary')
i = 0
rst = 0
for label in labels:
    if plabel[i] == label:
        rst += 1
    i += 1
    
print rst