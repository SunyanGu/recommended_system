trainDataFile = '../map/smallMatrix.txt'
usermap = '../map/usermap.txt'
relation = '../map/RealRelation.txt'

f1 = open(trainDataFile,'r')
f2 = open(usermap,'r')
f3 = open(relation,'r')
user_list = []
user_list2 = []
user_list3 = []
for i in f1:
    a = i.strip().split()
    user_list.append(a[0])
print(len(set(user_list)))

for j in f3:
    a = j.strip().split('::::')
    #print(a)
    user_list2.append(a[0])
    user_list3.append(a[1])

print(len(set(user_list2)))
print(len(set(user_list3)))
print(len(set(user_list2+user_list3)))
#print(user_list2+user_list3)




