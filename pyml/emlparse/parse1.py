#coding:utf8
import sys
import email
import base64
import codecs
reload(sys)
import os
import pdb
sys.setdefaultencoding('utf8')

def parse_eml(path):
#     fp = open(path, 'r')
    fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_file(fp)
#     pdb.set_trace()
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            data = bar.get_payload(decode=True)
            try:
                print data.decode('gb2312').encode('utf-8')
            except UnicodeDecodeError:
                print data
            print bar.get_content_maintype()
            print bar.get_content_type()
            break

def parse_eml_string(path):
    textflag = False
    base64flag = False
    linelst = []
#     with codecs.open(path, 'r', encoding='gbk') as file:
    with open(path, 'r') as file:
        
        lines = file.readlines()
        for line in lines:
            if textflag and base64flag:
                if 'NextPart' not in line:
                    linelst.append(line)
                else:
                    break
            if 'Content-Type' in line:
                if 'text/plain' in line:
                    textflag = True
                else:
                    textflag = False
                continue
            if 'Content-Transfer-Encoding' in line and 'base64' in line:
                if textflag:
                    base64flag = True
            
        pdb.set_trace()        
        strings = ''.join(map(lambda st:st.replace('\n', ''), linelst))
        print base64.decodestring(strings)
        
path = 'd:/naren'
lst = os.listdir(path)
for pth in lst:
    pth = path + '/' + pth
#     pdb.set_trace()
    print pth
    
    parse_eml(pth)
#     parse_eml_string(pth)
print sys.getfilesystemencoding()
