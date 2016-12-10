#coding: utf-8

from get_url import shop_information
import re
import time

# 删除用户过少的
# for i in shop_information.find({'average_cost':None,'environmental':None},{'average_cost':1,'environmental':1,'taste':1,'service':1,'rank_star':1,'coordinate':1,'summary':1,'dishTags':1,'label':1,'address':1}):
#     shop_information.remove({'_id':i['_id']})


def star2num(rank_star):
    if rank_star == '五星商户':
        star = 5
    elif rank_star == '准五星商户':
        star = 4.5
    elif rank_star == '四星商户':
        star = 4.5
    elif rank_star == '准四星商户':
        star = 4.5
    elif rank_star == '三星商户':
        star = 4.5
    elif rank_star == '准三星商户':
        star = 4.5
    elif rank_star == '二星商户':
        star = 4.5
    elif rank_star == '准二星商户':
        star = 4.5
    elif rank_star == '一星商户':
        star = 4.5
    elif rank_star == '准一星商户':
        star = 4.5
    elif rank_star == '该商户暂无星级':
        star = None
    else:
        star = 0
        print('chucuo')
        time.sleep(100)
    return star

#有些字符不好写，没办法
def data_to_text():
    f = open('./shop_data.txt','w')
    num = 0
    for i in shop_information.find({},{'_id':0,'comment_item':0}):
        #print(i)
        try:
            average_cost = i['average_cost']
            average_cost = re.findall('\d{1,}',average_cost,re.S)
            if average_cost == []:
                average_cost = [None]
            average_cost = average_cost[0]

            environmental = i['environmental']
            environmental = re.findall('\d\.\d',environmental,re.S)
            if environmental == []:
                environmental = [None]
            environmental = environmental[0]

            taste = i['taste']
            taste = re.findall('\d\.\d',taste,re.S)
            if taste == []:
                taste = [None]
            taste = taste[0]

            service = i['service']
            service = re.findall('\d\.\d', service, re.S)
            if service == []:
                service = [None]
            service = service[0]

            rank_star = i['rank_star']
            star = star2num(rank_star)



            coordinate = str(i['coordinate'][0]) + ',' + str(i['coordinate'][1])

            summary = ''
            summary_list = i['summary']
            if summary_list == [] or summary_list == None:
                summary_list = ['None']
            for j in range(len(summary_list)):
                summary =   summary_list[j] + ',' + summary
            summary = summary[:-1]

            dishTags = i['dishTags']
            if dishTags == '':
                dishTags = None

            label = i['label']
            if label == '':
                label = None

            address = i['address']

            shop_ID = i['url'].split('/')[4]
            #print(average_cost,environmental,taste,service,rank_star,coordinate,summary,dishTags,label,address,shop_ID)
            print(str(average_cost) + '::::' + str(environmental)+ '::::' + str(taste) + '::::' + str(service) + '::::' + str(star) + '::::' + str(coordinate) + '::::' + str(summary) + '::::' + str(dishTags) + '::::' + str(label) + '::::' + str(address) + '::::' + shop_ID)
            f.write(str(average_cost) + '::::' + str(environmental)+ '::::' + str(taste) + '::::' + str(service) + '::::' + str(star) + '::::' + str(coordinate) + '::::' + str(summary) + '::::' + str(dishTags) + '::::' + str(label) + '::::' + str(address) + '::::' + shop_ID)
            f.write('\n')
        except:
            num = num + 1
            print('error')
    print(num)
data_to_text()



