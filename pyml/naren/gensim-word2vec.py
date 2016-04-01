#coding:utf8

import logging
import os.path
import sys
import multiprocessing
reload(sys)
import pdb
sys.setdefaultencoding('utf8')

 
from gensim.corpora import WikiCorpus
from gensim.models import Word2Vec
from gensim.models.word2vec import LineSentence
 
if __name__ == '__main__':
    program = os.path.basename(sys.argv[0])
    logger = logging.getLogger(program)
 
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s')
    logging.root.setLevel(level=logging.INFO)
    logger.info("running %s" % ' '.join(sys.argv))
 
    # check and process input arguments

    inp = 'textfile/input.text'
    outp1 = 'textfile/model'
    outp2 = 'textfile/vector'

    pdb.set_trace()
 
    model = Word2Vec(LineSentence(inp), size=100, window=5, min_count=1,
            workers=multiprocessing.cpu_count())
 
    # trim unneeded model memory = use(much) less RAM
    #model.init_sims(replace=True)
    model.save(outp1)
    model.save_word2vec_format(outp2, binary=False)