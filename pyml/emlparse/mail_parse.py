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
from parse1 import parse_eml

def parse_eml_local(path):
    # fp = codecs.open(path, 'r', encoding='gbk')
    fp = codecs.open(path, 'r')
    msg = email.message_from_file(fp)
    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    print '======================================================='
    print 'email:',emailaddress
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            pdb.set_trace()
            data = bar.get_payload(decode=True)
            if bar.get_content_charset() == 'gb2312':
                print data.decode('gbk').encode('utf-8')
                content = data.decode('gbk').encode('utf-8')
            else:
                print data.decode(bar.get_content_charset()).encode('utf-8')
                content = data.decode(bar.get_content_charset()).encode('utf-8')
            # try:
            #     print data.decode('gb2312').encode('utf-8')
            #     content = data.decode('gb2312').encode('utf-8')
            # except UnicodeDecodeError:
            #     print data
            #     content = data
#             print bar.get_content_maintype()
#             print bar.get_content_type()
            break

if __name__ == '__main__':
    # path = 'd:/nreml'
    path = 'd:/mailtest'
    lst = os.listdir(path)
    for pth in lst:
        pth = path + '/' + pth
        try:
            print pth.decode('gb2312').encode('utf-8')
        except UnicodeDecodeError:
            print pth
        # pdb.set_trace()
        parse_eml(pth)