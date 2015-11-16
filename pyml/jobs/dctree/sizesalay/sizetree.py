#-*- coding:utf-8 -*-

import sys
from math import log
import operator
from numpy import mean
import numpy as np
import pdb
import time
import types
start = time.clock()

def get_labels(train_file):
#     pdb.set_trace()
    labels = []
    for index,line in enumerate(open(train_file,'rU').readlines()):
        label = line.strip().split(',')[-1]
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
    features = ['age','gender','major','size1','size2']
    return dataset,features

def split_dataset(dataset,feature_index,labels):

    dataset_less = []
    dataset_greater = []
    label_less = []
    label_greater = []
    datasets = []
    for data in dataset:
        datasets.append(data[0:4])
    mean_value = mean(datasets,axis = 0)[feature_index]   #��ݼ��ڸ������������ȡֵ��ƽ��ֵ
    for data in dataset:
        if data[feature_index] > mean_value:
            dataset_greater.append(data)
            label_greater.append(data[-1])
        else:
            dataset_less.append(data)
            label_less.append(data[-1])
    return dataset_less,dataset_greater,label_less,label_greater

def cal_entropy(dataset, index):

    n = len(dataset)    
    label_count = {}
    for data in dataset:
        label = data[index]
        if label_count.has_key(label):
            label_count[label] += 1
        else:
            label_count[label] = 1
    entropy = 0
    for label in label_count:
        prob = float(label_count[label])/n
        entropy -= prob*log(prob,2)
    #print 'entropy:',entropy
    return entropy

def cal_entropy_f(dataset, index):
    n = len(dataset)    
    label_count = {}
    for data in dataset:
        label = data[index]
        if label_count.has_key(label):
            label_count[label] += 1
        else:
            label_count[label] = 1
    entropy = 0
    for label in label_count:
        prob = float(label_count[label])/n
        entropy -= prob*log(prob,2)
    #print 'entropy:',entropy
    return entropy

def cal_entropy_dct(datadct, count):
    entropy = 0.0
    for key in datadct.keys():
        num = datadct[key]
        prob = float(num)/count
        entropy -= prob*log(prob,2)

    return entropy

def cal_info_gain_new(dataset, feature_index, base_entropy, index):
    #for data in dataset:
    #    datasets.append(data[1:7])
    feature_dct = {}
    for data in dataset:
    #    print data
        if feature_dct.has_key(data[feature_index]):
            feature_dct[data[feature_index]]['count'] += 1
            if feature_dct[data[feature_index]]['dct'].has_key(data[index]):
                feature_dct[data[feature_index]]['dct'][data[index]] += 1
            else:
                feature_dct[data[feature_index]]['dct'][data[index]] = 1
        else:
            feature_dct[data[feature_index]] = {'count':1}
            feature_dct[data[feature_index]]['dct'] = {}
            feature_dct[data[feature_index]]['dct'][data[index]] = 1
    info_gain = 0.0
    for item in feature_dct.iteritems():
        info_gain += (float(item[1]['count'])/len(dataset))*cal_entropy_dct(item[1]['dct'], item[1]['count'])
    print info_gain
    return base_entropy - info_gain
    
def cal_info_gain(dataset,feature_index,base_entropy):

    datasets = []
    for data in dataset:
        datasets.append(data[0:6])
    #print datasets
    mean_value = mean(datasets,axis = 0)[feature_index]    #����ָ��������������ݼ�ֵ��ƽ��ֵ
    #print mean_value
    dataset_less = []
    dataset_greater = []
    for data in dataset:
        if data[feature_index] > mean_value:
            dataset_greater.append(data)
        else:
            dataset_less.append(data)
    #������ H(D/F)
    condition_entropy = float(len(dataset_less))/len(dataset)*cal_entropy(dataset_less) + float(len(dataset_greater))/len(dataset)*cal_entropy(dataset_greater)
    #print 'info_gain:',base_entropy - condition_entropy
    return base_entropy - condition_entropy 

def cal_info_gain_ratio(dataset, feature_index, features):
   
    base_entropy = cal_entropy_f(dataset, len(features))
    feature_entropy = cal_entropy_f(dataset, feature_index)
    if feature_entropy == 0:
        return 0
    '''
    if base_entropy == 0:
        return 1
    '''
    info_gain = cal_info_gain_new(dataset,feature_index,base_entropy,len(features))
    info_gain_ratio = info_gain/feature_entropy
    print features[feature_index]
    print info_gain_ratio
    return info_gain_ratio
    
def choose_best_fea_to_split(dataset,features):

    #base_entropy = cal_entropy(dataset)
    split_fea_index = -1
    max_info_gain_ratio = 0.0
    for i in range(len(features)):
        #info_gain = cal_info_gain(dataset,i,base_entropy)
        #info_gain_ratio = info_gain/base_entropy
        info_gain_ratio = cal_info_gain_ratio(dataset, i, features)
        if info_gain_ratio > max_info_gain_ratio:
            max_info_gain_ratio = info_gain_ratio
            split_fea_index = i
    return split_fea_index
    

def most_occur_label(labels):

    label_count = {}
    for label in labels:
        if label not in label_count.keys():
            label_count[label] = 1
        else:
            label_count[label] += 1
    sorted_label_count = sorted(label_count.iteritems(),key = operator.itemgetter(1),reverse = True)
    return sorted_label_count[0][0]

def build_tree(dataset,labels,features, weight=None):

    if len(labels) == 0:
        return 'NULL'
    if len(labels) == len(labels[0]):
        return labels[0]
    #��û�пɻ��ֵ�������,�򷵻���ݼ��г��ִ�������label
    if len(features) == 0:
        return most_occur_label(labels)
    #����ݼ������ȶ����򷵻���ݼ��г��ִ�������label
    if cal_entropy(dataset, len(features)) == 0:
        return most_occur_label(labels)
    split_feature_index = choose_best_fea_to_split(dataset,features)
    split_feature_index = split_feature_index 
    split_feature = features[split_feature_index]
    decesion_tree = {split_feature:{}}
    #��������������Ϣ�����С����ֵ,�򷵻���ݼ��г��ִ�������label
    if cal_info_gain_ratio(dataset, split_feature_index, features) < weight:
        return most_occur_label(labels)
    split_feature_dct = {}
    for data in dataset:
        if split_feature_dct.has_key(data[split_feature_index]):
            split_feature_dct[data[split_feature_index]].append(data)
        else:
            split_feature_dct[data[split_feature_index]] = [data]
    for key in split_feature_dct.keys():
        train_labs = get_tlabels(split_feature_dct[key], len(features))
        decesion_tree[split_feature][key] = build_tree(split_feature_dct[key], train_labs, features)
    #del(features[split_feature_index])
    #dataset_less,dataset_greater,labels_less,labels_greater = split_dataset(dataset,split_feature_index,labels)
    #decesion_tree[split_feature]['<='] = build_tree(dataset_less,labels_less,features)
    #decesion_tree[split_feature]['>'] = build_tree(dataset_greater,labels_greater,features)
    return decesion_tree

def store_tree(decesion_tree,filename):

    import pickle
    writer = open(filename,'w')
    pickle.dump(decesion_tree,writer)
    writer.close()

def read_tree(filename):

    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)

def classify(decesion_tree,features,test_data,mean_values):
    first_fea = decesion_tree.keys()[0]
    fea_index = features.index(first_fea)
    if test_data[fea_index] <= mean_values[fea_index]:
        sub_tree = decesion_tree[first_fea]['<=']
        if type(sub_tree) == dict:
            return classify(sub_tree,features,test_data,mean_values)
        else:
            return sub_tree
    else:
        sub_tree = decesion_tree[first_fea]['>']
        if type(sub_tree) == dict:
            return classify(sub_tree,features,test_data,mean_values)
        else:
            return sub_tree

def classify_t(decesion_tree, features, test_data, mean_values=None):
    first_fea = decesion_tree.keys()[0]
    fea_index = features.index(first_fea)
    if not decesion_tree[first_fea].has_key(test_data[fea_index]):
        return 1
    if type(decesion_tree[first_fea][test_data[fea_index]]) is types.DictType:
            return classify_t(decesion_tree[first_fea][test_data[fea_index]], features, test_data)
    else:
        return decesion_tree[first_fea][test_data[fea_index]]
        
        
def get_means(train_dataset):

    dataset = []
    for data in train_dataset:
        dataset.append(data[0:4])
    mean_values = mean(dataset,axis = 0)   #��ݼ��ڸ������������ȡֵ��ƽ��ֵ
    return mean_values

def run(train_file, test_file, weight):
    #pdb.set_trace()
    labels = get_labels(train_file)
    train_dataset,train_features = format_data(train_file)
#     pdb.set_trace()
    decesion_tree = build_tree(train_dataset, labels, train_features, weight)
    print 'decesion_tree :',decesion_tree
    store_tree(decesion_tree,'size_tree')
    #mean_values = get_means(train_dataset)
    #test_dataset,test_features = format_data(test_file)
    #n = len(test_dataset)
    #correct = 0
    #for test_data in test_dataset:
    #    label = classify(decesion_tree,test_features,test_data,mean_values)
    #    #print 'classify_label  correct_label:',label,test_data[-1]
    #    if label == test_data[-1]:
    #        correct += 1
    #print "׼ȷ��: ",correct/float(n)

def test(test_file):
    decesion_tree = read_tree('size_tree')
    test_dataset,test_features = format_data(test_file)
#     pdb.set_trace()
    result = []
    for data in test_dataset:
        label = classify_t(decesion_tree, test_features, data)
        result.append(label)
#     pdb.set_trace()
    store_tree(result, 'sizeresult.txt')

#############################################################
if __name__ == '__main__':
    #if len(sys.argv) != 3:
    #    print "please use: python decision.py train_file test_file"
    #    sys.exit()
    train_file = 'd:/jobs/dctree/size/ss-train.csv'
    test_file = 'd:/jobs/dctree/size/ss-test.csv'
#     run(train_file, test_file, 0.058)
    test(test_file)
end = time.clock()
print (end - start)