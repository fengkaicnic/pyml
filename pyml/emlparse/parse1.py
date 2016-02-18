#coding:utf8
import sys
import email
reload(sys)
import os
import pdb
sys.setdefaultencoding('utf8')

def parse_eml(path):
    fp = open(path, 'r')
    msg = email.message_from_file(fp)
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print '附件名:', name
                continue
            data = bar.get_payload(decode=True)
            print data
            break

path = 'd:/naren'
lst = os.listdir(path)
for pth in lst:
    pth = path + '/' + pth
    pdb.set_trace()
    print pth
    
    parse_eml(pth)
    
    
