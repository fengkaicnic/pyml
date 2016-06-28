
import pdb
import time
import pickle
import traceback


def get_num():
    index = 0
    with open('d:/bimbo/train.csv', 'r') as file:
        line = file.readline()
        while line:
            index += 1
            line = file.readline()

    print index


def get_data():
    with open('d:/bimbo/train.csv', 'r') as file:
        for i in range(19):
            line = file.readline()
            print line


def handle_train_data():
    data_dct = {}
    with open('d:/bimbo/test.csv', 'r') as file:
        line = file.readline()
        # pdb.set_trace()
        while line:
            lst = line.strip().split(',')
            if not data_dct.has_key(lst[3]):
                data_dct[lst[3]] = {lst[2]:{lst[6]:{lst[4]:{lst[5]:lst[0]}}}}
            else:
                if not data_dct[lst[3]].has_key(lst[2]):
                    data_dct[lst[3]][lst[2]] = {lst[6]:{lst[4]:{lst[5]:lst[0]}}}
                else:
                    if not data_dct[lst[3]][lst[2]].has_key(lst[6]):
                        data_dct[lst[3]][lst[2]][lst[6]] = {lst[4]:{lst[5]:lst[0]}}
                    else:
                        if not data_dct[lst[3]][lst[2]][lst[6]].has_key(lst[4]):
                            data_dct[lst[3]][lst[2]][lst[6]][lst[4]] = {lst[5]:lst[0]}
                        else:
                            data_dct[lst[3]][lst[2]][lst[6]][lst[4]][lst[5]] = lst[0]
            line = file.readline()

    with open('d:/bimbo/train.csv', 'r') as file:
        line = file.readline()
        index = 0
        error = 0
        while line:
            # pdb.set_trace()
            # if index > 190:
            #     break
            lst = line.strip().split(',')
            try:
                id = data_dct[lst[2]][lst[1]][lst[5]][lst[3]][lst[4]]
                # print id
                index += 1
            except:
                # traceback.print_exc()
                error += 1
                pass
            line = file.readline()
    print index
    print error

    # file = open('data_dct', 'wb')
    # pickle.dump(data_dct, file)


if __name__ == '__main__':

    st = time.time()
    # get_data()
    # get_num()
    handle_train_data()
    ed = time.time()

    print ed - st
