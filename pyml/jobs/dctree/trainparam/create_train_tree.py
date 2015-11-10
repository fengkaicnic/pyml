from jobs.dctree.trainparam import degreetree

if __name__ == '__main__':
    #if len(sys.argv) != 3:
    #    print "please use: python decision.py train_file test_file"
    #    sys.exit()
    train_file = 'd:/jobs/dctree/degree/trainparam.csv'
    test_file = 'd:/jobs/dctree/degree/testparam.csv'
    #run(train_file,test_file)
    degreetree.run(train_file, test_file, 0.020)
    degreetree.test(train_file, test_file, 'result020.txt')
    degreetree.run(train_file, test_file, 0.021)
    degreetree.test(train_file, test_file, 'result021.txt')
    degreetree.run(train_file, test_file, 0.022)
    degreetree.test(train_file, test_file, 'result022.txt')
    degreetree.run(train_file, test_file, 0.023)
    degreetree.test(train_file, test_file, 'result023.txt')
    degreetree.run(train_file, test_file, 0.024)
    degreetree.test(train_file, test_file, 'result024.txt')
    degreetree.run(train_file, test_file, 0.025)
    degreetree.test(train_file, test_file, 'result025.txt')
    degreetree.run(train_file, test_file, 0.026)
    degreetree.test(train_file, test_file, 'result026.txt')
    degreetree.run(train_file, test_file, 0.027)
    degreetree.test(train_file, test_file, 'result027.txt')
    degreetree.run(train_file, test_file, 0.028)
    degreetree.test(train_file, test_file, 'result028.txt')
    degreetree.run(train_file, test_file, 0.029)
    degreetree.test(train_file, test_file, 'result029.txt')
    degreetree.run(train_file, test_file, 0.030)
    degreetree.test(train_file, test_file, 'result030.txt')