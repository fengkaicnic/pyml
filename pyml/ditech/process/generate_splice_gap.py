#generate splice gap
#for 46 gaps

splice = 46
results = []
with open('d:/ditech/all_date_splice.csv', 'r') as file:
    lines = file.readlines()

with open('d:/ditech/all_date_gap_splice.csv', 'r') as file:
    tlines = file.readlines()

for i in range(len(lines)):
    lst1 = lines[i].strip().split(',')
    srst1 = lst1[:2] + lst1[splice-2:splice+2]
    lst2 = tlines[i].strip().split(',')
    srst2 = lst2[:2] + lst2[splice-2:splice+2]
    results.append(','.join(srst1))
    results.append(','.join(srst2))

with open('d:/ditech/all_date_%d' % splice, 'wb') as file:
    file.writelines('\n'.join(results))
