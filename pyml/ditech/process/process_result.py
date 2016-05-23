#statstic num of the result

result_dct = {}
with open('d:/ditech/result_last.csv', 'r') as file:
    lines = file.readlines()

    for line in lines:
        rst = line.split(',')
        if not result_dct.has_key(int(rst[-1])):
            result_dct[int(rst[-1])] = 1
        else:
            result_dct[int(rst[-1])] += 1

results = sorted(result_dct.items(), key=lambda x:x[0])

for rs in results:
    print rs[0], rs[1]
