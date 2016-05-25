#supplement splice zero
import pdb

def remove_enter():
    with open('d:/ditech/splice_series.csv', 'r') as file:
        lines = file.readlines()
    num = 0
    results = []
    strws = ''
    for line in lines:
        num += 1
        line = line.strip()
        strws = strws + line
        if num%2 != 0:
            continue
        else:
            results.append(strws)
            strws = ''
    
    with open('d:/ditech/splice_series1.csv', 'wb') as file:
        file.writelines('\n'.join(results))

def add_zero():
    with open('d:/ditech/splice_series.csv', 'r') as file:
        lines = file.readlines()

    results = []
    for line in lines:
        lst = line.strip().split(',')

        while len(lst) < 23:
            lst.append('0')

        results.append(','.join(lst))

    with open('d:/ditech/splice_series.csv', 'wb') as file:
        file.writelines('\n'.join(results))


def sorted_splice():
    with open('d:/ditech/splice_series.csv', 'r') as file:
        lines = file.readlines()

    results = []
    splice_key = ''
    sorted_lst = []
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        if splice_key != lst[0]:
            if len(sorted_lst) == 0:
                splice_key = lst[0]
                sorted_lst = [lst]
            else:
                sorted_lst = sorted(sorted_lst, key=lambda item:int(item[2]))
                for ls in sorted_lst:
                    results.append(','.join(ls))
                sorted_lst = [lst]
                splice_key = lst[0]
        else:
            sorted_lst.append(lst)

    sorted_lst = sorted(sorted_lst, key=lambda item:int(item[2]))
    for ls in sorted_lst:
        results.append(','.join(ls))

    with open('d:/ditech/splice_sor_series.csv', 'wb') as file:
        file.writelines('\n'.join(results))


def split_by_week():
    with open('d:/ditech/citydata/read_me_1.txt', 'r') as file:
        tlines = file.readlines()
    with open('d:/ditech/splice_sor_series.csv', 'r') as file:
        lines = file.readlines()
    tdctt = {}
    for line in tlines:
        line = line.strip()
        lst = line.split('-')
        if not tdctt.has_key(int(lst[-2])):
            # pdb.set_trace()
            tdctt[int(lst[-2])] = [int(lst[-1])]
        else:
            tdctt[int(lst[-2])].append(int(lst[-1]))

    splice_dct = {}
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        if not splice_dct.has_key(lst[0]):
            splice_dct[lst[0]] = {int(lst[2]):lst[3:]}
        else:
            splice_dct[lst[0]][int(lst[2])] = lst[3:]

    results = []
    for key in tdctt.keys():
        for splice in tdctt[key]:
            for skey in splice_dct.keys():
                rst = []
                rst.append(skey)
                rst.append(key)
                rst.append(splice)
                num = key
                while num > 0:
                    # pdb.set_trace()
                    if num <= len(splice_dct[skey][splice]):
                        rst.append(splice_dct[skey][splice][num-1])
                    num -= 7
                results.append(','.join(map(lambda x:str(x), rst)))

    with open('d:/ditech/split_by_week.csv', 'wb') as file:
        file.writelines('\n'.join(results))


if __name__ == '__main__':
    remove_enter()
#     sorted_splice()
#     split_by_week()
