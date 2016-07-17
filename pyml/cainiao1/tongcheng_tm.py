import time

results = []
with open('d:/cainiao/tongcheng.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for index, line in enumerate(lines.split('\r')):
        if not index:
            results.append(line.strip())
        else:
            lst = line.strip().split(',')
            lst[3] = (int(lst[3].split(':')[0]) - 8)*60 + int(lst[3].split(':')[1])
            lst[4] = (int(lst[4].split(':')[0]) - 8)*60 + int(lst[4].split(':')[1])
            results.append(','.join(map(lambda x:str(x), lst)))

with open('d:/cainiao/tongcheng_tm.csv', 'wb') as file:
    file.writelines('\n'.join(results))
            