import math
import pickle
import time
import numpy as np

#calculate the overall average
def average(filename):
    fi = open(filename,'r')
    result = 0.0
    cnt = 0
    for line in fi:
        cnt += 1
        arr = line.split()
        result += int(arr[2].strip())
    return result/cnt

def InterProduct(v1,v2):
    result = 0
    for i in range(len(v1)):
        result += v1[i] * v2[i]
    return result

def PredictScore(pu,qi):
    pScore = InterProduct(pu,qi)
    if pScore < 1:
        pScore = 1
    elif pScore > 5:
        pScore = 5
    return pScore

#def SVD(configureFile, testDataFile, trainDataFile, modelSaveFile):
def SVD(configureFile,trainDataFile,modelSaveFile):
    #get the configure
    fi = open(configureFile,'r')
    line = fi.readline()
    arr = line.split()
    userNum = int(arr[1].strip())
    itemNum = int(arr[2].strip())
    factorNum = int(arr[3].strip())
    learnRate = float(arr[4].strip())
    regularization = float(arr[5].strip())
    fi.close()

    #temp = math.sqrt(factorNum)
    # qi = np.array([[(0.1 * np.random.random() / temp) for j in range(factorNum)] for i in range(itemNum)])   #构造商店/因子矩阵
    # pu = np.array([[(0.1 * np.random.random() / temp) for j in range(factorNum)] for i in range(userNum)])   #构造用户/因子矩阵

    qi = np.random.normal(0,1,size=(itemNum,factorNum))  # 构造商店/因子矩阵
    pu = np.random.normal(0,1,size=(userNum,factorNum))  # 构造用户/因子矩阵
    pq = np.random.normal(0,1,size=(userNum,itemNum))

    sigma = np.var(pq)
    sigmaU = np.var(pu)
    sigmaI = np.var(qi)

    regU = sigma/sigmaU
    regI = sigma/sigmaI

    print('initinalization end\nstart training\n')
    #train model
    preRmse = 100000000.0



    for step in range(50):
        fi = open(trainDataFile,'r')
        for line in fi:
            arr = line.split()
            uid = int(arr[0].strip()) - 1
            iid = int(arr[1].strip()) - 1
            # uid = int(arr[0].strip())
            # iid = int(arr[1].strip())
            score = float(arr[2].strip())
            prediction = PredictScore(pu[uid],qi[iid])   #预估分数
            eui = score - prediction    #实际分数和预测评分的差值
            for k in range(factorNum):
                temp = pu[uid][k]
                pu[uid][k] += learnRate * (eui * qi[iid][k] - regU * pu[uid][k])
                qi[iid][k] += learnRate * (eui * temp -regI * qi[iid][k])

        fi.close()
        #learnRate *= 0.9
        curRmse = Validate(trainDataFile,pu,qi)
        print("test_RMSE in step %d: %f" %(step, curRmse))
        if curRmse >= preRmse:
          break
        else:
          preRmse = curRmse

    #write the model to files
    fo = open(modelSaveFile,'wb')

    pickle.dump(qi, fo, True)
    pickle.dump(pu, fo, True)
    fo.close()
    print('model generation over')

#validate the model
def Validate(testDataFile,pu,qi):
    cnt = 0
    rmse = 0.0
    fi = open(testDataFile,'r')
    for line in fi:
        cnt += 1
        arr = line.split()
        uid = int(arr[0].strip()) - 1
        iid = int(arr[1].strip()) - 1
        # uid = int(arr[0].strip())
        # iid = int(arr[1].strip())
        pScore = PredictScore(pu[uid],qi[iid])

        tScore = float(arr[2].strip())
        rmse += (tScore - pScore) * (tScore - pScore)
    fi.close()
    return math.sqrt(rmse/cnt)

#use the model to make predict
def predict(modelSaveFile,testDataFile,resultSaveFile):
    #get model
    fi = open(modelSaveFile,'rb')
    qi = pickle.load(fi)
    pu = pickle.load(fi)
    fi.close()

    #predict
    fi = open(testDataFile,'r')
    fo = open(resultSaveFile,'w')
    for line in fi:
        arr = line.split()
        uid = int(arr[0].strip()) - 1
        iid = int(arr[1].strip()) - 1
        # uid = int(arr[0].strip())
        # iid = int(arr[1].strip())
        pScore = PredictScore(pu[uid],qi[iid])
        fo.write('{}    {}    {}'.format(arr[0],arr[1],pScore))
        fo.write('\n')
    fi.close()
    fo.close()
    result = test_rmse(testDataFile,resultSaveFile)
    print('test_RMSE is %f'%result)
    print('predict over')

def test_rmse(testDataFile,resultSaveFile):
    fi = open(testDataFile,'r')
    fo = open(resultSaveFile,'r')
    test_score = []
    predict_score = []
    rmse = 0
    cnt = 0
    for i in fi:
        test_score.append(float(i.split()[2].strip()))
    fi.close()
    for i in fo:
        predict_score.append(float(i.split()[2].strip()))
    fo.close()
    score = zip(test_score,predict_score)
    for tScore,pScore in score:
        cnt += 1
        rmse += (tScore - pScore) * (tScore - pScore)
    return math.sqrt(rmse/cnt)

if __name__ == '__main__':
    configureFile = 'PMF.conf'

    testDataFile = '../map/smallPredictionMatrix.txt'
    trainDataFile = '../map/smallMatrix.txt'
    modelSaveFile = 'PMF_model.pkl'
    resultSaveFile = '../map/prediction.txt'

    SVD(configureFile,trainDataFile,modelSaveFile)
    predict(modelSaveFile,testDataFile,resultSaveFile)