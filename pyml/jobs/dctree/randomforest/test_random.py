#coding:utf8
import sys
from jobs import utils
reload(sys)
import pdb
sys.setdefaultencoding('utf8')

test_file = 'd:/jobs/dctree/random/test.csv'
labels = utils.get_labels(test_file, 9)
# pdb.set_trace()
plabel1 = utils.read_rst('result.txt')
plabel2 = utils.read_rst('finalrut')
i = 0
rst = 0
for label in labels:
    if plabel2[i] == label:
        rst += 1
    i += 1
    
print rst