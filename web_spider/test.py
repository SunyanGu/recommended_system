#coding: utf-8
import multiprocessing
import time

# class a(object):
#     def __init__(self):
#         pass
#
#     def func(self,msg):
#         print ("msg:", msg)
#         time.sleep(3)
#         print ("end")
#
#     def run(self):
#         pool = multiprocessing.Pool(processes=4)
#         pool.map(self.func, range(4))  # 维持执行的进程总数为processes，当一个进程执行完毕后会添加新的进程进去
#         print("Mark~ Mark~ Mark~~~~~~~~~~~~~~~~~~~~~~")
#         pool.close()
#         pool.join()  # 调用join之前，先调用close函数，否则会出错。执行完close后不会有新的进程加入到pool,join函数等待所有子进程结束
#         print("Sub-process(es) done.")
#
#
# if __name__ == "__main__":
#     c = a()
#     c.run()

# import multiprocessing
#
# class someClass(object):
#     def __init__(self):
#         pass
#
#     def f(self, x):
#         print(x*x)
#
#     def go(self):
#         pool = multiprocessing.Pool(processes=4)
#         pool.map(self.f, range(10))
#         pool.close()
#         pool.join()
# if __name__ == "__main__":
#     a = someClass()
#     a.go()

# from get_url import header,user_index_distinct,user_information,shop_information
# from multiprocessing.dummy import Pool
#
# def get_member_information(a):
#     print(a)
#
# if __name__ == "__main__":
#     # 清空数据库
#     user_information.remove()
#     store_link = []
#     #User = UserCrawler()
#     for i in user_index_distinct.find():
#         store_link.append(i['user_url_distinct'])
#         # 初始化进程池
#     pool = Pool()
#     # 多进程爬取
#     pool.map(get_member_information, store_link)
#     pool.close()
#     pool.join()

# http://cn-proxy.com/
import random
from get_url import header,user_index_distinct,user_information,shop_information
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import socket
socket.setdefaulttimeout(3)


def Get_IP():
    f=open(".\IP.txt",'r')
    ip_list = []
    IP = f.readlines()
    for ip in IP:
        a = 'http://' + ip
        ip_list.append(a.strip())
    f.close()
    return ip_list

def is_good(proxy_ip):
    try:
        proxies = {'http': proxy_ip}
        web_page = requests.get('http://www.dianping.com', proxies=proxies,timeout=5)
        soup = BeautifulSoup(web_page.text, 'lxml')
        title = soup.title.text
        print(title)
        if title == '雪霁_2277的主页-会员-大众点评网':
            url_item = proxies['http']
            #print(url_item)
            return url_item
        else:
            #print(soup)
            return 0
    except:
        print('rubbish')
        return 0

#http://www.dianping.com/member/703158841


# def member_scored(url):
#     proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
#     proxies = {'http': proxy_ip}
#     web_page = requests.get(url,proxies=proxies,timeout=5)
#     soup = BeautifulSoup(web_page.text, 'lxml')
#     print(soup)
#     title = soup.title.text
#     print(title)


# def write():
#     f = open('./test.txt', 'w')
#     for i in range(100):
#         f.write(str(i))
#         f.write('\n')
#
# def read():
#     r = open('./test.txt','r')
#     a = r.readlines()
#     for i in a:
#         print(i)

if __name__ == '__main__':

    proxy_list = Get_IP()
    print(proxy_list)
    f = open('./good_ip.txt', 'a+')
    good_list = []
    #member_scored('http://www.dianping.com/shop/66183871')
    for proxy_ip in proxy_list:
        good_ip = is_good(proxy_ip)
        if good_ip != 0:
            good_list.append(is_good(proxy_ip))

    for i in good_list:
        try:
            f.write(i)
            f.write('\n')
        except:
            print('rubbish')




    # proxy_list = []
    # a = open('./good_ip.txt', 'r')
    # for i in a.readlines():
    #     proxy_list.append(i.strip())
    # print(proxy_list)




