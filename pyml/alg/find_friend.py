import Queue

def find_friend(lst):
    q1 = Queue()
    newlst = []
    q1.push(lst[0])
    newlst.append(lst[0])
    while not q1:
        fd = q1.pop()
        for fdr in lst:
            if fdr in newlst:
                continue
            if fd[0] == fdr[0] or fd[1] == fdr[0] or fd[0] == fdr[1] or fd[1] == fdr[1]:
                q1.push(fdr)
                newlst.append(fdr)

    return newlst

if __name__ == '__main__':
    pass

