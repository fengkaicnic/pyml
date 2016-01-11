import sys
import urllib
import binascii
import urllib2
import cookielib
import rsa
import base64
import re
import json
import hashlib

class weiboLogin:
    cj = cookielib.LWPCookieJar()
    cookie_support = urllib2.HTTPCookieProcessor(cj)
    opener = urllib2.build_opener(cookie_support, urllib2.HTTPHandler)
    urllib2.install_opener(opener)
    postdata = {
        'entry': 'weibo',
        'gateway': '1',
        'from': '',
        'savestate': '7',
        'userticket': '1',
        'ssosimplelogin': '1',
        'vsnf': '1',
        'vsnval': '',
        'su': '',
        'service': 'miniblog',
        'servertime': '',
        'nonce': '',
        'pwencode': 'rsa2',
        'sp': '',
        'encoding': 'UTF-8',
        'prelt': '115',
        'url': 'http://weibo.com/ajaxlogin.php?framelogin=1&callback=parent.sinaSSOController.feedBackUrlCallBack',
        'returntype': 'META'
    }

    def get_servertime(self):
#         url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=dW5kZWZpbmVk&client=ssologin.js(v1.3.18)&_=1329806375939'
        url = 'http://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.11)&_=1379834957683'
        data = urllib2.urlopen(url).read()
        p = re.compile('\((.*)\)')
        try:
            json_data = p.search(data).group(1)
            data = json.loads(json_data)
            servertime = str(data['servertime'])
            nonce = data['nonce']
            pubkey = data['pubkey']
            rsakv = data['rsakv']
            return servertime, nonce, pubkey, rsakv
        except:
            print 'Get severtime error!'
            return None

    def get_pwd(self, password, servertime, nonce, pubkey):  
        rsaPublickey = int(pubkey, 16)  
    
        key = rsa.PublicKey(rsaPublickey, 65537)   
    
        message = str(servertime) + '\t' + str(nonce) + '\n' + str(password)   
    
        passwd = rsa.encrypt(message, key)   
    
        passwd = binascii.b2a_hex(passwd)   
        return passwd  

    def get_pwd_old(self, pwd, servertime, nonce, pubkey=None):
        pwd1 = hashlib.sha1(pwd).hexdigest()
        pwd2 = hashlib.sha1(pwd1).hexdigest()
        pwd3_ = pwd2 + servertime + nonce
        pwd3 = hashlib.sha1(pwd3_).hexdigest()
        return pwd3

    def get_user(self, username):
        username_ = urllib.quote(username)
        username = base64.encodestring(username_)[:-1]
        return username


    def login(self,username,pwd):
        url = 'http://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.3.18)'
        #url = curl "http://weibo.com/login.php?url=http"%"3A"%"2F"%"2Fd.weibo.com"%"2F1087030002_417"%"3Ffrom"%"3Dunlogin_home"%"26mod"%"3Dpindao"%"26type"%"3Dpeople&comefrom=loginlayer" -H "Accept-Encoding: gzip, deflate, sdch" -H "Accept-Language: zh-CN,zh;q=0.8" -H "User-Agent: Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36" -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8" -H "Referer: http://d.weibo.com/1087030002_417?from=unlogin_home&mod=pindao&type=people" -H "Cookie: SINAGLOBAL=7988859217148.274.1431684154096; TC-Ugrow-G0=5e22903358df63c5e3fd2c757419b456; TC-V5-G0=52dad2141fc02c292fc30606953e43ef; _s_tentry=login.sina.com.cn; Apache=7041303883306.682.1452132590376; ULV=1452132590680:157:2:2:7041303883306.682.1452132590376:1452047381381; TC-Page-G0=0dba63c42a7d74c1129019fa3e7e6e7c; YF-V5-G0=9717632f62066ddd544bf04f733ad50a; login_sid_t=df6230055173b685671e131e6d7f7a90; un=fengkaibnu@sina.cn; myuid=1789397551; UOR=,,login.sina.com.cn; SUS=SID-1789397551-1452257693-XD-c9oj1-75c85180fd4df46ded2878b623bcbc04; SUE=es"%"3D05c742c9d6c7eb1b57fdfffce10688d5"%"26ev"%"3Dv1"%"26es2"%"3D923e61751881d043bec0a73e097adee7"%"26rs0"%"3D4i040W6VxfQanc62mKt5dHXPwpANiTMZZe6lzLkz3NcbfQZeIFaTmy0akasaxRLphBh8MhqQtc"%"252BO5"%"252FvRwAsfrs8zN"%"252B8oV0DMcbJUxfcMG9TUovLv"%"252Fg"%"252FKn5utKIZ9gYnLLPL71ScAVifl2pweT3SpSvy5nurpl9NfwcnOv609vaM"%"253D"%"26rv"%"3D0; SUP=cv"%"3D1"%"26bt"%"3D1452257693"%"26et"%"3D1452344093"%"26d"%"3Dc909"%"26i"%"3Dbc04"%"26us"%"3D1"%"26vf"%"3D0"%"26vt"%"3D0"%"26ac"%"3D0"%"26st"%"3D0"%"26uid"%"3D1789397551"%"26name"%"3Dfengkaibnu"%"2540sina.cn"%"26nick"%"3D"%"25E5"%"25A4"%"25A7"%"25E7"%"25AC"%"25A8"%"26fmp"%"3D"%"26lcp"%"3D; SUB=_2A257i8HNDeTxGedJ41sS-SnJzj2IHXVY4LQFrDV8PUNbuNAPLVLgkW9LHetFH_sSWEKiW8spOyDmsHC6cWTGjA..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhYEKY_bHIOC5Tm2zLZlMBd5JpX5K2t; SUHB=0qjl1kgWy3wA70; ALF=1452862493; SSOLoginState=1452257693" -H "Connection: keep-alive" --compressed
        try:
            servertime, nonce, pubkey, rsakv = self.get_servertime()
        except:
            print 'get servertime error!'
            return
        weiboLogin.postdata['servertime'] = servertime
        weiboLogin.postdata['nonce'] = nonce
        weiboLogin.postdata['rsakv'] = rsakv
        weiboLogin.postdata['su'] = self.get_user(username)
        weiboLogin.postdata['sp'] = self.get_pwd(pwd, servertime, nonce, pubkey)
        weiboLogin.postdata = urllib.urlencode(weiboLogin.postdata)
        headers = {'User-Agent':'Mozilla/5.0 (X11; Linux i686; rv:8.0) Gecko/20100101 Firefox/8.0 Chrome/20.0.1132.57 Safari/536.11'}
        req  = urllib2.Request(
            url = url,
            data = weiboLogin.postdata,
            headers = headers
        )
        result = urllib2.urlopen(req)
        text = result.read()
        #p = re.compile('location\.replace\(\'(.*?)\'\)')
        import pdb
        pdb.set_trace()
        p = re.compile('location\.replace\([\'"](.*?)[\'"]\)')  
        try:
            login_url = p.search(text).group(1)
            urllib2.urlopen(login_url)
            print "Login success!"
        except:
            print 'Login error!'