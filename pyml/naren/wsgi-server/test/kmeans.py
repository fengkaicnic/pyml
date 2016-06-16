#coding:utf8
import utils
import sys
import traceback
reload(sys)
import jieba
import numpy as np
import random
import pdb
sys.setdefaultencoding('utf8')
import pickle

stopwords = {}
with open('d:/naren/stopwords.txt', 'r') as file:
    tlines = file.readlines()
    for line in tlines:
        stopwords[line.lower().strip().decode('gbk')] = 1

with open('d:/naren/latesttitle.txt', 'r') as file:
    lines = file.readlines()

wordlst = []
for line in lines:
    lst = line.lower().strip().split(' ')
    if int(lst[-1]) < 10:
        continue
    if stopwords.has_key(lst[0].decode('gbk')):
        continue
    wordlst.append(lst[0])

worddct = {}
for index, word in enumerate(wordlst):
    worddct[word.decode('gbk')] = index
    # worddct[word.decode('gbk')] = 10
try:
    conn = utils.persist.connection()
    sql = 'select latesttitle from profile'
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    titleall = []
    # pdb.set_trace()
    for rs in rst:
        titlelst = [10 for i in range(len(worddct))]
        # pdb.set_trace()
        if not rs[0]:
            continue
        seglst = jieba.cut(rs[0].lower(), cut_all=False)
        for seg in seglst:
            if not worddct.has_key(seg):
                continue
            titlelst[worddct[seg]] -= 2
        titlelst.append(rs[0])
        titleall.append(titlelst)
    # pdb.set_trace()
    nums = 35
    numlst = []
    for i in range(nums):
        # lst = [0 for i in range(len(worddct))]
        # lst[random.randint(0, len(worddct))] = 5
        lst = titleall[random.randint(0, len(titleall))][:-1]
        # pdb.set_trace()
        lst[random.randint(0, len(lst))] += 1
        numlst.append(lst)
    total_distance = 99999999

    result_class = {}

    while 1:

        result_dct = {}
        for i in range(len(numlst)):
            result_dct[i] = []
        # pdb.set_trace()
        for title in titleall:
            results = []
            for index, numt in enumerate(numlst):
                title1 = np.array(title[:-1])
                numt = np.array(numt)
                results.append((index, np.sum((title1 - numt) ** 2)))
            results = sorted(results, key=lambda x:x[1])
            result_dct[results[0][0]].append(title)
        # pdb.set_trace()
        distance = 0
        newnumlst = []
        for key in result_dct.keys():
            nums = np.array([0.0 for i in range(len(worddct))])
            # pdb.set_trace()
            for lst in result_dct[key]:
                lst = np.array(lst[:-1])
                nums = nums + lst
                num = np.array(numlst[key])
                distance += np.sum((lst - num) ** 2)
            # pdb.set_trace()
            newnumlst.append(nums/len(result_dct[key]))
        # pdb.set_trace()

        if total_distance - distance < 100:
            break
        total_distance = distance
        print total_distance
        numlst = newnumlst
        result_class = result_dct
    pdb.set_trace()

    # file = open('result_class', 'wb')
    # pickle.dump(result_class, file)

    for key in result_class.keys():
        titles = []
        print len(result_class[key])
        for result in result_class[key]:
            try:
                titles.append(result[-1].decode('utf8').encode('gbk'))
            except:
                traceback.print_exc()
        with open('d:/naren/result'+str(key), 'wb') as file:
            file.writelines('\n'.join(titles))

    conn.close()
except:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
