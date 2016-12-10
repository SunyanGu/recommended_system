'''
# #用于获取用户的url
# from get_url import store_information,user_index,user_index_distinct
#
# user_index.remove()
# for i in store_information.find({},{'member_comment' :1,'_id':0}):
#     for information in i['member_comment']:
#         print(information['name'])
#         user_index.insert_one({'user_url':information['name'][0],'user_name':information['name'][1]})
#
# print(user_index.count())
#
# print(len(user_index.distinct('user_url')))
# print(user_index_distinct.count())
# for i in user_index.distinct('user_url'):
#     user_index_distinct.insert_one({'user_url_distinct':i})
'''
from get_url import header,user_index_distinct,user_information,shop_information,user_information_url,shop_index_distinct,shop_information_url,user_review_db
import requests
from bs4 import BeautifulSoup
import re
import time
import json
import random
from multiprocessing.dummy import Pool

# for i in user_index_distinct.find():
#     print(i)

class UserCrawler(object):
    def __init__(self):
        pass
        # self.user_name = None
        # self.user_contribute = None
        # self.user_birth = None
        # self.user_city = None
        # self.user_gender = None
        # self.user_label = None
        # self.user_follow = None
        # self.user_fans = None
        # self.score_list = []

    def get_member_information(self,url):
        #print(url)
        user_ID = url.split('/')[4]
        try:
            #print(type(user_ID))
            web_page = requests.get(url,proxies=proxies,timeout=5)
            time.sleep(random.random() * 2)
            soup = BeautifulSoup(web_page.text,'lxml')
            #print(soup)
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            user_names = soup.select('.tit .name')
            if len(user_names) > 0:
                user_name = user_names[0].text
            else:
                user_name = 'None'

            user_contributes = soup.find(id="J_col_exp")
            if len(user_contributes) > 0:
                user_contribute = user_contributes.text
            else:
                user_contribute = 0

            user_births = soup.select('.user-message')
            if len(user_births) > 0:
                user_birth = re.findall(r'\d{4}-\d{1,2}-\d{1,2}',str(user_births),re.S)
                if len(user_birth) > 0:
                    user_birth = user_birth[0]
                else:
                    user_birth = 'None'
            else:
                user_birth = 'None'

            user_citys = soup.select('.user-groun')
            if len(user_citys) > 0:
                user_genders = re.findall(r'<i class="(.*?)"></i>',str(user_citys),re.S)

                if len(user_citys[0].text) > 0:
                    user_city = user_citys[0].text
                else:
                    user_city = 'None'
                if len(user_genders) > 0:
                    user_gender = user_genders[0]
                else:
                    user_gender = 'None'

            else:
                user_city = 'None'
                user_gender = 'None'
            #print(user_citys)

            user_labels = soup.find(id="J_usertag")
            user_label = re.findall(r'<em class="user-tag" id="-1">(.*?)</em>',str(user_labels),re.S)
            if len(user_label) == 0:
                user_label = None
            #print(user_ID)
            user_follow = self.member_follows(user_ID)
            user_fans = self.member_fans(user_ID)
            score_list = self.member_scored(user_ID)
            #用户关注，用户粉丝
            '''
            member_follows(user_ID)
            member_fans(user_ID)
            member_reviews(user_ID)
            member_checkin(user_ID)
            '''
            #print(self.user_name,self.user_contribute,self.user_birth,self.user_city,self.user_gender,self.user_label,self.user_follow,self.user_fans,self.score_list)
            data = {'user_name':user_name,'user_contribute':user_contribute,'user_birth':user_birth,\
                    'user_city':user_city,'user_gender':user_gender,'user_label':user_label,'user_ID':user_ID,\
                    'user_follow':user_follow,'user_fans':user_fans,'score_list':score_list}
            user_information.insert_one(data)
            print(data)

        except:
            print('rubbish')
            pass


    #人数和人物
    def member_follows(self,user_ID):
        #该用户关注的人
        member_follow_list = []
        num = self.member_follows_number(user_ID)
        if num == 0:
            temp_url_list = ['http://www.dianping.com/member/{}/follows'.format(user_ID)]
        else:
            temp_url_list = ['http://www.dianping.com/member/{}/follows?pg={}'.format(user_ID,i) for i in range(1,num+1)]
        try:
            for temp_url in temp_url_list:
                web_page = requests.get(temp_url,proxies=proxies,timeout=5)
                time.sleep(random.random() * 2)
                soup = BeautifulSoup(web_page.text,'lxml')
                if soup.title.text == '提示_大众点评网':
                    print('被屏蔽')
                    time.sleep(300)

                member_informations = soup.select('.modebox  .pic-txt .tit')
                #print(member_informations)
                if len(member_informations) > 0:
                    for member_information in member_informations:
                        member_name = member_information.text.strip()
                        member_ID = re.findall(r'<a class="J_card" href="/member/(.*?)"',str(member_information),re.S)
                        if len(member_ID) > 0:
                            member_ID =  member_ID[0]
                            member_url = 'http://www.dianping.com/member/{}'.format(member_ID)
                        else:
                            member_url = None
                            member_ID = None

                        member_follow_dic = {'member_name': member_name, 'member_url': member_url,'member_ID':member_ID}
                        member_follow_list.append(member_follow_dic)
                else:
                    #print(len(member_follow_list))
                    return member_follow_list
            #print(len(member_follow_list))
            return member_follow_list
        except:
            return None



    def member_follows_number(self,user_ID):
        temp_url = 'http://www.dianping.com/member/{}/follows'.format(user_ID)
        try:
            web_page = requests.get(temp_url,proxies=proxies,timeout=5)
            time.sleep(random.random() * 2)
            soup = BeautifulSoup(web_page.text, 'lxml')
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            page_nums = soup.select('.pages-num')
            # print(page_nums)
            if len(page_nums) > 0:
                page_num = page_nums[0]
                page_num = page_num.text
                page_num = re.findall(r'\d+', page_num, re.S)
                # print(page_num)
                max_num = self.get_max(page_num)
                #print(max_num)
                return max_num
            else:
                return 0
        except:
            return 0

    def get_max(self,number_list):
        for i in range(len(number_list)):
            number_list[i] = int(number_list[i])
        max = number_list[0]
        for i in range(len(number_list)):
            if max < number_list[i]:
                max = number_list[i]
        return max

    def member_fans(self,user_ID):
        # 关注该用户的人
        fans_follow_list = []
        num = self.member_fans_number(user_ID)
        #print(num)
        if num == 0:
            temp_url_list = ['http://www.dianping.com/member/{}/fans'.format(user_ID)]
        else:
            temp_url_list = ['http://www.dianping.com/member/{}/fans?pg={}'.format(user_ID, i) for i in range(1, num + 1)]
        try:
            for temp_url in temp_url_list:
                web_page = requests.get(temp_url,proxies=proxies,timeout=5)
                time.sleep(random.random() * 2)
                soup = BeautifulSoup(web_page.text, 'lxml')
                if soup.title.text == '提示_大众点评网':
                    print('被屏蔽')
                    time.sleep(300)
                member_informations = soup.select('.modebox  .pic-txt .tit')
                # print(member_informations)
                if len(member_informations) > 0:
                    for fans_information in member_informations:
                        fans_name = fans_information.text.strip()
                        fans_ID = re.findall(r'<a class="J_card" href="/member/(.*?)"', str(fans_information), re.S)
                        if len(fans_ID) > 0:
                            fans_ID = fans_ID[0]
                            fans_url = 'http://www.dianping.com/fans/{}'.format(fans_ID)
                        else:
                            fans_url = None
                            fans_ID = None

                        fans_follow_dic = {'fans_name': fans_name, 'fans_url': fans_url, 'fans_ID': fans_ID}
                        fans_follow_list.append(fans_follow_dic)
                else:
                    # print(len(fans_follow_list))
                    return fans_follow_list
            #print(len(fans_follow_list))
            return fans_follow_list
        except:
            return None

    def member_fans_number(self,user_ID):
        temp_url = 'http://www.dianping.com/member/{}/fans'.format(user_ID)
        try:
            web_page = requests.get(temp_url,proxies=proxies,timeout=5)
            time.sleep(random.random() * 2)
            soup = BeautifulSoup(web_page.text, 'lxml')
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            page_nums = soup.select('.pages-num')
            # print(page_nums)
            if len(page_nums) > 0:
                page_num = page_nums[0]
                page_num = page_num.text
                page_num = re.findall(r'\d+', page_num, re.S)
                # print(page_num)
                max_num = self.get_max(page_num)
                #print(max_num)
                return max_num
            else:
                return 0
        except:
            return 0



    def member_scored_number(self,user_ID):
        temp_url = 'http://www.dianping.com/member/{}/reviews?reviewCityId=5&reviewShopType=10'.format(user_ID)
        try:
            web_page = requests.get(temp_url,proxies=proxies,timeout=5)
            time.sleep(random.random() * 2)
            soup = BeautifulSoup(web_page.text, 'lxml')
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            page_nums = soup.select('.pages-num')
            # print(page_nums)
            if len(page_nums) > 0:
                page_num = page_nums[0]
                page_num = page_num.text
                page_num = re.findall(r'\d+', page_num, re.S)
                # print(page_num)
                max_num = self.get_max(page_num)
                # print(max_num)
                return max_num
            else:
                return 0
        except:
            return 0

    def member_scored(self,user_ID):
        user_url = 'http://www.dianping.com/member/' + str(user_ID)
        num = self.member_scored_number(user_ID)
        if num == 0:
            num = 1
        score_list = []
        temp_urls = [
            'http://www.dianping.com/member/{}/reviews?pg={}&reviewCityId=5&reviewShopType=10'.format(user_ID, i) for i
            in range(1, num + 1)]
        star_list = []
        comment_list = []
        try:
            for temp_url in temp_urls:
                web_page = requests.get(temp_url, proxies=proxies, timeout=5)
                time.sleep(random.random() * 2)
                soup = BeautifulSoup(web_page.text, 'lxml')
                if soup.title.text == '提示_大众点评网':
                    print('被屏蔽')
                    time.sleep(300)
                scored_list = soup.select('.modebox  .pic-txt .txt .tit')
                if len(scored_list) > 0:
                    for scored in scored_list:
                        score = re.findall(r'href="(.*?)"', str(scored), re.S)
                        if score == []:
                            score = None
                        else:
                            score = score[0]
                        score_list.append(score)
                adds = soup.select('.modebox  .pic-txt .txt .txt-c')
                # print(adds)
                if len(adds) > 0:
                    for add in adds:
                        # print(add)
                        star = re.findall(r'item-rank-rst irr-star(.*?)"', str(add), re.S)
                        if star == []:
                            star = None
                        else:
                            star = star[0]
                        star_list.append(star)
                    for comm in adds:
                        # print(add)
                        comment = re.findall(r'<div class="mode-tc comm-entry">(.*?)</div>', str(comm), re.S)
                        if comment == []:
                            comment = None
                        else:
                            comment = comment[0]
                        comment_list.append(comment)
            user_review = zip(star_list, comment_list, score_list)
            #print(user_review)
            for i in user_review:
                user_review_db.insert_one({'star': i[0], 'comment': i[1], 'shop_url': i[2], 'user_url': user_url})
                print(i[0], i[1], i[2])
            print(user_url)
            #return score_list
        except:
            print('rubb')
            pass
        #return score_list



    #记录用户签到的地点，没实际用处，删了
    # def member_checkin(self):
    #     #把店名称和经纬度搞出来就行
    #     locate_list = []
    #     temp_url = 'http://www.dianping.com/member/{}/checkin'.format(self.user_ID)
    #     try:
    #         web_page = requests.get(temp_url, headers=header)
    #         time.sleep(1)
    #         soup = BeautifulSoup(web_page.text, 'lxml')
    #         locations = soup.select('.sign-list')
    #         if len(locations) > 0:
    #             location = locations[0]
    #             location = re.findall(r'<span class="time">(.*?)</span>\n<a href="/shop/(.*?)" ',str(location), re.S)
    #             for loc in location:
    #                 coordinate = self.base_info(loc[1])
    #                 locate_dic = {'locate_time':loc[0],'locate_shop':loc[1],'coordinate':coordinate}
    #                 locate_list.append(locate_dic)
    #             print(locate_list)
    #             # print(max_num)
    #             return locate_list
    #         else:
    #             return None
    #     except:
    #         pass
    #
    # def base_info(self, shop_ID):
    #     url = 'http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP&shopId={}'.format(shop_ID)
    #     try:
    #         web_page = requests.get(url, headers=header)
    #         time.sleep(1)
    #         soup = BeautifulSoup(web_page.text, 'lxml').text
    #         shop_item = json.loads(soup)
    #         glat = shop_item['msg']['shopInfo']['glat']
    #         glng = shop_item['msg']['shopInfo']['glng']
    #
    #     except:
    #         glat = None
    #         glng = None
    #     coordinate = [glng, glat]
    #     return  coordinate


class StoreCrawler(object):
    def __init__(self):
        pass
        # self.shop_name = None
        # self.rank_star = None
        # self.average_cost = None
        # self.taste = None
        # self.environmental  = None
        # self.service = None
        # self.address = ''
        # self.label = None
        # self.coordinate = None
        # self.summary = []
        # self.comment_item = []
        # self.dishTags = None


    def shop_information(self,url):
        shop_ID = url.split('/')[4]
        address_late = ''
        summary_late = []
        comment_item_late = []

        try:
            web_page = requests.get(url,headers= header, proxies=proxies,timeout=5)
            time.sleep(random.random() * 5)
            soup = BeautifulSoup(web_page.text, 'lxml')
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            shop_names = soup.select('.breadcrumb span')
            if len(shop_names) > 0:
                shop_name = shop_names[0].text
            else:
                shop_name = 'None'
            #print(self.shop_name)
            rank_stars = soup.select('.brief-info .mid-rank-stars')
            if len(rank_stars) > 0:
                #print(rank_stars)
                rank_star = re.findall(r'title="(.*?)"',str(rank_stars[0]),re.S)
                if len(rank_star) > 0:
                    rank_star = rank_star[0]
                else:
                    rank_star = None
            else:
                rank_star = None
            #print(self.rank_star)
            base_items = soup.select('.brief-info .item')
            #print(base_items)
            if len(base_items) == 5:
                average_cost = base_items[1].text
                taste = base_items[2].text
                environmental = base_items[3].text
                service = base_items[4].text
            else:
                average_cost = None
                taste = None
                environmental = None
                service = None
            #print(self.average_cost, self.taste, self.environmental, self.service)
            dishTags,label,coordinate = self.base_info(shop_ID)
            #print(self.label,self.coordinate)

            address = soup.select('.breadcrumb')
            if len(address) > 0:
                address = address[0].text.split()
            address_late = address_late.join(address)
            #print(self.address)

            summarys = soup.select('.comment-condition .good')
            if len(summarys) > 0:
                for summary in summarys:
                    #print(summary.text)
                    summary_late.append(summary.text)
            else:
                summary_late = None

            #comment_item_late = self.get_comment(shop_ID)
            comment_item_late = []

            data = {'shop_name':shop_name,'rank_star':rank_star,'average_cost':average_cost,'taste':taste,\
                    'environmental':environmental,'service':service,'label':label,'coordinate':coordinate,\
                    'address':address_late,'summary':summary_late,'comment_item':comment_item_late,
                    'dishTags':dishTags,'url':url}
            print(data)
            shop_information_url.insert_one({'url':url})
            shop_information.insert_one(data)

        except:
            pass


    def base_info(self,shop_ID):
        url = 'http://www.dianping.com/ajax/json/shop/wizard/BasicHideInfoAjaxFP&shopId={}'.format(shop_ID)
        try:
            web_page = requests.get(url, headers= header,proxies=proxies,timeout=5)
            time.sleep(random.random() * 5)
            soup = BeautifulSoup(web_page.text, 'lxml')
            shop_item = json.loads(soup.text)
            dishTags = shop_item['msg']['shopInfo']['dishTags']
            label = shop_item['msg']['shopInfo']['shopTags']
            glat = shop_item['msg']['shopInfo']['glat']
            glng = shop_item['msg']['shopInfo']['glng']

        except:
            dishTags = None
            label = None
            glat = None
            glng = None
        coordinate = [glng,glat]
        return dishTags,label,coordinate

    def is_restaurant(self,url):
        try:
            web_page = requests.get(url,headers= header, proxies=proxies,timeout=5)
            time.sleep(random.random() * 5)
            soup = BeautifulSoup(web_page.text, 'lxml')
            #print(soup.title.text)
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            _is_restaurants = soup.select('.current-category')
            if len(_is_restaurants) > 0:
                _is_restaurant = _is_restaurants[0].text
            else:
                _is_restaurant = None
            if _is_restaurant == '美食':
                return True
            else:
                return False
        except:
            return False

    def get_comment(self,shop_ID):
        comment_item_list = []
        num = self.member_comments_number(shop_ID)
        #print(num)
        if num == 0:
            temp_url_list = ['http://www.dianping.com/shop/{}/review_more'.format(shop_ID)]
        else:
            temp_url_list = ['http://www.dianping.com/shop/{}/review_more?pageno={}'.format(shop_ID, i) for i in range(1, num + 1)]

        try:
            for url in temp_url_list:
                web_page = requests.get(url, headers= header,proxies=proxies,timeout=5)
                time.sleep(random.random() * 5)
                soup = BeautifulSoup(web_page.text, 'lxml')
                if soup.title.text == '提示_大众点评网':
                    print('被屏蔽')
                    time.sleep(300)
                items = soup.select('.comment-list')
                #print(items)
                if len(items) > 0:
                    item = re.findall(r'<a href="/member/(.*?)" target="_blank" title="">(.*?)</a></p>\n(.*?)\n<span class="rst">(.*?)</em></span>\n<span class="rst">(.*?)</em></span>\n<span class="rst">(.*?)</em></span>\n</div>\n</div>\n<div class="comment-txt">\n<div class="J_brief-cont">\n(.*?)</div>',str(items[0]),re.S)
                    for i in item:
                        if len(i) > 0:
                            user_ID = i[0]
                            user_name = i[1]
                            user_taste = re.findall(r'(.*?)<em',i[3],re.S)[0]
                            user_envirnoment = re.findall(r'(.*?)<em',i[4],re.S)[0]
                            user_service = re.findall(r'(.*?)<em',i[5],re.S)[0]
                            user_comment = i[6].strip()
                            #print(user_comment)
                        else:
                            user_ID = None
                            user_name = None
                            user_taste = None
                            user_envirnoment = None
                            user_service = None
                            user_comment = None
                        #print(user_ID, user_name, user_taste, user_envirnoment, user_service,user_comment)
                        comment_item = {'user_ID':user_ID,'user_name':user_name,'user_score':user_taste + '|' + user_envirnoment + '|' + user_service,'user_comment':user_comment}
                        comment_item_list.append(comment_item)
        except:
            comment_item_list = None
        #print(comment_item_list)
        return comment_item_list

    def member_comments_number(self,shop_ID):
        temp_url = 'http://www.dianping.com/shop/{}/review_more'.format(shop_ID)
        try:
            web_page = requests.get(temp_url, headers= header,proxies=proxies,timeout=5)
            time.sleep(random.random() * 5)
            soup = BeautifulSoup(web_page.text, 'lxml')
            if soup.title.text == '提示_大众点评网':
                print('被屏蔽')
                time.sleep(300)
            page_nums = soup.select('.Pages')

            if len(page_nums) > 0:
                page_num = page_nums[0]
                page_num = page_num.text
                page_num = re.findall(r'\d+', page_num, re.S)
                #print(page_num)
                if len(page_num) == 0:
                    return 0
                max_num = self.get_max(page_num)
                return max_num
            else:
                return 0
        except:
            pass

    def get_max(self, number_list):
        for i in range(len(number_list)):
            number_list[i] = int(number_list[i])
        max = number_list[0]
        for i in range(len(number_list)):
            if max < number_list[i]:
                max = number_list[i]
        return max

    def shop_go(self):

        # print(proxies)
        pool = Pool()
        # 多进程爬取
        pool.map(self.shop_information, rest_of_urls)
        pool.close()
        pool.join()


def print_url(proxy_list):
    for i in proxy_list:
        time.sleep(0.1)
        print(i)

def get_url():
    proxy_list = []
    a = open('./good_ip.txt', 'r')
    for i in a.readlines():
        proxy_list.append(i.strip())
    return proxy_list

def is_good(proxies):
    try:
        web_page = requests.get('http://www.dianping.com/member/703158841', proxies=proxies,timeout=5)
        soup = BeautifulSoup(web_page.text, 'lxml')
        #print(soup)
        title = soup.title.text
        #print(title)
        if title == '雪霁_2277的主页-会员-大众点评网':
            url_item = proxies['http']
            # print(url_item)
            return url_item
        else:
            # print(soup)
            return 0
    except:
        print('rubbish')
        return 0
#主函数
# if __name__ == "__main__":
#       #清空数据库
#     user_information.remove()
#     store_link = []
#     User = UserCrawler()
#     for i in user_index_distinct.find():
#         store_link.append(i['user_url_distinct'])
#       #初始化进程池
#     pool = Pool()
#       #多进程爬取
#     pool.map(User.get_member_information,store_link)
#     pool.close()
#     pool.join()

if __name__ == "__main__":


    # proxy_list = get_url()
    # user_information_url_list = ['http://www.dianping.com/member/' + item['user_ID'] for item in user_information.find()]
    # user_index_distinct_list = [item['user_url_distinct'] for item in user_index_distinct.find()]
    # x = set(user_index_distinct_list)
    # y = set(user_information_url_list)
    # print(len(x))
    # print(len(y))
    # rest_of_urls = x - y
    # print(len(rest_of_urls))
    # User = UserCrawler()
    # #for i in rest_of_urls:
    # proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # proxies = {'http': proxy_ip}
    # pool = Pool()
    # # 多进程爬取
    # pool.map(User.get_member_information, rest_of_urls)
    # pool.close()
    # pool.join()


    # proxy_list = get_url()
    # shop_index_distinct = [item['shop_url'] for item in user_review_db.find()]
    # shop_information_list = [item['url'] for item in shop_information.find()]
    # x = set(shop_index_distinct)
    # y = set(shop_information_list)
    # rest_of_urls = (x | y) - y
    # print(len(rest_of_urls))
    # #print(len(y))
    # StoreCrawler = StoreCrawler()
    # # for i in rest_of_urls:
    # #     proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # #     proxies = {'http': proxy_ip}
    # #     while is_good(proxies) == 0:
    # #         #print(len(proxy_list))
    # #         proxy_list.remove(proxy_ip)
    # #         if len(proxy_list) == 0:
    # #             print('没有IP了')
    # #             time.sleep(100000)
    # #         proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # #         proxies = {'http': proxy_ip}
    # #     #print(proxies)
    # proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # proxies = {'http': proxy_ip}
    # pool = Pool()
    # # 多进程爬取
    # pool.map(StoreCrawler.shop_information, rest_of_urls)
    # pool.close()
    # pool.join()

    # ID_list = []
    # proxy_list = get_url()
    # user_index = [item['user_url_distinct'] for item in user_index_distinct.find()]
    # user_url = [item['user_url'] for item in user_review_db.find()]
    # x = set(user_index)
    # y = set(user_url)
    # rest_of_urls = x - y
    # print(len(y))
    # print(len(x))
    # print(len(rest_of_urls))
    # User = UserCrawler()
    # for i in rest_of_urls:
    #     ID_list.append(i.split('/')[4])
    #     # print(proxies)
    #     # print(proxies)
    # proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # proxies = {'http': proxy_ip}
    # # while is_good(proxies) == 0:
    # #     # print(len(proxy_list))
    # #     proxy_list.remove(proxy_ip)
    # #     if len(proxy_list) == 0:
    # #         print('没有IP了')
    # #         time.sleep(100000)
    # #     proxy_ip = random.choice(proxy_list)  # 随机获取代理ip
    # #     proxies = {'http': proxy_ip}
    # #print(ID_list)
    # pool = Pool()
    # # 多进程爬取
    # pool.map(User.member_scored, ID_list)
    # pool.close()
    # pool.join()

    # StoreCrawler = StoreCrawler()
    # StoreCrawler.shop_information('http://www.dianping.com/shop/9973213')
    pass
