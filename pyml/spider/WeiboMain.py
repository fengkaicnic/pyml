#encoding:utf-8

import urllib2
import cookielib
import WeiboEncode
import WeiboSearch
import WeiboLogin

if __name__ == '__main__':
    weiboLogin = WeiboLogin.WeiboLogin('fengkaibnu@sina.cn', 'woxihuanni')
    if weiboLogin.Login():
        print 'log wright'
    else:
        print 'log error'