import sys
reload(sys)
import pdb
import types
import copy
from jobs import utils

def read_tree(filename):

    import pickle
    reader = open(filename,'rU')
    return pickle.load(reader)

def format_data(dataset_file):

    dataset = []
    for index,line in enumerate(open(dataset_file,'rU').readlines()):
        line = line.strip()
        fea_and_label = line.split(',')
        dataset.append(fea_and_label)
    #features = [dataset[0][i] for i in range(len(dataset[0])-1)]
    #sepal length
    features = ['age','bstart_year','gender','major','salary1','salary2']
    return dataset,features

def get_tlabels(train_data, index=None):
    labels = []
    for data in train_data:
        labels.append(data[-1])
    return labels

def label_error(labels):
    total = len(labels)
    if total == 0:
        return 0, 0
    label_dct = {}
    for label in labels:
        if not label_dct.has_key(label):
            label_dct[label] = 1
        else:
            label_dct[label] += 1
    
    lst = sorted(label_dct.items(),key=lambda jj:jj[1],reverse=True)
#     pdb.set_trace()
    return float(lst[0][1]/total), lst[0][0]

def prun_error(labels, result):
    total = len(labels)
    if total == 0:
        return 0
    num = 0
    for i in range(len(labels)):
        if labels[i] == result[i]:
            num += 1
    return float(num)/total

def lst_tdct(prunlst, prundct):
    prundctt = {}
    if len(prunlst) != 0:
        prundctt[prunlst.pop()] = prundct
        return lst_tdct(prunlst, prundctt)
    return prundct
    
def prun(tree_dct, features, dataset, prunlst = None):
    if prunlst is None:
        prunlst = []
#     prundct = {}
    for key in tree_dct.iterkeys():
        if type(tree_dct[key]) is types.DictionaryType:
            prunlst.append(key)
            tree_dct[key] = prun(tree_dct[key], features, dataset, prunlst)
#             print prunlst
            prunlst.pop()
        else:
            continue
#     pdb.set_trace()
#     if prunlst[-1] in features:
#         prunlst.pop()
    prundct = lst_tdct(copy.deepcopy(prunlst), {})
    
    testdata = []
    if len(prundct) != 0:
        for data in dataset:
            testd = classify_prun(prundct, features, data)
            if testd is not None:
                testdata.append(testd)
    else:
        testdata = dataset
#     pdb.set_trace()
    print prundct
    print len(testdata)
    labels = get_tlabels(testdata)
    label_pre, label = label_error(labels)
    
    tree_result = []
    result = 0
#     pdb.set_trace()
    for data in testdata:
        result = classify_t(tree_dct, features, data)
        tree_result.append(result)
    prun_pre = prun_error(labels, tree_result)
    if label_pre > prun_pre:
        return label
    else:
        return tree_dct
    
def classify_prun(decesion_tree, features, test_data, mean_values=None):
#     pdb.set_trace()
    first_fea = decesion_tree.keys()[0]
    fea_index = features.index(first_fea)
    if not decesion_tree[first_fea].has_key(test_data[fea_index]):
        return None
    if type(decesion_tree[first_fea][test_data[fea_index]]) is types.DictType:
            if len(decesion_tree[first_fea][test_data[fea_index]]) == 0:
                return test_data
            return classify_prun(decesion_tree[first_fea][test_data[fea_index]], features, test_data)
    else:
        return decesion_tree[first_fea][test_data[fea_index]]

def classify_t(decesion_tree, features, test_data, mean_values=None):
    first_fea = decesion_tree.keys()[0]
    fea_index = features.index(first_fea)
    if not decesion_tree[first_fea].has_key(test_data[fea_index]):
        return 1
    if type(decesion_tree[first_fea][test_data[fea_index]]) is types.DictType:
            return classify_t(decesion_tree[first_fea][test_data[fea_index]], features, test_data)
    else:
        return decesion_tree[first_fea][test_data[fea_index]]
    
if __name__ == '__main__':
    #if len(sys.argv) != 3:
    #    print "please use: python decision.py train_file test_file"
    #    sys.exit()
    test_file = 'd:/jobs/dctree/salary/test.csv'
    decesion_tree = read_tree('salary_tree')
    dataset, features = format_data(test_file)
    prun_tree = prun(decesion_tree, features, dataset)
    utils.store_rst(prun_tree, 'prunsalary_tree')
    print prun_tree