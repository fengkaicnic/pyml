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
from family_name import get_family_dct

urlph = re.compile('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
urlp = re.compile('[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
mphonep = re.compile('(1(([357][0-9])|(47)|[8][0126789]))\d{8}')
telephonep = re.compile('0\d{2,3}(\-)?\d{7,8}')
telephonep1 = re.compile('\d{7,8}')
chinesep = re.compile(u'^[\u4e00-\u9fa5]+$')
#chinesepl = re.compile('[\x{4e00}-\x{9fa5}]+')

family_dct = get_family_dct()

def check_name(name):
    for key in family_dct.iterkeys():
        if name.startswith(key):
            return True
    return False

def extract_data(content):
    url = urlph.search(content)
    mphone = mphonep.search(content)
    telephone = telephonep.search(content)
    if not telephone:
        telephone = telephonep1.search(content)
    if url:
        print 'url:',url.group(0)
    else:
        url = urlp.search(content)
        if 'www' in url.group(0):
            print 'url:',url.group(0)
    if mphone:
        print '手机：',mphone.group(0)
    if telephone:
        print '座机：',telephone.group(0)
#     pdb.set_trace()
    contentlst = content.split('\n')
    for line in contentlst:
        for linen in line.split(' '):
            if len(linen) < 13 and len(linen) > 5:
#             pdb.set_trace()
                name = chinesep.search(linen.strip().decode('utf-8'))
                if name:
                    if check_name(name.group(0)):
                        print "联系人：",name.group(0)
            continue
        linet = line.replace(' ', '')

        if linet.find('联系人：') != -1:
            print "联系人：",linet[linet.find('联系人')+len('联系人：'):]
            continue

        if linet.find('联系人:') != -1:
            print "联系人：",linet[linet.find('联系人:')+len('联系人:'):]
            continue
        
        if linet.find('地址：') != -1:
            print '地址：',linet[linet.find('地址')+len('地址：'):]
            continue
        
        if linet.find('地址:') != -1:
            print '地址：',linet[linet.find('地址:')+len('地址:'):]
    
def parse_eml(path):
    fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_file(fp)
    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    print 'email:',emailaddress
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
            data = bar.get_payload(decode=True)
            try:
#                 print data.decode('gb2312').encode('utf-8')
                content = data.decode('gb2312').encode('utf-8')
            except UnicodeDecodeError:
                # print data
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
        
path = 'd:/eml'
lst = os.listdir(path)
for pth in lst:
    pth = path + '/' + pth
    
    try:
        print pth.decode('gb2312').encode('utf-8')
    except UnicodeDecodeError:
        print pth
    parse_eml(pth)
