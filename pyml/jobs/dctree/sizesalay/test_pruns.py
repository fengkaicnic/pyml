from jobs import utils
import pdb

test_file = 'd:/jobs/dctree/salary/test.csv'
labels = utils.get_labels(test_file, 6)
pdb.set_trace()
plabel1 = utils.read_rst('salaryresult.txt')
plabel2 = utils.read_rst('salaryresult1.txt')
i = 0
rst = 0
for label in plabel1:
    if plabel2[i] == label:
        rst += 1
    i += 1
    
print rst