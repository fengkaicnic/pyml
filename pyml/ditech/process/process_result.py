#statstic num of the result

import pdb

def statstic_num():
    result_dct = {}
    # with open('d:/ditech/compare_result_53.csv', 'r') as file:
    # with open('d:/ditech/result_last.csv', 'r') as file:
    with open('d:/ditech/gbdt_model_result.csv', 'r') as file:
        lines = file.readlines()

        for line in lines:
            rst = line.strip().split(',')
            if not result_dct.has_key(float(rst[-1])):
                result_dct[float(rst[-1])] = 1
            else:
                result_dct[float(rst[-1])] += 1

    results = sorted(result_dct.items(), key=lambda x:x[0])

    for rs in results:
        print rs[0], rs[1]

    return results

def simulate_one(results):
    allnum = 0
    # pdb.set_trace()
    allnum += results[0][1]
    for rs in results[1:]:
        allnum += rs[1]/(rs[0]/(0/10.0 + 1))
        # allnum += rs[1]/rs[0]
    print (2838 - allnum)/2838.0


def compare_last_result():
    with open('d:/ditech/gbdt_model_result.csv', 'r') as file:
        lines = file.readlines()

    with open('d:/ditech/result_3_inter', 'r') as file:
        rlines = file.readlines()

    result_dct = {}
    for line in rlines:
        line = line.strip()
        lst = line.split(',')
        result_dct[lst[1]+'-'+lst[2]] = lst[4]

    num = 0
    results = []
    for line in lines:
        line = line.strip()
        lst = line.split(',')
        # if int(result_dct[lst[0]+'-'+lst[1]]) / float(lst[2]) < 1 and float(lst[2]) > 1:
        if int(result_dct[lst[0]+'-'+lst[1]]) / float(lst[2]) > 2 or 1:
            print lst[0]+'-'+lst[1],lst[2],result_dct[lst[0]+'-'+lst[1]]
            if not float(result_dct[lst[0]+'-'+lst[1]]) < 5:
                lst[2] = float(result_dct[lst[0]+'-'+lst[1]])*2/3
            num += 1
        results.append(','.join(map(lambda x:str(x), lst)))

    # with open('d:/ditech/compare_result_53.csv', 'wb') as file:
    #     file.writelines('\n'.join(results))

    print num

if __name__ == '__main__':

    # results = statstic_num()
    # simulate_one(results)
    compare_last_result()
    # pdb.set_trace()
