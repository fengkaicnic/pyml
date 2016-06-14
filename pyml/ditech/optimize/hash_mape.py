
import pdb
import pickle

def get_mape(hash_splice_dct):
    with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
        lines = file.readlines()
    splice_lst = [46, 58, 70, 82, 94, 106, 118, 130, 142]
    total = 0
    mape = 0.0
    for line in lines:
        lst = line.strip().split(',')
        for splice in splice_lst:
            if not int(lst[splice + 1]):
                total += 1
                continue
            else:
                vec = hash_splice_dct[lst[0]][splice]
                # pdb.set_trace()
                mape += abs(max((int(lst[splice - 2])*vec[0] + int(lst[splice - 1])*vec[1] + int(lst[splice])*vec[2])/2, 1) - int(lst[splice + 1]))/float(lst[splice + 1])
                total += 1

    print mape, total, mape/total
    return mape/total

if __name__ == '__main__':

    file = open('hash_splice_dct', 'r')
    hash_splice_dct = pickle.load(file)
    file = open('hash_splice_param', 'r')
    hash_splice_param = pickle.load(file)

    mape = 0.0

    mape += get_mape(hash_splice_param)
    # mape += get_mape(splice, vec)

    print mape
