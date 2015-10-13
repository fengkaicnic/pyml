summ = [0]

def add_fun(n, sun):
    n and add_fun(n-1, sun)
    sun[0] = sun[0]+n
    return sun[0]

n = 101
print summ[0]
print "1+2+.....+n= %d" % add_fun(n, summ)