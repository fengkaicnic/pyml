#statstic num of the result

import pdb

def statstic_num():
    result_dct = {}
#     with open('d:/ditech/result_last.csv', 'r') as file:
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

if __name__ == '__main__':

    results = statstic_num()
    simulate_one(results)
