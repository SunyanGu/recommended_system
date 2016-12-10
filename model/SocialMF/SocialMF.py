import math
import random
import pickle

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

def PredictScore(av,bu,bi,pu,qi):
    pScore = av + bu + bi + InterProduct(pu,qi)
    if pScore < 1:
        pScore = 1
    elif pScore > 5:
        pScore = 5
    return pScore

#def SVD(configureFile, testDataFile, trainDataFile, modelSaveFile):
def SocialMF(configureFile,trainDataFile,modelSaveFile):
    #get the configure
    fi = open(configureFile,'r')
    line = fi.readline()
    arr = line.split()
    averageScore = float(arr[0].strip())
    userNum = int(arr[1].strip())
    itemNum = int(arr[2].strip())
    factorNum = int(arr[3].strip())
    learnRate = float(arr[4].strip())
    regularization = float(arr[5].strip())
    print(factorNum)
    fi.close()

    bi = [0.0 for i in range(itemNum)]   #bi表示用户评分偏离平均分程度
    bu = [0.0 for i in range(userNum)]   #bu表示商户评分偏离平均分程度
    temp = math.sqrt(factorNum)
    qi = [[(0.1 * random.random() / temp) for j in range(factorNum)] for i in range(itemNum)]   #构造商店/因子矩阵
    pu = [[(0.1 * random.random() / temp) for j in range(factorNum)] for i in range(userNum)]   #构造用户/因子矩阵
    print('initinalization end\nstart training\n')

    #train model
    preRmse = 100000000.0
    for step in range(500):
        fi = open(trainDataFile,'r')
        for line in fi:
            arr = line.split()
            uid = int(arr[0].strip()) - 1
            iid = int(arr[1].strip()) - 1
            # uid = int(arr[0].strip())
            # iid = int(arr[1].strip())
            score = float(arr[2].strip())
            # print('uid is %d'%uid)
            # print('iid is %d'%iid)
            prediction = PredictScore(averageScore,bu[uid],bi[iid],pu[uid],qi[iid])   #预估分数

            eui = score - prediction    #实际分数和预测评分的差值

            #update parameters
            bu[uid] += learnRate * (eui - regularization * bu[uid])
            bi[iid] += learnRate * (eui - regularization * bi[iid])

            for k in range(factorNum):
                temp = pu[uid][k]  #attention here,must save the value of pu before updating
                pu[uid][k] += learnRate * (eui * qi[iid][k] - regularization*pu[uid][k])
                qi[iid][k] += learnRate * (eui * temp -regularization * qi[iid][k])
                # pu[uid][k] += learnRate * (eui  - regularization * pu[uid][k])
                # qi[iid][k] += learnRate * (eui  - regularization * qi[iid][k])
        fi.close()
        #learnRate *= 0.9
        curRmse = Validate(trainDataFile, averageScore, bu, bi, pu, qi)
        print("test_RMSE in step %d: %f" %(step, curRmse))
        if curRmse >= preRmse:
          break
        else:
          preRmse = curRmse
    #write the model to files
    fo = open(modelSaveFile,'wb')
    pickle.dump(bu,fo,True)
    pickle.dump(bi, fo, True)
    pickle.dump(qi, fo, True)
    pickle.dump(pu, fo, True)
    fo.close()
    print('model generation over')

#validate the model
def Validate(testDataFile,av,bu,bi,pu,qi):
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
        pScore = PredictScore(av,bu[uid],bi[iid],pu[uid],qi[iid])

        tScore = float(arr[2].strip())
        #print('tScore%f'%tScore,'pScore%f\n'%pScore)
        rmse += (tScore - pScore) * (tScore - pScore)
    fi.close()
    return math.sqrt(rmse/cnt)

#use the model to make predict
def predict(configureFile,modelSaveFile,testDataFile,resultSaveFile):
    #get parameter
    fi = open(configureFile,'r')
    line = fi.readline()
    arr = line.split()
    averageScore = float(arr[0].strip())
    fi.close()

    #get model
    fi = open(modelSaveFile,'rb')
    bu = pickle.load(fi)
    bi = pickle.load(fi)
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
        pScore = PredictScore(averageScore,bu[uid],bi[iid],pu[uid],qi[iid])
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
    configureFile = 'svd.conf'

    testDataFile = '../map/smallPredictionMatrix.txt'
    trainDataFile = '../map/smallMatrix.txt'
    modelSaveFile = 'svd_model.pkl'
    resultSaveFile = '../map/prediction.txt'

    # SVD(configureFile,trainDataFile,modelSaveFile)
    # predict(configureFile,modelSaveFile,testDataFile,resultSaveFile)