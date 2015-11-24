#coding:utf8
import random
from jobs.dctree.randomforest import tree
import time
import sys
import pdb
from jobs.utils import store_rst
reload(sys)
start = time.clock()
sys.setdefaultencoding('utf8')

def generate_feature_index(indexs, num):
    flag = False
    indexlst = []
    while not flag:
        index = random.randint(1,len(indexs)-1)
        if index not in indexlst:
            indexlst.append(index)
            if len(indexlst) == num:
                flag = True
    return indexlst

def generate_train_file(dataset, features_index, total=None):
    datasets = []
    labels = []
    for i in xrange(10000):
        nu = random.randint(0, 69999)
#         datasets[i].append(dataset[nu][0])
        datasets.append([dataset[nu][j] for j in features_index])
        datasets[i].append(dataset[nu][0])
        labels.append(dataset[nu][0])
    
    return datasets, labels

def generate_test_file(dataset, feature_index, total=None):
    datasets = []
    for i in xrange(20000):
#         nu = random.randint(0, 9999)
        datasets.append([dataset[i][j] for j in feature_index])
    
    return datasets

def generate_result(results):
    num1 = len(results)
    num2 = len(results[0])
    result = []
    for i in range(num2):
        dct = {}
        for j in range(num1):
            if not dct.has_key(results[j][i]):
                dct[results[j][i]] = 1
            else:
                dct[results[j][i]] += 1
#         pdb.set_trace()
        srlst = sorted(dct.items(),key=lambda jj:jj[1],reverse=True)
        result.append(srlst[0][0])
    
    return result

def get_labels(train_file, ind):
    #pdb.set_trace()
    labels = []
    for index,line in enumerate(open(train_file,'rU').readlines()):
        label = line.strip().split(',')[ind]
        labels.append(label)
    return labels

def get_tlabels(train_data, index):
    labels = []
    for data in train_data:
        labels.append(data[index])
    return labels

def format_data(dataset_file):

    dataset = []
    for index,line in enumerate(open(dataset_file,'rU').readlines()):
        line = line.strip()
        fea_and_label = line.split(',')
        dataset.append(fea_and_label)
    #features = [dataset[0][i] for i in range(len(dataset[0])-1)]
    #sepal 
#     features = ['age', 'start_age', 'bstart_year', 'start_salary', 'gender', 'major', 'size1', 'size2', 'salary1', 'salary2', 'industry1', 'industry2']
    features = ['degree', 'age','start_age','bstart_year','start_salary','start_size','major']
    return dataset,features

if __name__ == '__main__':
    #    print "please use: python decision.py train_file test_file"
    #    sys.exit()
    train_file = 'd:/jobs/dctree/random/degree-train.csv'
    test_file = 'd:/jobs/dctree/random/degree-test.csv'
    
    labels = get_labels(train_file,0)
    train_dataset, train_features = format_data(train_file)
    test_dataset, test_features = format_data(test_file)
    tree_num = 3990
    feature_num = 2
    result = []

    for j in range(tree_num):
        features_index = generate_feature_index(train_features, feature_num)
        features = [train_features[l] for l in features_index]
        print features_index
        print features
        train_set, labels = generate_train_file(train_dataset, features_index)
        decesion_tree = tree.rand(train_set, features, labels, 0.0005)
        test_set = generate_test_file(test_dataset, features_index)
        rst = tree.rand_test(test_set, features, decesion_tree)
        result.append(rst)
    
    finalrst = generate_result(result)
    store_rst(finalrst, 'finalrut')
    
end = time.clock()
print (end - start)