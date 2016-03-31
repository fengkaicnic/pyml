#coding:utf8
import sys
import os
reload(sys)
import pdb
import jieba

sys.setdefaultencoding('utf8')

stop_words = {}

with open('stopwords', 'r') as file:
    lines = file.readlines()
    lines = map(lambda x: x.decode('utf8'), lines)
    lines = map(lambda x: x.strip(), lines)
    for line in lines:
        stop_words[line] = 1

with open('input_text', 'r') as file:
    lines = file.readlines()

fln = []
for line in lines:
    seglst = jieba.cut(line.strip(), cut_all=False)
    words = filter(lambda x: not stop_words.has_key(x), seglst)
    # pdb.set_trace()
    fln.append(' '.join(words))

with open('input.text', 'wb') as file:
    file.writelines('\n'.join(fln).decode('utf8').encode('gbk'))