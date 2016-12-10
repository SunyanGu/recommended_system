#/usr/local env python
#coding utf-8
import os
import urllib
from bs4 import BeautifulSoup
import requests
# def Get_IP():
#     f=open(".\IP.txt",'r')
#     ip_list = []
#     IP = f.readlines()
#     print(IP)
#     for ip in IP:
#         a = 'http://' + ip
#         ip_list.append(a.strip())
#     f.close()
#     return ip_list
#
# ip_list = Get_IP()
# w = open('.\IP_.txt','w')
# for i in ip_list:
#     w.write(i)
# print(ip_list)

# a = ['a','b','c','d']
# a.remove('a')
# print(a)
# import random
#
# def get_url():
#     proxy_list = []
#     a = open('./good_ip.txt', 'r')
#     for i in a.readlines():
#         proxy_list.append(i.strip())
#     return proxy_list
#
# proxy_list = get_url()
#
# for i in range(100):
#     proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
#     proxies = {'http': proxy_ip}
#     print(proxies)
# from get_url import header
#
# web_page = requests.get('http://www.dianping.com/member/703158841',headers = header, timeout=5)
# soup = BeautifulSoup(web_page.text, 'lxml')
# title = soup.title.text
# print(title)
# if title == '雪霁_2277的主页-会员-大众点评网':
#     print('shide')
#
# f = open('./good_ip.txt', 'a+')
# f.write('1')
# f.write('\n')

from get_url import header,user_index_distinct,user_information,shop_information,user_information_url,user_index,shop_index_distinct,shop_information_url

# user_url_distinct = [item['user_url_distinct'] for item in user_index_distinct.find()]
# user_url = [item['user_url'] for item in user_index.find()]
# #print(type(user_url_distinct))
# x = set(user_url_distinct)
# y = set(["http://www.dianping.com/member/179068091"])
# rest_of_urls = x-y
# print(len(user_url))
# print(len(user_url_distinct))
# print(type(rest_of_urls))
# for i in rest_of_urls:
#     print(i)




# f = open('./Proxies2016-05-24.txt','r')
# p = open('./1.txt','w')
# read = f.readlines()
# for i in read:
#     p.write('http://' + i)

# print(user_index_distinct.count())
# print(user_information_url.count())
# print(user_information.count())
# print(len(user_information_url.distinct('user_url')))
# print(len(user_information.distinct('user_ID')))
# print(shop_index_distinct.count())
# print(shop_information.count())
# print(len(shop_information.distinct('url')))

# store_list = []
# for i in user_information.find():
#     for j in i['score_list']:
#         store_list.append(j)
# print(len(set(store_list)))


