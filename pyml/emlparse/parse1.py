# coding:utf8
import sys
import email
import base64
import codecs
import re
reload(sys)
import os
import pdb
from bs4 import BeautifulSoup
sys.setdefaultencoding('utf8')
from family_name import get_family_dct

urlph = re.compile('(http|ftp|https):\/\/[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
urlp = re.compile('[\w\-_]+(\.[\w\-_]+)+([\w\-\.,@?^=%&amp;:/~\+#]*[\w\-\@?^=%&amp;/~\+#])?')
mphonep = re.compile('(1(([3578][0-9])|(47)|[8][0126789]))\d{8}')
telephonep = re.compile('0\d{2,3}(\-)?\d{7,8}')
telephonep1 = re.compile('\d{7,8}')
chinesep = re.compile(u'^[\u4e00-\u9fa5]+$')
#chinesepl = re.compile('[\x{4e00}-\x{9fa5}]+')

family_dct = get_family_dct()

def check_name(name):
    if len(name) > 10:
        return False
    for key in family_dct.iterkeys():
        if name.startswith(key):
            if not u'先生' in name and not u'女士' in name:
                return True
    return False

def check_address(address):
    if len(address) < 10:
        return False
    return True

def html_parser(content):
    soup = BeautifulSoup(content)
    spanlst = soup.find_all('span')
    contentlst = []
    for span in spanlst:
        contentlst.append(span.text)
    return contentlst

def extract_data(content):
    url = urlph.search(content)
    # mphone = mphonep.search(content)
    # telephone = telephonep.search(content)
    if url:
        print 'url:',url.group(0)
    else:
        url = urlp.search(content)
        if url and 'www' in url.group(0):
            print 'url:',url.group(0)
    # if mphone:
    #     print '手机：',mphone.group(0)
    # if telephone:
    #     print '座机：',telephone.group(0)
#     pdb.set_trace()
    if content.count('\n') < 5:
        contentlst = content.split(' ')
    else:
        contentlst = content.split('\n')
    for line_l in contentlst:
        # pdb.set_trace()
        for line in line_l.split('|'):
            if u'说明: 说明' in line:
                continue
            for linen in line.split(' '):
                if len(linen.strip(' ')) < 10 and len(linen.strip(' ')) > 5:
    #             pdb.set_trace()
                    name = chinesep.search(linen.strip().strip(' ').decode('utf-8'))
                    if name:
                        if check_name(name.group(0)):
                            print "联系人：",name.group(0)
                continue
            linet = line.replace(' ', '')
            mphone = mphonep.search(linet)
            telephone = telephonep.search(linet)
            if not telephone:
                telephone = telephonep1.search(linet)
            if mphone:
                print '手机：',mphone.group(0)
            if telephone:
                print '座机：',telephone.group(0)

            if linet.find('联系人：') != -1:
                if check_name(linet[linet.find('联系人')+len('联系人：'):]):
                    print "联系人：",linet[linet.find('联系人')+len('联系人：'):]
                    continue

            if linet.find('联系人:') != -1:
                if check_name(linet[linet.find('联系人:')+len('联系人:'):]):
                    print "联系人：",linet[linet.find('联系人:')+len('联系人:'):]
                    continue

            if linet.find('地址：') != -1:
                if check_address(linet[linet.find('地址')+len('地址：'):]):
                    print '地址：',linet[linet.find('地址')+len('地址：'):]
                    continue

            if linet.find('地址:') != -1:
                if check_address(linet[linet.find('地址:')+len('地址:'):]):
                    print '地址：',linet[linet.find('地址:')+len('地址:'):]
                    continue

            if linet.find('地点：') != -1:
                if check_address(linet[linet.find('地点')+len('地点：'):]):
                    print '地点：',linet[linet.find('地点')+len('地点：'):]
                    continue

            if linet.find('地点:') != -1:
                if check_address(linet[linet.find('地点:')+len('地点:'):]):
                    print '地点：',linet[linet.find('地点:')+len('地点:'):]
    
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
            if bar.get_content_type() == 'text/plain':
                data = bar.get_payload(decode=True)
            else:
                data = '\n'.join(html_parser(bar.get_payload(decode=True)))
            try:
                if bar.get_content_charset() == 'gb2312':
                    # print data.decode('gbk').encode('utf-8')
                    content = data.decode('gbk').encode('utf-8')
                else:
                    # print data.decode(bar.get_content_charset()).encode('utf-8')
                    content = data.decode(bar.get_content_charset()).encode('utf-8')
            except UnicodeDecodeError:
                print data
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
