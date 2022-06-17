from nbformat import write
from requests import request
import urllib3
import re
from loguru import logger
import sys

from bs4 import BeautifulSoup

# 实例化产生请求对象
http = urllib3.PoolManager()

def writeSplit(str, index):
    res = []
    left = 0
    right = 0+index
    while True:
        if right >= len(str):
            if left >= len(str):
                break
            res.append(str[left:len(str)])
            break
        res.append(str[left:right])
        left = right
        right = left + index
    return res

def writeInfo(response):
    with open("cookies.log", 'w', encoding="utf-8") as f:
        res = ""


        f.write('cookie:\n\n')
        res = writeSplit(response.getheader('Set-Cookie'), 80)
        for i in res:
            f.write(i+'\n')
        f.write("\n\n================================================\n\n")


        f.write('headers:\n\n')
        res = writeSplit(str(response.headers), 80)
        for i in res:
            f.write(i+'\n')
        f.write("\n\n================================================\n\n")

        f.write('data:\n\n')
        res = writeSplit(response.data.decode('utf-8'), 80)
        for i in res:
            f.write(i+'\n')
        f.write(response.data.decode('utf-8'))
        f.write("\n\n================================================\n\n")


# get请求指定网址
url = "https://www.baidu.com"
res = http.request("GET",url)

# 获取HTTP状态码
print("status:%d" % res.status)

#print(res.getheader('Set-Cookie'))
#print(res.data)
#print(type(res.headers))
#print(res.headers)
writeInfo(res)

# 获取响应内容
data = res.data.decode("utf-8")

# 正则解析并输出
print(re.findall("<title>(.*?)</title>",data))
