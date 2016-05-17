#coding:utf8
import utils
import traceback
import sys
import pdb
reload(sys)
import pickle
import jieba

try:
    stopword = {}
    keyword = [u'岗位职责', u'职位要求', u'工作职责', u'任职资格', u'岗位需求', u'岗位要求', u'岗位描述', u'职位描述', u'任职要求', u'任职需求']
    keyword1 = [u'福利介绍', u'我们能为你提供']
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description , type from company where type != "None" '
    cur.execute(sql)
    rst = cur.fetchall()
    pdb.set_trace()
    for rs in rst:
        descr = rs[0]
        delst = descr.split('\n')

        for num, delrt in enumerate(delst):
            if u'\uff1a' in delrt and delrt[:delrt.index(u'\uff1a')] in keyword1:
                # pdb.set_trace()
                # print delrt[:delrt.index(u'\uff1a')]

                stw = ''.join(delst[num:])
                segs = jieba.cut(stw, cut_all=False)
                for seg in segs:
                    if not stopword.has_key(seg.lower()):
                        stopword[seg.lower()] = 1
                    else:
                        stopword[seg.lower()] += 1
                break
    pdb.set_trace()
    for key in stopword.keys():
        print key,stopword[key]

    print stopword
    stopf = open('stopword', 'wb')
    pickle.dump(stopword, stopf)
    conn.close()
except:
    traceback.print_exc()
    conn.close()
