#coding:utf8
import pickle
import sys
reload(sys)
import pdb
sys.setdefaultencoding('utf8')
def store_rst(decesion_tree,filename):

    writer = open(filename,'w')
    pickle.dump(decesion_tree,writer)
    writer.close()

def read_rst(filename):

    reader = open(filename,'rU')
    return pickle.load(reader)

def get_key_positionsingle(postdct, position_dct, position): 
    if position_dct.has_key(position):
        return position
    
    for key in postdct.keys():   
        if key in position:
            if u'总监' in position or u'主管' in position:
                return postdct[key][2]
            elif u'经理' in position or u'主任' in position:
                return postdct[key][1]
            else:
                return postdct[key][0]
    return 'None'

def get_key_position(postdct, positions): 
    for key in postdct.keys():   
        if key in positions[0][0]:
            if u'总监' in positions[0][0] or u'主管' in positions[0][0]:
                return postdct[key][2]
            elif u'经理' in positions[0][0] or u'主任' in positions[0][0]:
                return postdct[key][1]
            else:
                return postdct[key][0]
        elif key in positions[1][0]:
            if u'总监' in positions[1][0] or u'主管' in positions[1][0]:
                return postdct[key][2]
            elif u'经理' in positions[1][0] or u'主任' in positions[1][0]:
                return postdct[key][1]
            else:
                return postdct[key][0]
    return None

def get_key_position_old(postdct, positions): 
    for key in postdct.keys():   
        if key in positions[0]:
            if u'总监' in positions[0] or u'主管' in positions[0]:
                return postdct[key][2]
            elif u'经理' in positions[0] or u'主任' in positions[0]:
                return postdct[key][1]
            else:
                return postdct[key][0]
        elif key in positions[1]:
            if u'总监' in positions[1] or u'主管' in positions[1]:
                return postdct[key][2]
            elif u'经理' in positions[1] or u'主任' in positions[1]:
                return postdct[key][1]
            else:
                return postdct[key][0]
    return None

def get_position(major_dusdct, positions, position_dct, postdct):
    if major_dusdct.has_key(positions[0][2]):
        if major_dusdct[positions[0][2]].has_key(positions[0][1]):
            for position_name in major_dusdct[positions[0][2]][positions[0][1]]:
                if position_dct.has_key(position_name):
                    return position_name
            for position_name in major_dusdct[positions[0][2]][positions[0][1]]:
                for key in postdct.keys():   
                    if key in positions[0]:
                        if u'总监' in positions[0] or u'主管' in positions[0]:
                            return postdct[key][2]
                        elif u'经理' in positions[0] or u'主任' in positions[0]:
                            return postdct[key][1]
                        else:
                            return postdct[key][0]
                    elif key in positions[1]:
                        if u'总监' in positions[0] or u'主管' in positions[0]:
                            return postdct[key][2]
                        elif u'经理' in positions[0] or u'主任' in positions[0]:
                            return postdct[key][1]
                        else:
                            return postdct[key][0]
    return u'销售经理'    

def get_industry_position(industryr, industrys, position_dct, postdct):
    if industryr.has_key(industrys[0]):
        if position_dct.has_key(industryr[industrys[0]][0]):
            return industryr[industrys[0]][0]
        else:
            position = get_key_positionsingle(postdct, industryr[industrys[0]][0])
            if position:
                return position
    if industryr.has_key(industrys[1]):
        if position_dct.has_key(industryr[industrys[1]][0]):
            return industryr[industrys[1]][0]
        else:
            position = get_key_positionsingle(postdct, industryr[industrys[1]][0])
            if position:
                return position
    return 'test'

def get_labels(train_file, ind):

    labels = []
    for index,line in enumerate(open(train_file,'rU').readlines()):
        print index
        label = line.strip().split(',')[ind]
        labels.append(label)
    return labels

def format_data(dataset_file):
    dataset = []
    for index,line in enumerate(open(dataset_file,'rU').readlines()):
        line = line.strip()
        fea_and_label = line.split(',')
        dataset.append(fea_and_label)
    #features = [dataset[0][i] for i in range(len(dataset[0])-1)]
    #sepal length�����೤�ȣ���sepal width�������ȣ���petal length�����곤�ȣ���petal width�������ȣ�
    features = ['degree', 'age','start_age','bstart_year','gender','start_salary','start_size','major']
    return dataset,features