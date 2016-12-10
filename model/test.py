f = open('../data/data/RealRelation.txt', 'r')
p = open('../data/data/rating.txt', 'r')
q = open('../data/data/RealRating.txt', 'w')

relation_data = f.readlines()
item_data = p.readlines()

relation_list = []
relation_list1 = []
relation_list2 = []
item_list = []

num = 0

for i in relation_data:
    relation_list.append(i.split('::::')[0].strip())
    relation_list1.append(i.split('::::')[1].strip())
    relation_list2.append(i.split('::::')[0].strip())
    relation_list2.append(i.split('::::')[1].strip())

for j in item_data:
    item_list.append(j.split('::::')[0].strip())
rate = set(item_list) & set(relation_list2)

for k in item_data:
    if k.split('::::')[0] in rate:
        print(k)
        q.write(str(k))
        num = num + 1
        print(num)



print(len(set(relation_list)))
print(len(set(relation_list1)))
print(len(set(relation_list2)))
print(len(set(item_list)))

print(len(set(relation_list) & set(relation_list1)))
print(len(set(item_list) & set(relation_list2)))
# print(relation_list)
# print(relation_list1)