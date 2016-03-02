#coding:utf8
import sys
import email
import os
import time
import pdb
from email import Parser
reload(sys)
import codecs
from email.header import decode_header
import poplib
sys.setdefaultencoding('utf-8')

messageid_dct = None
pth = 'd:/pop3/'

def validate_mail_path(user):
    path = pth + user
    if not os.path.exists(path):
        os.makedirs(path)
    if not os.path.isfile(path + '/messageid'):
        fle = open(path + '/messageid', 'wb')
        fle.close()

def generate_name(subject, mailtm):
    mailtm = mailtm[:mailtm.find('+')-1]
    mailtime = time.strptime(mailtm, '%a,%d %b %Y %H:%M:%S')
    year = str(mailtime.tm_year)
    mon = '0' + str(mailtime.tm_mon) if mailtime.tm_mon < 10 else str(mailtime.tm_mon)
    day = '0' + str(mailtime.tm_mday) if mailtime.tm_mday < 10 else str(mailtime.tm_mday)
    year_mon = year + mon + day


    pass

def check_email(messageid_dct, messageid, user):
    if messageid_dct is None:
        messageid_dct = {}
        with open(pth + user) as fle:
            lines = fle.readlines()
            for line in lines:
                messageid_dct[line] = 1
    if messageid_dct.has_key(messageid):
        return False
    return True

def write_mail(path, content):
    pass

def parse_eml_local(msg_content):
    # fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_string(msg_content)
    messageid = msg.get('Message-Id')
    if not check_email(messageid_dct, messageid):
        return
    subject = msg.get('Subject')
    name = generate_name(subject)
    for header in ['From', 'To', 'Subject']:
        value = msg.get(header, '')
        print '*****************************'
        print header,':',value
        if header == 'Subject':
            print decode_header(value)[0][0]

    emailaddress = msg.get('from')[msg.get('from').find('<')+1:msg.get('from').find('>')]
    print '======================================================='
    print 'email:',emailaddress
    for bar in msg.walk():
        if not bar.is_multipart():
            name = bar.get_param('name')
            if name:
                print 'attachment:', name
                continue
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
    user = 'bugemail@nrnr.me'
    password = 'Naren2016'
    pop3_server = 'pop.exmail.qq.com'
    server = poplib.POP3(pop3_server)
    pdb.set_trace()
    validate_mail_path(user)

    print server.getwelcome()
    server.user(user)
    server.pass_(password)

    print 'Message: %s. Size: %s' % server.stat()

    resp, mails, octets = server.list()
    print mails

    index = len(mails)
    resp, lines, octets = server.retr(index)
    msg_content = '\r\n'.join(lines)
    print msg_content
    msg = email.message_from_string(msg_content)
    mailtm = msg.get('date')
    mailtm = mailtm[:mailtm.find('+')-1]
    path = 'd:/pop3/mailtest/mailtest.eml'
    open(path, 'wb').write(msg_content)
    # parse_eml_local(msg_content)

    server.quit()