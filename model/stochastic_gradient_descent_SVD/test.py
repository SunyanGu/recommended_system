import random
import math
configureFile = 'svd.conf'
fi = open(configureFile, 'r')
line = fi.readline()
arr = line.split()
averageScore = float(arr[0].strip())
userNum = int(arr[1].strip())
itemNum = int(arr[2].strip())
factorNum = int(arr[3].strip())
learnRate = float(arr[4].strip())
regularization = float(arr[5].strip())
fi.close()
temp = math.sqrt(factorNum)


import numpy as np

# rarray=np.random.normal(0,1,size=(10,100000))
# # print(rarray)
# qi = np.array([[(0.1 * np.random.random() / temp) for j in range(factorNum)] for i in range(itemNum)])   #构造商店/因子矩阵
# pu = np.array([[(0.1 * np.random.random() / temp) for j in range(factorNum)] for i in range(userNum)])   #构造用户/因子矩阵
#
# #print(qi)

# from scipy import stats
# a = stats.norm(0,1).rvs(60000000).reshape(20000,3000)
# print(np.sum(a))
# #print(a)

