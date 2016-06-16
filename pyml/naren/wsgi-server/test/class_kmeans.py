import jieba
import pdb

with open('d:/naren/kmeans1/result0', 'r') as file:
    lines = file.readlines()

stopwords = {}
with open('d:/naren/stopwords.txt', 'r') as file:
    tlines = file.readlines()
    for line in tlines:
        stopwords[line.strip().decode('gbk')] = 1

wordct = {}

for line in lines:
    seglst = jieba.cut(line.strip(), cut_all=False)
    # pdb.set_trace()
    for seg in seglst:
        if stopwords.has_key(seg):
            continue
        if not wordct.has_key(seg):
            wordct[seg] = 1
        else:
            wordct[seg] += 1

terms = sorted(wordct.items(), key=lambda x:x[1])

for term in terms:
    print term[0], term[1]
