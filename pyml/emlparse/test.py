#coding:utf8
import os
import sys
import base64
reload(sys)
import re
sys.setdefaultencoding('utf8')
import pdb

emailp = re.compile('\w[-\w.+]*@([A-Za-z0-9][-A-Za-z0-9]+\.)+[A-Za-z]{2,14}')

pdb.set_trace()
strings = ''' 
Can not deliver the message you sent. Will not retry.

Sender: <59aaf40c-df5c-11e5-8780-00163e1cf649@email.xnaren.com>

The following addresses had delivery problems

<wang.qiang@o-film.com> : Reply from mx20.o-film.com[192.168.119.110]:
        >>> RCPT TO:<wang.qiang@o-film.com>
        <<< 550 5.1.1 <wang.qiang@o-film.com>: Recipient address rejected: User unknown
'''

emailone = emailp.search(strings)
emails = re.findall(emailp, strings)

print emailone.group()
print emails