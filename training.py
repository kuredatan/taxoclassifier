#for training part in classification
from normalization import expectSTDevList
from misc import partitionSampleByMetadatumValue
from randomSampling import randomChoice

#dataArray = [samplesInfoList,infoList,paths,n,nodesList,taxoTree,sampleIDList,featuresVectorList,matchingSequences]

#Computes classes according to metadata values
def computeClasses(dataArray,metadataList):
    valueSets = []
    classesNumber = 1
    for metadatum in metadataList:
        valueSet,_ = partitionSampleByMetadatumValue([metadatum],dataArray[1],dataArray[0])
        if not valueSet:
            print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
            raise ValueError
        valueSets.append(valueSet)
        classesNumber = classesNumber*len(valueSet)
    classes = [[]]*classesNumber
    for valueSet in valueSets:
        n = len(valueSet)
        #classesNumber mod n == 0 by definition
        number = classesNumber/n
        i = 0
        

 #Training step #1: selects a random subset of the set of features vectors (samples)
 #knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    return randomChoice(dataArray[7],n,knuth)

#Training step #2: according to metadata, assign a class to each sample of this subset
def assignClass(dataArray,trainSubset,classes,metadataList):
    ()

#Training step #3: computes expectation and standard deviation for the different criterias over nodes for each class
def computeExpect(dataArray,assignedClasses,nodesList):
    ()
    
def trainingPart(dataArray,metadataList,nodesList):
    classes = computeClasses(dataArray,metadataList)
    #len(classes): enough? 
    trainSubset = selectTrainingSample(dataArray,len(classes))
    assignedClasses = assignClass(dataArray,trainSubset,classes,metadataList)
    valuesClasses = computeExpect(dataArray,assignedClasses,nodesList)
    return valuesClasses
    
