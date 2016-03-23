#coding:utf8
import sys
import pandas as pd
import numpy as np
import jieba
import operator
reload(sys)
from sklearn import metrics
from sklearn.feature_extraction.text import HashingVectorizer
import random
from sklearn.naive_bayes import MultinomialNB
import time
sys.setdefaultencoding('utf-8')
wordct = {}
wordpct = {}
def get_feature_word():
    with open('d:/naren/ter1.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.decode('gbk').split('|')[0]
            seglst = jieba.cut(line, cut_all=False)
            for seg in seglst:
                if wordct.has_key(seg):
                    wordct[seg] += 1
                else:
                    wordct[seg] = 1

    # words = sorted(wordct.iteritems(), key=operator.itemgetter(1), reverse=True)
    # for word in words:
    #     print word[0],':',word[1]

    print '=================分割线==================='
    with open('d:/naren/spam1.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            line = line.decode('gbk').split('|')[0]
            seglst = jieba.cut(line, cut_all=False)
            for seg in seglst:
                if wordct.has_key(seg):
                    wordct[seg] += 1
                else:
                    wordct[seg] = 1

    wordsp = sorted(wordct.iteritems(), key=operator.itemgetter(1), reverse=True)
    for word in wordsp:
        print word[0],':',word[1]
    # print len(words)
    print len(wordsp)


def generate_train_test():
    trainlines = []
    testlines = []
    with open('d:/naren/spam1.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if random.randint(1, 3) == 1:
                testlines.append(line.strip().split('|')[0] + ',0')
                trainlines.append(line.strip().split('|')[0] + ',0')
            else:
                trainlines.append(line.strip().split('|')[0] + ',0')

    with open('d:/naren/ter1.csv', 'r') as file:
        lines = file.readlines()
        for line in lines:
            if random.randint(1, 3) == 1:
                testlines.append(line.strip().split('|')[0] + ',1')
                trainlines.append(line.strip().split('|')[0] + ',1')
            else:
                trainlines.append(line.strip().split('|')[0] + ',1')

    with open('d:/naren/train.csv', 'wb') as file:
        file.writelines('\n'.join(trainlines))

    with open('d:/naren/test.csv', 'wb') as file:
        file.writelines('\n'.join(testlines))


if __name__ == '__main__':
    # get_feature_word()
    generate_train_test()