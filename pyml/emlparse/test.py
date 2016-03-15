#coding:utf8
import time
import sys
import email
import os
import time
import time
import argparse
import traceback
reload(sys)
import pdb
from email import utils
import base64
import poplib
from email.header import decode_header
sys.setdefaultencoding('utf8')

filter_words = ['智联', '汇总', '奖品', '确认', '提醒', '在线考评', '薪水', '电影',\
                '会员', '注册', '51job', '已经有', '不合适', '最新职位', '手机',\
                '简历', '跳槽',  '猎头', '网易考拉', '互联网淘金', '已投', '安全问题', '机会'\
                '靠谱']
mailst = ['service@steelport.zhaopin.com', 'service@51job.com']

def decode_nck(nick):
    nklst = nick.split('?')
    return base64.decodestring(nklst[3]).decode(nklst[1])

start = time.time()
if __name__ == '__main__':
    # user = 'bugemail@nrnr.me'
    # password = 'Naren2016'
    # pop3_server = 'pop.exmail.qq.com'
    user = 'nrall001@163.com'
    password = 'nr1531032'
    pop3_server = 'pop.163.com'

    server = poplib.POP3(pop3_server)
    print server.getwelcome()
    server.user(user)
    server.pass_(password)

    print 'Message: %s. Size: %s' % server.stat()

    resp, mails, octets = server.list()
    # print mails
    index = len(mails)
    num = 0
    for v in range(index):
        try:
            flag = 0
            # resp, lines, octets = server.retr(v+1)
            resp, lines, octets = server.top(v+1, 7)
            msg_content = '\r\n'.join(lines)
            msg = email.message_from_string(msg_content)
            # pdb.set_trace()
            fmail = msg.get('From')
            from_mail = utils.parseaddr(msg.get('From'))[1]
            nick = utils.parseaddr(msg.get('From'))[0]
            subject = msg.get('Subject')
            subject = decode_header(subject)[0][0].replace(' ', '')
            try:
                subject = subject.decode('utf8').encode('utf8')
            except:
                try:
                    subject = subject.decode('gbk').encode('utf8')
                except:
                    subject = subject.decode('gb18030').encode('utf8')
            for word in filter_words:
                if word in subject:
                    flag = 1
                    break

            if not flag:
                # print '========================================='
                # print from_mail
                print fmail
                print nick
                if not nick:
                    # pdb.set_trace()
                    nick = ''
                else:
                    if '=' in nick:
                        nick = decode_nck(nick)
                print subject,'||',nick

                num += 1
                # print '*****************************************'
        except:
            pass
    print num
    server.quit()
end = time.time()

print (end - start)
