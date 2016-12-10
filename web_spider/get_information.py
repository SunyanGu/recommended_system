import pymongo
import requests
from bs4 import BeautifulSoup
import re
import time
from get_url import url_goods_distinct,header,store_information_db,store_information
import json
from multiprocessing.dummy import Pool



def group_purchase_comment(item_ID):
    review_list = []
    score = 0
    num = group_purchase_num(item_ID)
    if num == 0:
        num = 1
    group_purchase_url_all = ['http://t.dianping.com/ajax/detailDealRate?dealGroupId={}&pageNo={}'.format(item_ID,str(i)) for i in range(num)]
    for url in group_purchase_url_all:
        try:
            web_page = requests.get(url,headers = header)
            time.sleep(1)
            soup = BeautifulSoup(web_page.text,'lxml')
            scores = soup.select('.c-total')
            if len(scores) > 0:
                score = scores[0]
                score = score.text.strip()
            else:
                score = 0
                pass
            comments = soup.select('li.Fix')
            if len(comments) > 0:
                for comment in comments:
                    date = re.findall(r'\d{4}-\d{2}-\d{2}',str(comment),re.S)
                    if len(date) == 0:
                        date = ['None']
                    #date = re.findall('<span class="date">(.*?)</span><span class="location"></span>',str(comment),re.S)
                    review = re.findall(r'<div class="J_brief_cont_full ">(.*?)</div>',str(comment),re.S)
                    if len(review) == 0:
                        review = ['None']
                    comment_data = {'date':date[0],'review':review[0].strip()}
                    #print(comment_data)
                    review_list.append(comment_data)
            else:
                pass
        except:
            pass
    # print(score)
    # print(review_list)
    return score,review_list

def group_purchase_num(item_ID):
    group_purchase_url = 'http://t.dianping.com/ajax/detailDealRate?dealGroupId={}'.format(item_ID)
    try:
        web_page = requests.get(group_purchase_url,headers = header)
        time.sleep(1)
        soup = BeautifulSoup(web_page.text,'lxml')
        page_nums = soup.select('.Pages')
        if len(page_nums) > 0:
            page_num = page_nums[0]
            page_num = page_num.text
            page_num = re.findall(r'\d+',page_num,re.S)
            #print(page_num)
            max_num = get_max(page_num)
            #print(max_num)
            return max_num
        else:
            return 0
    except:
        pass


def get_max(number_list):
    for i in range(len(number_list)):
        number_list[i] = int(number_list[i])
    max = number_list[0]
    for i in range(len(number_list)):
        if max < number_list[i]:
            max = number_list[i]
    return max

def get_shop_detail(item_ID):
    url = 'http://t.dianping.com/ajax/dealGroupShopDetail?dealGroupId={}&action=shops'.format(item_ID)
    try:
        web_page = requests.get(url,headers = header)
        time.sleep(1)
        soup = BeautifulSoup(web_page.text,'lxml').text
    except:
        soup=''
    try:
        value = json.loads(soup)
        address = value['msg']['shops'][0]['address']
        shopName = value['msg']['shops'][0]['shopName']
        shopId = value['msg']['shops'][0]['shopId']

    except:
        print('json')
        address = None
        shopName = None
        shopId = None
    data = {'address': address, 'shopName': shopName, 'shopId': shopId}
    #print(data)
    return data


def get_member_comment(item_ID):
    review_list = []
    num = member_comment_num(item_ID)
    if num == 0:
        num = 1
    member_comment_url_all = ['http://t.dianping.com/ajax/dealbody/{}/2?&page={}&version=new'.format(item_ID,str(i)) for i in range(1,num+1)]
    for url in member_comment_url_all:
        try:
            web_page = requests.get(url,headers = header)
            time.sleep(1)
            soup = BeautifulSoup(web_page.text,'lxml')
            #print(soup)
            items = soup.select('.site-item')
            #print(items)
            if len(items) > 0:
                for item in items:
                    name = re.findall(r'<p class="name"><a href="(.*?)" target="_blank" title="">(.*?)</a></p>', str(item), re.S)
                    # print(name)
                    # print(len(name))
                    if len(name) == 0:
                        name = ['None']
                    # date = re.findall('<span class="date">(.*?)</span><span class="location"></span>',str(comment),re.S)
                    score = re.findall(r'<span class="rst">(.*?)<em class="col-exp">', str(item), re.S)
                    if len(score) != 3:
                        score = ['None']
                    #print(score)
                    review = re.findall(r'<div class="J_brief_cont_full ">(.*?)</div>', str(item), re.S)
                    if len(review) == 0:
                        review = ['None']
                    comment_time = re.findall(r'<span class="time">(.*?)</span>', str(item), re.S)
                    if len(comment_time) == 0:
                        comment_time = ['None']
                    #print(comment_time)
                    comment_data = {'name': name[0], 'review': review[0].strip(),'score':score,'comment_time':comment_time[0]}
                    # print(comment_data)
                    review_list.append(comment_data)
            else:
                pass
        except:
            pass

    return review_list



def member_comment_num(item_ID):
    group_purchase_url = 'http://t.dianping.com/ajax/dealbody/{}/2?'.format(item_ID)
    try:
        web_page = requests.get(group_purchase_url,headers = header)
        time.sleep(2)
        soup = BeautifulSoup(web_page.text,'lxml')
        page_nums = soup.select('.Pages')
        #print(page_nums)
        if len(page_nums) > 0:
            page_num = page_nums[0]
            page_num = page_num.text
            page_num = re.findall(r'\d+',page_num,re.S)
            #print(page_num)
            max_num = get_max(page_num)
            return max_num
        else:
            return 0
    except:
        pass

def get_store_information(url):
    item_ID = url.split('/')[4]
    try:
        web_page = requests.get(url, headers=header)
        time.sleep(1)
        soup = BeautifulSoup(web_page.text, 'lxml')
        titles = soup.select('.title')
        if len(titles) > 0:
            title = titles[0].text.strip()
            # print(title)
            # area = title[0]
            # store_name = title[1]
            # title = title[0] + ' ' + title[1]
            # print(area)
            # print(title)
            # print(store_name)
        else:
            title = 'None'
            # area = 'None'
            # store_name = 'None'
            pass

        notes = soup.select('.purchase-notes')
        if len(notes) > 0:
            note = notes[0]
            note = note.text.strip()
            #print(note)
        else:
            note = 'None'
            pass

        current_prices = soup.select('.price-display')
        # print(current_prices) #还有折扣，原价等，以后如果需要爬取
        discounts = soup.select('.price-discount')
        # print(discounts)
        original_prices = soup.select('.price-original')
        # print(original_prices)
        if len(current_prices) > 0 and len(discounts) > 0 and len(original_prices) > 0:
            current_price = current_prices[0]
            current_price = current_price.text
            # print(current_price)
            discount = discounts[0]
            discount = discount.text
            # print(discount)
            original_price = original_prices[0]
            original_price = original_price.text.split()
            original_price = original_price[1]
            # print(original_price)
        else:
            current_price = 'None'
            discount = 'None'
            original_price = 'None'
            pass

        score, purchase_comment = group_purchase_comment(item_ID)
        detail_data = get_shop_detail(item_ID)
        member_comment = get_member_comment(item_ID)
        data = {'title': title, 'note': note,
                'current_price': current_price, 'discounts': discount, 'original_price': original_price,
                'score':score,'purchase_comment':purchase_comment,
                'detail_data':detail_data,'member_comment':member_comment
                }
        store_information.insert_one(data)
        print(data)
    except:
        pass

# for i in url_goods_distinct.find():
#
#get_store_information('http://t.dianping.com/deal/18394420')
# group_purchase_comment(13621353)
# get_shop_detail(13621353)
# print(len(get_member_comment(18394420)))
# print(get_member_comment(18394420))




# #主函数
# if __name__ == "__main__":
#       #清空数据库
#     store_information.remove()
#     store_link = []
#     for i in url_goods_distinct.find():
#         store_link.append(i['url'])
#       #初始化进程池
#     pool = Pool()
#       #多进程爬取
#     pool.map(get_store_information,store_link)
#     pool.close()
#     pool.join()



# print(url_goods_distinct.count())
# print(store_information.count())