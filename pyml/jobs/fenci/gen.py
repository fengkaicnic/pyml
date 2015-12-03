import jieba
from gensim import corpora, models, similarities
import os 
import random
from pprint import pprint
import string
import re

RESULT_DIR = 'douban_result'
regex = re.compile(ur"[^\u4e00-\u9f5aa-zA-Z0-9]")

class DoubanDoc(object):
    def __init__(self, root_dir='douban'):
        self.root_dir = root_dir

    def __iter__(self):
        for name in os.listdir(self.root_dir):
            if os.path.isfile(os.path.join(self.root_dir, name)):
                data = open(os.path.join(self.root_dir, name), 'rb').read()
                title = data[:data.find('\r\n')]
                yield (name, title, data)


class DoubanCorpus(object):
    def __init__(self, root_dir, dictionary):
        self.root_dir = root_dir
        self.dictionary = dictionary

    def __iter__(self):
        for name, title, data in DoubanDoc(self.root_dir):
            yield self.dictionary.doc2bow(jieba.cut(data, cut_all=False))

def random_doc():
    name = random.choice(os.listdir('douban'))
    data = open('douban/%s'%name, 'rb').read()
    print 'random choice ', name
    return name, data

texts = []
for name, title, data in DoubanDoc():
    def etl(s): #remove 标点和特殊字符
        s = regex.sub('', s)
        return s

    seg = filter(lambda x: len(x) > 0, map(etl, jieba.cut(data, cut_all=False)))
    texts.append(seg)

# remove words that appear only once
all_tokens = sum(texts, [])
token_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in token_once] for text in texts]
dictionary = corpora.Dictionary(texts)

corpus = list(DoubanCorpus('douban', dictionary))

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]
lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=30)

i = 0
for t in lsi.print_topics(30):
    print '[topic #%s]: '%i, t
    i+=1

index = similarities.MatrixSimilarity(lsi[corpus])

_, doc = random_doc()
vec_bow = dictionary.doc2bow(jieba.cut(doc, cut_all=False))
vec_lsi = lsi[vec_bow]
print 'topic probability:'
pprint(vec_lsi)
sims = sorted(enumerate(index[vec_lsi]), key=lambda item: -item[1])
print 'top 10 similary notes:'
pprint(sims[:10])