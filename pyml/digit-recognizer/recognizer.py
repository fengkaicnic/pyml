def readCSVFile(file):
    rawData=[]
    trainFile=open(path+file,'rb')
    reader=csv.reader(trainFile)
    for line in reader:
        rawData.append(line)#42001 lines,the first line is header
    rawData.pop(0)#remove header
    intData=np.array(rawData).astype(np.int32)
    return intData
    
def loadTrainingData():
    intData=readCSVFile("train.csv")
    label=intData[:,0]
    data=intData[:,1:]
    data=np.where(data>0,1,0)#replace positive in feature vector to 1
    return data,label

def loadTestData():
    intData=readCSVFile("test.csv")
    data=np.where(intData>0,1,0)
    return data

def handwritingClassTest():
    #load data and normalization
    trainData,trainLabel=loadTrainingData()
    testData=loadTestData()
    testLabel=loadTestResult()
    #train the rf classifier
    clf=RandomForestClassifier(n_estimators=1000,min_samples_split=5)
    clf=clf.fit(trainData,trainLabel)#train 20 objects
    m,n=np.shape(testData)
    errorCount=0
    resultList=[]
    for i in range(m):#test 5 objects
         classifierResult = clf.predict(testData[i])
         resultList.append(classifierResult)
    saveResult(resultList)
    
