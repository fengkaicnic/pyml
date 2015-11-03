#coding:utf8
import jieba
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf8')
pdb.set_trace()
seg_lst = jieba.cut(u'品质工程师（QE）')
for letter in seg_lst:
    print letter