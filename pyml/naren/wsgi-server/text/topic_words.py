#coding:utf8
import utils
import traceback
import pickle
import jieba
import pdb

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description, position_name, type from company where type != "None"'
    cur.execute(sql)
    stopf = open('stopword', 'rb')
    stopword = pickle.load(stopf)
    topics = []

    topic_words = {}

    rst = cur.fetchall()

    for rs in rst:
        desc = rs[0]
        pname = rs[1]
        ptype = rs[2]
        topics.append(ptype)
        topic_word = []
        segs = jieba.cut(utils.discrement_unicode(desc))

        for seg in segs:
            if stopword.has_key(seg):
                continue
            if not topic_words.has_key(seg.lower()):
                topic_words[seg.lower()] = 0
    pdb.set_trace()
    # print topic_words
    for word in topic_words:
        print word
    topic_word = open('topic_word', 'wb')
    pickle.dump(topic_words, topic_word)
except:
    traceback.print_exc()
