#coding:utf8
def bag(n,c,w,v):
    res=[[-1 for j in range(c+1)] for i in range(n+1)]
    for j in range(c+1):
        res[0][j]=0
    for i in range(1,n+1):
        for j in range(1,c+1):
            res[i][j]=res[i-1][j]
            if j>=w[i-1] and res[i][j]<res[i-1][j-w[i-1]]+v[i-1]:
                res[i][j]=res[i-1][j-w[i-1]]+v[i-1]
    return res

def show(n,c,w,res):
    print(u'最大价值为:',res[n][c])
    x=[False for i in range(n)]
    j=c
    for i in range(1,n+1):
        if res[i][j]>res[i-1][j]:
            x[i-1]=True
            j-=w[i-1]
    print(u'选择的物品为:')
    for i in range(n):
        if x[i]:
            print(u'第',i,u'个,')
    print('')

if __name__=='__main__':
    n=5
    c=10
    w=[2,2,6,5,4]
    v=[6,3,5,4,6]
    res=bag(n,c,w,v)
    show(n,c,w,res)
