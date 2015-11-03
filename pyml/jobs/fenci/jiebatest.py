#coding:utf8
import jieba
import sys
import pdb
reload(sys)
sys.setdefaultencoding('utf8')
pdb.set_trace()
seg_lst = jieba.cut(u'机电工程师')
for letter in seg_lst:
    print letter