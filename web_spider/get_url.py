import pymongo
import requests
from bs4 import BeautifulSoup
import re
import time

Client = pymongo.MongoClient('localhost',27017)
dazhongdianping = Client['dazhongdianping']
url_goods = dazhongdianping['url_goods']
url_goods_distinct = dazhongdianping['url_goods_distinct']
store_information = dazhongdianping['store_information']
store_information_db = dazhongdianping['store_information_db']
user_index = dazhongdianping['user_index']
user_index_distinct = dazhongdianping['user_index_distinct']
user_information = dazhongdianping['user_information']
shop_information = dazhongdianping['shop_information']
user_information_url = dazhongdianping['user_information_url']
shop_index_distinct = dazhongdianping['shop_index_distinct']
shop_information_url = dazhongdianping['shop_information_url']
user_review_db = dazhongdianping['user_review_db']
chaloubuque = dazhongdianping['chaloubuque']
locate_url = {
    '秦淮区':'http://t.dianping.com/list/nanjing-category_1-region_3s11957',
    '江宁区':'http://t.dianping.com/list/nanjing-category_1-region_3s12019',
    '玄武区':'http://t.dianping.com/list/nanjing-category_1-region_3s11979',
    '建邺区':'http://t.dianping.com/list/nanjing-category_1-region_3s12002',
    '鼓楼区':'http://t.dianping.com/list/nanjing-category_1-region_3s11945',
    '浦口区':'http://t.dianping.com/list/nanjing-category_1-region_3s11937',
    '栖霞区':'http://t.dianping.com/list/nanjing-category_1-region_3s11928',
    '雨花台区': 'http://t.dianping.com/list/nanjing-category_1-region_3s11932',
    '六合区':'http://t.dianping.com/list/nanjing-category_1-region_3s11934',
    '下关区':'http://t.dianping.com/list/nanjing-category_1-region_3s12014',
    '高淳区':'http://t.dianping.com/list/nanjing-category_1-region_3s29756',
    '溧水区': 'http://t.dianping.com/list/nanjing-category_1-region_3s29755',
}
header = {
        'Cookie':'_hc.v="\"4c951dd7-85a4-4bc2-bc1f-014990ccd929.1463272954\""; dper=baea8cdf709d160e0c1145f05c22aa203c14f91f225c80d0a099ab966d8c5089; ua=18801583533; __utma=205923334.752221830.1463899345.1463899345.1463899651.2; __utmb=205923334.44.10.1463899651; __utmc=205923334; __utmz=205923334.1463899651.2.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; JSESSIONID=7111686C9873CCC5F2EB3BD606FAAF67; cy=5; cye=nanjing; ll=7fd06e815b796be3df069dec7836c3df; PHOENIX_ID=0a010493-154d753ddfd-b575cc; _tr.u=ZQgMJdekTvHQphmS; _tr.s=rytGUeQGeLnWVuXq',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'
}
def get_nanjing_item(url):
    url_list = []
    web_page = requests.get(url,headers=header, allow_redirects=False)
    time.sleep(4)
    soup = BeautifulSoup(web_page.text,'lxml')
    url_all = soup.select('.tg-floor-title ')
    for i in url_all:
        url_list.append('http://t.dianping.com'+ i.get('href'))
        url_good = 'http://t.dianping.com'+ i.get('href')
        url_goods.insert_one({'url':url_good})
        print(url_good)

def get_num(url):
    web_page = requests.get(url, headers=header, allow_redirects=False)
    time.sleep(4)
    soup = BeautifulSoup(web_page.text, 'lxml')
    #print(soup)
    number = soup.select('.tg-paginator-wrap')[0]
    #print(number)
    num = number.text.split()[6]
    return num

def get_all_url(url,num):
    url_all = [url + '?pageIndex={}'.format(str(i)) for i in range(num) ]
    for url_link in url_all:
        get_nanjing_item(url_link)
    print(url_all)

#
# if __name__ == "__main__":
#         for locate,url in locate_url.items():
#             #url_list = get_nanjing_item(url)
#             try:
#                 num = get_num(url)
#                 get_all_url(url,int(num))
#             except:
#                 print('have err')
#                 print(locate)



# print(url_goods.count())
# print(len(url_goods.distinct('url')))
# for i in url_goods.distinct('url'):
#     url_goods_distinct.insert_one({'url':i})
# print(url_goods_distinct.count())