#coding:utf8
import utils
import sys
import traceback
reload(sys)
import jieba
import numpy as np
import random
import pdb

with open('d:/naren/latesttitle.txt', 'r') as file:
    lines = file.readlines()

wordlst = []
for line in lines:
    lst = line.strip().split(' ')
    if int(lst[-1]) < 10:
        continue
    wordlst.append(lst[0])

worddct = {}
for index, word in enumerate(wordlst):
    worddct[word] = index

try:
    conn = utils.persist.connection()
    sql = 'select latesttitle from profile'
    cur = conn.cursor()
    cur.execute(sql)
    rst = cur.fetchall()
    titleall = []
    for rs in rst:
        titlelst = [0 for i in range(len(worddct))]
        seglst = jieba.cut(rs[0], cut_all=False)
        for seg in seglst:
            if not worddct.has_key(seg):
                continue
            titlelst[worddct[seg]] += 1
        titleall.append(titlelst)

    nums = 10
    numlst = []
    for i in range(nums):
        lst = [0 for i in range(len(worddct))]
        lst[random.randint(0, len(worddct))] = 5
        numlst.append(lst)
    total_distance = 99999999

    result_class = {}

    while 1:

        result_dct = {}
        for i in range(len(numlst)):
            result_dct[i] = []
        for title in titleall:
            results = []
            for index, numt in enumerate(numlst):
                title = np.array(title)
                numt = np.array(numt)
                results.append((index, np.sum((title - numt) ** 2)))
                results = sorted(results, key=lambda x:x[1])
                result_dct[results[0][0]].append(results[0][1])
        pdb.set_trace()
        distance = 0
        newnumlst = []
        for key in result_dct.keys():
            nums = np.array([0.0 for i in range(len(worddct))])
            pdb.set_trace()
            for lst in result_dct[key]:
                lst = np.array(lst)
                nums = nums + lst
                num = np.array(numlst[key])
                distance += np.sum((lst - num) ** 2)
            newnumlst.append(nums/len(result_dct[key]))
        pdb.set_trace()

        if distance - total_distance < 100:
            break
        total_distance = distance
        print total_distance
        numlst = newnumlst
        result_class = result_dct

    for key in result_class.keys():
        print len(result_class[key])

    conn.close()
except:
    traceback.print_exc()
    pdb.set_trace()
    conn.close()
