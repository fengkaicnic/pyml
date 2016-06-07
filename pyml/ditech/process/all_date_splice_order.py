
with open('d:/ditech/all_date_splice.csv', 'r') as file:
    lines = file.readlines()

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    rlines = file.readlines()

results = []
for index, line in enumerate(lines):
    rlst = rlines[index].strip().split(',')
    lst = line.strip().split(',')
    result = []
    result.append(lst[0])
    result.append(lst[1])
    for i in range(144):
        result.append(int(lst[i+2]) - int(rlst[i+2]))

    results.append(','.join(map(lambda x:str(x), result)))

with open('d:/ditech/all_date_splice_order.csv', 'wb') as file:
    file.writelines('\n'.join(results))
