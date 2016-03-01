#coding:utf8
import os
import sys
import codecs
reload(sys)
import email
from parse1 import parse_eml
sys.setdefaultencoding('utf8')

filter_words = ['智联招聘', '在线考评', '51job', '已经有', '不合适', '最新职位', '推荐', '简历排名',  '猎头', '网易考拉', '互联网淘金', '已投']
mailst = ['service@steelport.zhaopin.com', 'service@51job.com']
# path = u"d:/eml/email"
path = u'd:/eml/bugmail'
usedlst = []
nouselst = []

def filter_email(name):
    pth = path + '/' + name
    fp = codecs.open(pth, 'r')
    msg = email.message_from_file(fp)
    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    if emailaddress in mailst:
        return False
    else:
        return True

lst = os.listdir(path)

for pth in lst:
    name = ''
    namefg = True
    try:
        name = pth.decode('gb2312').encode('utf-8')
    except UnicodeDecodeError:
        name = pth
    for word in filter_words:
        if word in name:
            nouselst.append(name)
            namefg = False
            break
    if namefg:
        usedlst.append(name)
        # if filter_email(name):
        #     usedlst.append(name)
        # else:
        #     nouselst.append(name)

print '============================used name:=============================='
for name in usedlst:
    print name
    parse_eml(path + '/' + name)
print len(usedlst)
print '============================noused name:============================'
for name in nouselst:
    print name
print len(nouselst)

