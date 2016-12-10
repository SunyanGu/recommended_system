import random

user_Map = {}
shop_Map = {}

with open('./map/RealRating.txt') as fp:
    fp_user = open('./map/usermap.txt','w')    #用户映射
    fp_shop = open('./map/shopmap.txt','w')    #商店映射
    fp_out = open('./map/bigMatrix.txt','w')   #用户商店打分映射

    for line in fp:
        line = line.strip()
        if line == '':
            continue
        tup = line.split('::::')
        raw_user = tup[0]
        raw_shop = tup[1]
        rate = float(tup[2])
        if raw_user not in user_Map:
            user_Map[raw_user] = len(user_Map.keys())
        user_id = user_Map[raw_user]
        if raw_shop not in shop_Map:
            shop_Map[raw_shop] = len(shop_Map.keys())
        shop_id = shop_Map[raw_shop]
        fp_out.write('{0}   {1}   {2}\n'.format(user_id,shop_id,rate))

    for raw_user,user_id in user_Map.items():
        fp_user.write('{0}  {1}\n'.format(raw_user,user_id))

    for raw_shop,shop_id in shop_Map.items():
        fp_shop.write('{0}  {1}\n'.format(raw_shop,shop_id))


