#coding:utf8
import sys
import os
reload(sys)
import json
import pdb
sys.setdefaultencoding('utf8')

with open("d:/naren/data/read/66510-11561507.txt") as file:
    content = json.load(file)


rst = []
for key in content.iterkeys():
    print key
    # rst.append(key + u':' + content[key].decode('utf8'))

pdb.set_trace()

rst.append(content['selfappraise'].decode('utf8').encode('gbk'))
rst.append(eval(content['education_history'])[0]['major'].encode('gbk'))

with open('d:/naren/data/test.txt', 'wb') as file:
    file.writelines('\r\n'.join(rst))

