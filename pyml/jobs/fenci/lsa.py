# -*- coding: utf-8 -*-
"""
Created on Wed Jun 11 17:02:39 2014

@author: modified by zhouxu,add plot
"""

from numpy import zeros
import numpy as np
from scipy.linalg import svd
from matplotlib import pyplot as plt


titles =[
    "The Neatest Little Guide to Stock Market Investing",
    "Investing For Dummies, 4th Edition",
    "The Little Book of Common Sense Investing: The Only Way to Guarantee Your Fair Share of Stock Market Returns",
    "The Little Book of Value Investing",
    "Value Investing: From Graham to Buffett and Beyond",
    "Rich Dad's Guide to Investing: What the Rich Invest in, That the Poor and the Middle Class Do Not!",
    "Investing in Real Estate, 5th Edition",
    "Stock Investing For Dummies",
    "Rich Dad's Advisors: The ABC's of Real Estate Investing: The Secrets of Finding Hidden Profits Most Investors Miss"
]
stopwords = ['and','edition','for','in','little','of','the','to']
ignorechars = ''''',:'!'''


class LSA(object):
    def __init__(self, stopwords, ignorechars):
        self.stopwords = stopwords
        self.ignorechars = ignorechars
        self.wdict = {}
        self.dcount = 0

    def parse(self, doc):
        words = doc.split(); 
        for w in words:
            #print self.dcount
            w = w.lower().translate(None, self.ignorechars)
            if w in self.stopwords:
                continue
            elif w in self.wdict:
                self.wdict[w].append(self.dcount)
            else:
                self.wdict[w] = [self.dcount]
        self.dcount += 1

    def build(self):
        self.keys = [k for k in self.wdict.keys() if len(self.wdict[k]) > 1]
        self.keys.sort()
        print self.keys
        self.A = zeros([len(self.keys), self.dcount])
        for i, k in enumerate(self.keys):
            for d in self.wdict[k]:
                self.A[i,d] += 1
    
    
    def printA(self):
        print self.A
        u,s,vt = svd(self.A)
        print """\r"""        
        print u
        print """\r"""
        print s
        print """\r"""        
        print vt
        print """\r"""  
        
        plt.title("LSA")
        plt.xlabel(u'dimention2')
        plt.ylabel(u'dimention3')

        titles = ['T1','T2','T3','T4','T5','T6','T7','T8','T9']
        vdemention2 = vt[1]
        vdemention3 = vt[2]
        for j in range(len(vdemention2)):
            plt.text(vdemention2[j],vdemention3[j],titles[j]) 
        plt.plot(vdemention2, vdemention3, '.')        
        
        ut = u.T
        demention2 = ut[1]
        demention3 = ut[2]
        for i in range(len(demention2)):
            plt.text(demention2[i],demention3[i],self.keys[i]) 
        plt.plot(demention2, demention3, '.')
        
import pdb
mylsa = LSA(stopwords, ignorechars)
for t in titles:
    mylsa.parse(t)
mylsa.build()
pdb.set_trace()
mylsa.printA()
