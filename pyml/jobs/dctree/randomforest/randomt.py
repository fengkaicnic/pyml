import random
from jobs.dctree.randomforest import tree
import time
start = time.clock()

def generate_feature_index(indexs, num):
    flag = False
    indexlst = []
    while not flag:
        index = random.randint(len(indexs))
        if index not in indexlst:
            indexlst.append(index)
            if len(indexlst) == num:
                flag = True
    return indexlst

def generate_train_file(dataset, features_index, total=None):
    datasets = []
    labels = []
    for i in xrange(60000):
        nu = random.randint(0, 59999)
        datasets.append([dataset[nu][j] for j in features_index])
        labels.append(dataset[nu][-1])
    
    return datasets, labels

def generate_test_file(dataset, feature_index, total=None):
    datasets = []
    for i in xrange(10000):
        nu = random.randint(0, 9999)
        datasets.append([dataset[nu][j] for j in feature_index])
    
    return datasets

def generate_result(results):
    num1 = len(results)
    num2 = len(results[0])
    result = []
    for i in num2:
        dct = {}
        for j in num2:
            if not dct.has_key(results[j][i]):
                dct[results[j][i]] = 1
            else:
                dct[results[j][i]] += 1
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
    #sepal length�����೤�ȣ���sepal width�������ȣ���petal length�����곤�ȣ���petal width�������ȣ�
    features = ['age', 'start_age', 'bstart_year', 'start_salary', 'gender', 'major', 'size1', 'size2', 'salary1', 'salary2', 'industry1', 'industry2']
    return dataset,features

if __name__ == '__main__':
    #    print "please use: python decision.py train_file test_file"
    #    sys.exit()
    train_file = 'd:/jobs/dctree/salary/train.csv'
    test_file = 'd:/jobs/dctree/salary/test.csv'
    
    labels = get_labels(train_file,5)
    train_dataset, train_features = format_data(train_file)
    test_dataset, test_features = format_data(train_file)
    tree_num = 10
    feature_num = 4
    result = []

    for j in tree_num:
        features_index = generate_feature_index(train_features, feature_num)
        features = [train_features[l] for l in features_index]
        train_set, labels = generate_train_file(train_dataset, features_index)
        decesion_tree = tree.rand(train_set, features, labels, 0.057)
        test_set = generate_test_file(test_dataset, features_index)
        rst = tree.rand_test(test_set, features, decesion_tree)
        result.append(rst)
    
    lastrst = generate_result(result)
    