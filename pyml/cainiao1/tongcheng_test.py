
num = 0
with open('d:/cainiao/dianshang.csv', 'r') as file:
    lines = file.readlines()
    lines = lines[0]
    for line in lines.strip().split('\r')[1:]:
        lst = line.strip().split(',')
        num += int(lst[3])

print num
        