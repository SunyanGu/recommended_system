import random

def split_train_test(text_name,text_train,text_test,proportion = 0.1):
    f = open(text_name,'r')
    train = open(text_train,'w')
    test = open(text_test,'w')

    data_split = f.readlines()
    random.shuffle(data_split)

    train_num = len(data_split)*(1-proportion)
    test_num = len(data_split)*proportion

    for i in range(0,int(train_num)):
        train.write(data_split[i])
    for i in range(1,int(test_num+1)):
        test.write(data_split[-i].split()[0] + '    '+ data_split[-i].split()[1] + '    '+ data_split[-i].split()[2])
        test.write('\n')




if __name__ == '__main__':
    proportion = 0.1
    text_name = './map/bigMatrix.txt'   #所有数据
    text_test = './map/smallPredictionMatrix.txt'  #测试集
    text_train = './map/smallMatrix.txt'    #训练集
    split_train_test(text_name, text_train, text_test, proportion)