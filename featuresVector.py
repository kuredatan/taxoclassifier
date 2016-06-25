#Creates for each patient the corresponding features vector, that is:
#@name: name of sample/patient
#for each metadatum, (metadatum,value for this patient in the data matrix)
#a list of couples (node,ID of read such as node matches this read)
#(this is more efficient than an array of all nodes)

#Returns a list of features vectors
def featuresCreate(sampleInfoList,infoList):
    featuresVectorList = []
    for sample in sampleInfoList:
        n = len(sample)
        if n < 1:
            print "\n/!\ ERROR: Sample info incorrect."
            raise ValueError
        #@name of sample
        featuresVector = [sample[0]]
        for i in range(1,n):
            featuresVectorList.append(infoList[i],sample[i])
        featuresVectorList.append(featuresVector)
    return featuresVectorList
