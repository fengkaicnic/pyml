#coding:utf8
import utils
import traceback
import jieba
import pickle
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import CountVectorizer
import time
import pdb

start = time.time()

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description, position_name from company where type != "None"'
    cur.execute(sql)
    rst = cur.fetchall()
    transformer=TfidfTransformer()
    vectorizer=CountVectorizer()
    stopf = open('stopword', 'r')
    stopwords = pickle.load(stopf)
    train_data = []
    for rs in rst:
        desc = utils.discrement_unicode(rs[0])
        segs = jieba.cut(desc, cut_all=False)
        wordss = []
        for seg in segs:
            if not stopwords.has_key(seg.lower()):
                wordss.append(seg.lower())
        segs = jieba.cut(utils.discrement_unicode(rs[1]), cut_all=False)

        for seg in segs:
            if not stopwords.has_key(seg.lower()):
                for i in range(5):
                    wordss.append(seg.lower())

        train_data.append(' '.join(wordss))

    tfidf=transformer.fit_transform(vectorizer.fit_transform(train_data))
    word=vectorizer.get_feature_names()
    pdb.set_trace()
    weight = tfidf.toarray()
    tfidfwords = {}

    for wg in weight:
        topsn = [(0, 0) for i in range(15)]
        for i in range(len(wg)):
            topsn = sorted(topsn, key= lambda x:x[0], reverse=True)
            if topsn[-1][0] < wg[i]:
                topsn.pop()
                topsn.append((wg[i], i))
        # pdb.set_trace()
        for tp in topsn:
            print word[tp[1]]
            tfidfwords[word[tp[1]].lower()] = 0
    tfidfwords['java'] = 0
    tfidfwords['c++'] = 0
    tfidfwd = open('tfidfwords', 'wb')

    pickle.dump(tfidfwords, tfidfwd)
    tfidfwd.close()
    pdb.set_trace()
    conn.close()

except:
    traceback.print_exc()
    conn.close()

end = time.time()

print end - start

