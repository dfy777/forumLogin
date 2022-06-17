import imp
from posixpath import split
import ssl
import urllib3
import pathlib
from bs4 import BeautifulSoup
import myprint as mypr


class HostLoc(object):
    username = None
    password = None
    loginUrl = "/wp-login.php"
    referer = "https://www.teaqqq.com/wp-login.php"
    creditUrl = "/home.php?mod=spacecp&ac=credit&showcredit=1&inajax=1&ajaxtarget=extcreditmenu_menu"
    userAgent = "User-Agent,Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.67 Safari/537.36"
    cookie = {}
    
    http = None;
    origin_cookie = None
    identity_cookie_name = None
    host = None

    def __init__(self, username, password, host, identity_cookie_name):
        self.username = username
        self.password = password
        self.host = host
        self.identity_cookie_name = identity_cookie_name
        self.loginUrl = self.host + self.loginUrl
        self.creditUrl = self.host + self.creditUrl
        self.http = urllib3.PoolManager(cert_reqs=ssl.CERT_NONE, assert_hostname=False)

        self.handleCookie()
    
    def is_Login(self):
        if self.identity_cookie_name in self.cookie:
            return True
        return False

    def Login(self):
        print(0)
        response = self._request("POST", self.loginUrl, fields={
            "log":self.username,
            "pwd":self.password,
            "testcookie":1, 
            "redirect_to": "https://www.teaqqq.com/wp-admin/"
        })
        print(4)
        if response.status == 400:
            print("服务器已限制")
            return False
        
        if response.status == 200:
            print("success")
            return True

        print("status:")
        print(response.status)
        print(response.getheaders())
        print(response.data)

        return False



    def info():
        pass

    def _request(self, method, url, fields = None):
        print(1)
        headers = {
            "origin": self.host,
            "referer": self.referer,
            "User-Agent": self.userAgent,
        }

        if len(self.cookie) > 0:
            headers['cookie'] = self.joinCookies()
        
        response = self.http.request(
            method, url, fields, headers
        )


        print(2)
        cookies = response.getheader('Set-Cookie')
        if len(cookies) > 0:
            #self.cookie.update(cookies)
            print(cookies)
            print("-------")
        
        #TODO 检验aes

        
        return response

    

    def joinCookies(self):
        cookie_str = ""
        for key, value in self.cookie.items():
            cookie_str += key + "=" + value + ";"
        return cookie_str.rstrip(";")


    def parseCookie(self, cookie=None):
        res = {}
        if cookie == None:
            return cookie

        for val in cookie.split(';'):
            lis = val.split('=')
            if (len(lis) < 2 or lis[0].strip() in ["expires", "max-age", "path"]):
                continue
            name = lis[0]
            index = lis[0].find(',')
            if index != -1:
                name = name[index+1:].lstrip()
            res[name] = lis[1]
        return res


    def handleCookie(self):
        if self.origin_cookie != None:
            for value in self.origin_cookie.split(';'):
                lis = value.split('=')
                self.cookie[lis[0]] = lis[1]


    def readCookie():
        if pathlib.Path("./cookie.txt").exists():
            with open("cookie.txt", 'r') as f:
                return f.read()
        else:
            return None
    

if __name__ =="__main__":
    tb = HostLoc("", "", "https://www.teaqqq.com", "d")
    if (tb.is_Login()) == False:
        tb.Login()
    
