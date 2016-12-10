

def average(trainDataFile):
    f = open(trainDataFile,'r')
    result = 0.0
    cnt = 0
    for i in f:
        cnt += 1
        score = i.split()[2].strip()
        result += float(score)
    return result/cnt

# def get_itemNum(trainDataFile):
#     f = open(trainDataFile, 'r')
#     item_list = []
#     for i in f:
#         item_list.append(i.split()[1].strip())
#     return len(set(item_list))
#
# def get_userNum(trainDataFile):
#     f = open(trainDataFile, 'r')
#     user_list = []
#     for i in f:
#         user_list.append(i.split()[0].strip())
#     return len(set(user_list))


def get_itemNum(trainDataFile):
    f = open(trainDataFile, 'r')
    max = 0
    for i in f:
        if int(i.split()[1].strip()) > max:
            max = int(i.split()[1].strip())
    return max

def get_userNum(trainDataFile):
    f = open(trainDataFile, 'r')
    max = 0
    for i in f:
        if int(i.split()[0].strip()) > max:
            max = int(i.split()[0].strip())
    return max

if __name__ == '__main__':
    trainDataFile = '../map/smallMatrix.txt'
    configureFile = 'svd.conf'
    conf_name = ['averageScore','userNum','itemNum','factorNum','learnRate','regularization']
    average = average(trainDataFile)
    userNum = get_userNum(trainDataFile)
    itemNum = get_itemNum(trainDataFile)
    print(userNum)
    print(itemNum)
    p = open(configureFile,'w')
    p.write('{}    {}    {}    {}    {}    {}\n'.format(average,userNum,itemNum,10,0.01,0.05))
    for line in conf_name:
        p.write(line)
        p.write('    ')
