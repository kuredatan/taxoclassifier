 #for training


#Computes classes according to metadata values
def computeClasses(dataArray,metadataList):
    ()

 #Training step #1: selects a random subset of the set of samples
def selectTrainingSample(dataArray):
    ()

#Training step #2: according to metadata, assign a class to each sample of this subset
def assignClass(dataArray,trainSubset,classes,metadataList):
    ()

#Training step #3: computes expectation and standard deviation for the different criterias over nodes for each class
def computeExpect(dataArray,assignedClasses,nodesList):
    ()

    
def trainingPart(dataArray,metadataList,nodesList):
    classes = computeClasses(dataArray,metadataList)
    trainSubset = selectTrainingSample(dataArray)
    assignedClasses = assignClass(dataArray,trainSubset,classes,metadataList)
    valuesClasses = computeExpect(dataArray,assignedClasses,nodesList)
    return valuesClasses
    
