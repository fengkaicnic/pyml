#statstic result lenght

with open('d:/ditech/all_date_splice.csv', 'r') as file:
    lines = file.readlines()

num = 0
for line in lines:
    if len(line.strip().split(',')) < 146:
        num += 1
        print len(line.strip().split(','))

print num

print len(lines)
