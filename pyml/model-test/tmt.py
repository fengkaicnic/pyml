
with open('d:/bimbo/test.csv', 'r') as file:
    for i in range(19):
        line = file.readline()
        lst = line.split(',')
        print line
