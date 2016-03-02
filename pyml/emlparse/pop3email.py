#coding:utf8
import sys
import email
import pdb
from email import Parser
reload(sys)
import codecs
from email.header import decode_header
import poplib
sys.setdefaultencoding('utf-8')

def parse_eml_local(msg_content):
    # fp = codecs.open(path, 'r', encoding='gbk')
    msg = email.message_from_string(msg_content)
    pdb.set_trace()
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
    parse_eml_local(msg_content)

    server.quit()