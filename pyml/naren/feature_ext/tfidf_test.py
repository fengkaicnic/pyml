#coding:utf8

import jieba
import jieba.posseg as pseg
import os
from sklearn import feature_extraction
from sklearn.feature_extraction.text import TfidfTransformer
import utils
from sklearn.feature_extraction.text import CountVectorizer
import string
import traceback
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )
from numpy import *


data = []
try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description from mail_work limit 300'
    cur.execute(sql)
    rst = cur.fetchall()

    for term in rst:
        content = term[0]
        data.append(" ".join(jieba.cut(content, cut_all=False)))

except:
    traceback.print_exc()


#将得到的词语转换为词频矩阵
freWord = CountVectorizer()
#统计每个词语的tf-idf权值
transformer = TfidfTransformer()
#计算出tf-idf(第一个fit_transform),并将其转换为tf-idf矩阵(第二个fit_transformer)
tfidf = transformer.fit_transform(freWord.fit_transform(data))
#获取词袋模型中的所有词语
word = freWord.get_feature_names()
#得到权重
weight = tfidf.toarray()
tfidfDict = {}
for i in range(len(weight)):
  for j in range(len(word)):
    getWord = word[j]
    getValue = weight[i][j]
    if getValue != 0:
      if tfidfDict.has_key(getWord):
        tfidfDict[getWord] += string.atof(getValue)
      else:
        tfidfDict.update({getWord:getValue})
sorted_tfidf = sorted(tfidfDict.iteritems(),
            key = lambda d:d[1],reverse = True)
fw = open('result.txt','w')
for i in sorted_tfidf:
  fw.write(i[0] + '\t' + str(i[1]) +'\n')