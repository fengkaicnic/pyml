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

urlph = re.compile('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
urlp = re.compile('[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
mphonep = re.compile('(1(([35][0-9])|(47)|[8][0126789]))\d{8}')
telephonep = re.compile('0\d{2,3}(\-)?\d{7,8}')

def extract_data(content):
    url = urlph.search(content)
    mphone = mphonep.search(content)
    telephone = telephonep.search(content)
    if url:
        print url.group(0)
    else:
        url = urlp.search(content)
        if 'www' in url.group(0):
            print url.group(0)
    if mphone:
        print mphone.group(0)
    if telephone:
        print telephone.group(0)
    
def parse_eml(path):
    fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_file(fp)
    pdb.set_trace()
    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    print emailaddress
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            data = bar.get_payload(decode=True)
            try:
#                 print data.decode('gb2312').encode('utf-8')
                content = data
            except UnicodeDecodeError:
#                 print data
                content = data
            extract_data(content)
#             print bar.get_content_maintype()
#             print bar.get_content_type()
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
    
    try:
        print pth.decode('gb2312').encode('utf-8')
    except UnicodeDecodeError:
        print pth
    parse_eml(pth)
