#encoding:utf-8
import sys
# sys.setdefaultencoding('utf8')
import random
import numpy as np

print u'\u4e0a\u5468\u516d\u7684\u5f00\u653e\u65e5\uff0c\u6709\u987e\u5ba2\u6307\u7740\u5de5\u4f5c\u5ba4\u95e8\u5916\u7684\u6a44\u6984\u6811\u95ee\u201c\u4e0a\u6d77\u80fd\u79cd\u6d3b\u5417\uff1f\u201d \u4e4b\u524d\u6211\u4eec\u4e5f\u4e00\u76f4\u62b1\u7740\u8fd9\u6837\u7684\u7591\u95ee\uff0c\u4e0a\u6d77\u7684\u6f6e\u6e7f\u591a\u96e8\uff0c\u6a44\u6984\u6811\u80fd\u9002\u5e94\u5417\uff1f\u73b0\u5728\u770b\u6765\uff0c\u4eca\u5e74\u4e94\u6708\u521d\u4ece\u5916\u5730\u679c\u56ed\u8fd0\u6765\u7684\u4e09\u682a\u4e8c\u5e74\u751f\u6cb9\u6a44\u6984\u82d7\u8fd8\u5168\u90e8\u6210\u6d3b\u4e0b\u6765\u4e86\u5462\u3002\u63a5\u4e0b\u6765\u7684\u76ee\u6807\uff0c\u8be5\u662f\u5e73\u5b89\u8fc7\u51ac\u5427\u3002'

if __name__ == '__main__':
    a = 1
    b = 2.5
    c= 6
    d = 7
    x = np.array([random.randint(1, 20) for i in range(7)])
    y = np.array([random.randint(1, 30) for i in range(7)])
    z = np.array([random.randint(1, 40) for i in range(7)])
    # rst = np.array([x, y, z]).T
    # for index, num in enumerate(x):
    rst = a*x + b*y + c*z +d
    print np.array([x, y, z, rst]).T
