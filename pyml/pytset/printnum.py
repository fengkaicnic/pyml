def printNumber(numlst):
    beginning0 = True
    length = len(numlst)
    num = 0
    for i in range(length):
        if numlst[i] != '0':
            break
        num += 1
        
    print ''.join(numlst[num:length])
    #for i in range(length):
    #    if beginning0 and numlst[i] != '0':
    #        beginning0 = False
    #    if not beginning0:
    #        print numlst
            
def Print1ToMaxOfNDigitsRecursively(numlst, length, index):
    if index == length:
        printNumber(numlst)
        return 
    for i in range(10):
        numlst[index] = str(i)
        Print1ToMaxOfNDigitsRecursively(numlst, length, index+1)
        
def Print1ToMaxOfNDigit3(n):
    if n<0:
        return
    numlst = ['\0' for i in xrange(n)]
    #for i in xrange(10):
    #    numlst[0] = str(i)
    Print1ToMaxOfNDigitsRecursively(numlst, n, 0)
        

Print1ToMaxOfNDigit3(3)