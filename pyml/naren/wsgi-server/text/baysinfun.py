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

def vectorize(train_words):
    v = HashingVectorizer(tokenizer=comma_tokenizer, n_features=1000, non_negative=True)
    train_data = v.fit_transform(train_words)
    return train_data

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
    train_words = []
    train_tags = []
    for rs in rst:
        desc = rs[0]
        train_words.append(utils.discrement_unicode(desc))
        train_tags.append(utils.discrement_unicode(rs[1]))
    pdb.set_trace()
    train_data = vectorize(train_words)
    clf = MultinomialNB(alpha=0.01)

    clf.fit(train_data, train_tags)

    sqll = 'select description, position_name, id from company where type = "None"'

    cur.execute(sqll)
    rst = cur.fetchall()

    test_words = []
    pdb.set_trace()
    for rs in rst:
        desc = rs[0]
        # test_words = vectorize(utils.discrement_unicode(desc))
        # pred = clf.predict(test_words)
        # print pred[0], utils.discrement_unicode(rs[1])
        test_words.append(utils.discrement_unicode(desc))

    test_data = vectorize(test_words)
    pdb.set_trace()
    for test in test_data:
        pred = clf.predict(test)
        print pred[0]
except:
    traceback.print_exc()

end = time.time()

print end - start
