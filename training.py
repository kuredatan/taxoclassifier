from __future__ import division

#for training part in classification
from misc import partitionSampleByMetadatumValue
from randomSampling import randomChoice
import numpy as np
from multiDimList import MultiDimList

#@dataArray = [samplesInfoList,infoList,idSequences,sampleList,matchingNodes]

#Computes classes according to metadatum values
#Returns the MDL @classes of the expected partition of the set of samples by values of metadata
def computeClasses(dataArray,metadata):
    #@clustersOneMetadatum[i] is a list of classes according to the value of metadatum @metadata[i]
    #@valueSets[i] is the set of (known) values of @metadata[i] 
    clustersOneMetadatum,valueSets = [],[]
    for metadatum in metadata:
        valueSet,classes = partitionSampleByMetadatumValue(metadatum,dataArray[1],dataArray[0])
        if not valueSet:
            print "\n/!\ ERROR: metadatum",metadatum,"having abnormal values."
            raise ValueError
        valueSets.append(valueSet)
        clustersOneMetadatum.append(classes)
    shape = []
    n = len(valueSets)
    for valueSetID in range(n):
        shape.append(len(valueSets[valueSetID]))
    #Initializing the list with empty classes
    classes = MultiDimList([],shape)
    #@classes is a list containing partition of the samples ID according to the value of the metadata
    #@dataArray[3] = sampleList
    for sample in dataArray[3]:
        #path to the class of this sample in @classes
        dimList = []
        #n = len(valueSets) = len(clustersOneMetadatum) = len(metadata) = len(shape)
        for clustersID in range(n):
            i = 0
            while i < shape[clustersID] and not (clustersOneMetadatum[clustersID] == sample):
                i += 1
            if i == shape[clustersID]:
                #Sample not in partition: must have an unknown value
                print "Sample",sample,"not in partition."
            else:
                dimList.append(i)
        #Assigns the sample to its corresponding class
        previousClass = classes.accessMDL(dimList)
        classes = classes.modifyMDL(dimList,previousClass + [sample])
    return classes,valueSets

#______________________________________________________________________________________________________

#Training step #1: selects a random subset of the set of features vectors (samples)
#knuth=True uses Knuth's algorithm S, knuth=False uses Algorithm R
def selectTrainingSample(dataArray,n,knuth=False):
    #@dataArray[3] = sampleList
    trainSubset,unchosen = randomChoice(dataArray[3],n,knuth)
    return trainSubset,unchosen

#______________________________________________________________________________________________________

#Training step #2: according to the values of metadata, assigns a class to each sample of the training subset ONLY
#@classes (see @computeClasses) is the known partition of the whole set of samples ID, that will be useful to
#compute the Youden's J coefficient
#returns @assignedClasses that is the partial partition of the set of samples restricted to the samples in @trainSubset
def assignClass(trainSubset,classes):
    classLength = classes.mapIntoListMDL(len)
    assignedClasses = MultiDimList([],classes.shape)
    for sampleID in trainSubset:
        dimList = classes.searchMDL(sampleID)
        #if sampleID is in @classes
        if dimList:
            #assigns sampleID in the corresponding class
            previousClass = classes.accessMDL(dimList)
            classes = classes.modifyMDL(dimList,previousClass + [sampleID])
    return assignedClasses

#______________________________________________________________________________________________________

#Training step #3: computes the prior probability (also called posterior probability)
#of a certain node n of being in the whole training subset using Bayesian average (to deal with zero probabilities)

#Computes mean for a list of integer values
def computeMean(vList):
    n = len(vList)
    s = 0
    for v in vList:
        s += v
    return 1/n*s

#Returns an array @probList such as @probList[i] is the probability of having node @nodesList[i]
#See report at section about Bayesian average for formula below
def getPriorProbability(nodesList,trainSubset,dataArray):
    probList = []
    #The number of nodes being both in @nodesList and in the matching lists of samples in the training set
    numberNodesInTrainSubset = 0
    numberNodes = len(nodesList)
    numberSstart = len(trainSubset)
    #matchingNodes = @dataArray[4] is a dictionary of (key=name of sample,value=list of nodes matching in sample) pairs
    n = len(dataArray[4])
    #@nodesPresence is a list such as @nodesPresence[i][j] = 1 if node nodesList[i] matches in sample matchingNodes[j][0]
    #@dataArray[8] = @matchingNodes
    nodesPresence = [[0]*n]*numberNodes
    #@nodesPositive is a list such as @nodesPositive[i] is the number of samples in the training subset containing node @nodesList[i]
    nodesPositive = [0]*numberNodes
    for sample in trainSubset:
        nodesSampleList = dataArray[4].get(sample)
        i = 0
        for node in nodesList:
            nodesPresence[i][j] = int((node in nodesSampleList))
            #if @nodesPresence[i][j] == 1
            if nodesPresence[i][j]:
                nodesPositive[i] += 1
                numberNodesInTrainSubset += 1
            i += 1
    for i in range(numberNodes):
        M = nodesPositive[i]/numberSstart
        v = 0
        for j in range(numberSstart):
            v += (nodesPresence[i][j]-M)*(nodesPresence[i][j]-M)
        v = np.sqrt(v)
        c = numberSstart/(2*(v+1))
        m = c/numberSstart
        probList.append((c*m+nodesPositive[i])/(c+numberSstart))
    return probList,nodesPresence

#Returns @classes, which is the partition of the whole set of samples according to the values of metadatum
#and @assignedClasses the partial partition of the training subset of samples
#and @valuesClasses is the list of lists of (expectation,standard deviation) pairs for each node considered
#and @unchosen is the set of remaining samples to cluster
def trainingPart(dataArray,metadatum,nodesList,numberStartingSamples):
    n = len(nodesList)
    classes,valueSets = computeClasses(dataArray,metadatum)
    trainSubset,unchosen = selectTrainingSample(dataArray,numberStartingSamples)
    probList,nodesPresence = getPriorProbability(nodesList,trainSubset,dataArray)
    assignedClasses = assignClass(trainSubset,classes)
    return classes,valueSets,assignedClasses,unchosen,probList,nodesPresence
    
