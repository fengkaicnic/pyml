# coding:utf8
import sys
import email
import base64
import codecs
import re
reload(sys)
import os
import pdb
sys.setdefaultencoding('utf8')

family_dct = {}


def get_family_dct():
    with open("xing.txt", 'r') as file:
        lines = file.readlines()
        for line in lines:
            for word in line.split(' '):
                if not family_dct.has_key(word.strip()):
                    family_dct[word.strip()] = 1

    return family_dct