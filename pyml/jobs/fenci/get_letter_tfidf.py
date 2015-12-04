#coding:utf8

from jobs import utils
import jieba
import jieba.posseg as pseg
import os
import pdb
import sys
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
reload(sys)
sys.setdefaultencoding('utf8')

letter_dct = utils.read_rst('letterdct')

# pdb.set_trace()
corpus = []
keys = []
for item in letter_dct.items():
    keys.append(item[0])
    corpus.append(' '.join(item[1][0]))
# corpus = [[' '.join(item[1][0])] for item in letter_dct.items()]

vectorizer=CountVectorizer()#该类会将文本中的词语转换为词频矩阵，矩阵元素a[i][j] 表示j词在i类文本下的词频
transformer=TfidfTransformer()#该类会统计每个词语的tf-idf权值
tfidf=transformer.fit_transform(vectorizer.fit_transform(corpus))#第一个fit_transform是计算tf-idf，第二个fit_transform是将文本转为词频矩阵
word=vectorizer.get_feature_names()#获取词袋模型中的所有词语
weight=tfidf.toarray()#将tf-idf矩阵抽取出来，元素a[i][j]表示j词在i类文本中的tf-idf权重

for i in range(len(weight)):#打印每类文本的tf-idf词语权重，第一个for遍历所有文本，第二个for便利某一类文本下的词语权重
    print u"-------这里输出第              ",keys[i],u"    类文本的词语tf-idf权重------"
    for j in range(len(word)):
      if weight[i][j] == 0.0:
          continue
      print word[j],weight[i][j]
      
print len(corpus)
print len(keys)
