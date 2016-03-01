# coding:utf8
import sys
import email
import base64
import codecs
from bs4 import BeautifulSoup
import re
reload(sys)
import os
import pdb
sys.setdefaultencoding('utf8')

soup = BeautifulSoup(open('testfle.txt'))

spanlst = soup.find_all('span')
for span in spanlst:
    print span.text
