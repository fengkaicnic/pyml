import utils
import traceback
import pickle
import jieba
import copy
import pdb
import time
import numpy as np
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis
from sklearn.feature_extraction.text import HashingVectorizer
from sklearn.naive_bayes import MultinomialNB

start = time.time()

comma_tokenizer = lambda x: jieba.cut(x, cut_all=True)

jieba.load_userdict('dict.txt')

def vectorize(train_words):
    v = HashingVectorizer(tokenizer=comma_tokenizer, n_features=30000, non_negative=True)
    train_data = v.fit_transform(train_words)
    return train_data

try:
    conn = utils.persist.connection()
    cur = conn.cursor()
    sql = 'select description, type, position_name from company where type != "None"'
    cur.execute(sql)
    rst = cur.fetchall()

    # topic_word = open('topic_word', 'r')
    topic_word = open('tfidfwords', 'r')
    topic_words = pickle.load(topic_word)
    topicsx = []
    topicsy = []

    type_dct = {}
    type_dct_r = {}

    train_data = []
    train_tags = []
    for rs in rst:
        desc = rs[0]
        segs = jieba.cut(utils.discrement_unicode(desc).lower(), cut_all=False)
        tpword = copy.deepcopy(topic_words)
        train_words = []
        for seg in segs:
            if tpword.has_key(seg.lower()):
                tpword[seg.lower()] += 1
        segs = jieba.cut(utils.discrement_unicode(rs[2]).lower(), cut_all=False)

        for seg in segs:
            if tpword.has_key(seg.lower()):
                tpword[seg.lower()] += 1
        # pdb.set_trace()
        # for key in sorted(tpword.keys()):
        for key in tpword.keys():
            train_words.append(tpword[key])

        train_data.append(train_words)

        train_tags.append(utils.discrement_unicode(rs[1]))

    clf = MultinomialNB(alpha=0.01)
    pdb.set_trace()
    train_data = np.array(train_data)
    train_tags = np.array(train_tags)
    clf.fit(train_data, train_tags)

    sqll = 'select description, position_name, id from company where type = "None"'

    cur.execute(sqll)
    rst = cur.fetchall()

    # pdb.set_trace()
    for rs in rst:
        desc = rs[0]
        segs = jieba.cut(utils.discrement_unicode(desc), cut_all=False)
        tpword = copy.deepcopy(topic_words)
        for seg in segs:
            if tpword.has_key(seg.lower()):
                tpword[seg.lower()] += 1
        test_words = []
        for key in tpword.keys():
            test_words.append(tpword[key])

        test_data = np.array(test_words)

        pred = clf.predict(test_data)
        print pred[0], utils.discrement_unicode(rs[1]), rs[2]
except:
    traceback.print_exc()

pdb.set_trace()
end = time.time()

print end - start
