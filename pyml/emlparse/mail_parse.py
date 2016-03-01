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

def parse_eml(path):
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
            try:
                print data.decode('gb2312').encode('utf-8')
                content = data.decode('gb2312').encode('utf-8')
            except UnicodeDecodeError:
                print data
                content = data
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
        parse_eml(pth)