import utils
import traceback
import pickle
import jieba
import copy
import pdb
import time
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description, type from company where type != "None"'
    cur.execute(sql)
    rst = cur.fetchall()

    topic_word = open('topic_word', 'r')
    topic_words = pickle.load(topic_word)
    topicsx = []
    topicsy = []

    type_dct = {}
    type_dct_r = {}
    num = 0
    for rs in rst:
        if not type_dct.has_key(rs[1].lower()):
            type_dct[rs[1].lower()] = num
            type_dct_r[num] = rs[1].lower()
            num += 1

    for rs in rst:
        desc = rs[0]
        segs = jieba.cut(utils.discrement_unicode(desc), cut_all=False)
        tpwords = copy.deepcopy(topic_words)
        for seg in segs:
            if tpwords.has_key(seg.lower()):
                tpwords[seg.lower()] += 1

        tpwordl = []
        topicsy.append(type_dct[rs[1].lower()])
        for key in sorted(tpwords.keys()):
            tpwordl.append(tpwords[key])

        topicsx.append(tpwordl)

    pdb.set_trace()

    x = np.array(topicsx)
    y = np.array(topicsy)

    clf = LinearDiscriminantAnalysis()

    clf.fit(x, y)

    sqll = 'select description, position_name, id from company where type = "None"'

    cur.execute(sqll)
    rst = cur.fetchall()

    for rs in rst:
        desc = rs[0]
        segs = jieba.cut(utils.discrement_unicode(desc), cut_all=False)
        tpwords = copy.deepcopy(topic_words)
        for seg in segs:
            if tpwords.has_key(seg.lower()):
                tpwords[seg.lower()] += 1

        tpwordl = []
        for key in sorted(tpwords.keys()):
            tpwordl.append(tpwords[key])
        # pdb.set_trace()
        print type_dct_r[clf.predict(tpwordl)[0]], utils.discrement_unicode(rs[1]), rs[2]

except:
    traceback.print_exc()

end = time.time()

print end - start
