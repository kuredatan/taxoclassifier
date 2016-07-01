from __future__ import division

from misc import mem,addOne
from training import trainingPart
from multiDimList import MultiDimList

#@dataArray = [samplesInfoList,infoList,nodesList,sampleIDList,featuresVectorList,matchingNodes]

#Computes Bayes's theorem
#Uses an hypothesis of Bernouilli naive distribution (that is, we are assuming the independance between the values of metadata) + equiprobability of being in one of the classes (that is, we are assuming that a sample can be equiprobably take one of the values of the total set of values of the metadatum), which are quite strong hypotheses (for a clearer explanation, see README)
#Returns a MDL @postMeasures containing class probabilities for each class such as @postMeasures[dimList] is the class probability for class @assignedClasses[dimList]
def probabilityKnowingClass(nodesList,assignedClasses,dataArray,numberClass,numberNodes,probList,nodesPresence,numberMatching):
    #@probKnowingClass[dimList][i] = @probKnowingClass[a1][a2][...][i] is the probability of having node @nodesList[i] knowing that sample is in class @assignedClasses[dimList]
    probKnowingClass = MultiDimList(0,assignedClasses.shape + [numberNodes])
    nod = 0
    currDimList = [0]*len(assignedClasses.shape)
    for node in nodesList:
        while currDimList:
            numberNodeInClass = 0
            numberNodeAppearsInClass = 0
            sampleClassList = assignedClasses.access(currDimList)
            for sample in sampleClassList:
                indexSample = 0
                #@dataArray[5] = @matchingNodes
                while indexSample < numberMatching and not (sample == dataArray[5][indexSample][0]):
                    indexSample += 1
                if indexSample == numberMatching:
                    print "\n/!\ ERROR: This sample",sample,"is not in matchingNodes."
                    raise ValueError
                #@nodesPresence[nod][indexSample] == 1 or 0
                numberNodeAppearsInClass += nodesPresence[nod][indexSample]
                numberNodeInClass += len(dataArray[5][indexSample][1])
            probKnowingClass = probKnowingClass.modify(currDimList + [nod],probList[nod]**numberNodeAppearsInClass + (1 - probList[nod])**(numberNodeInClass - numberNodeAppearsInClass))
            currDimList = addOne(currDimList,assignedClasses.shape)
        nod += 1
    return probKnowingClass

def bayesCalculus(sample,nodesList,dataArray,assignedClasses,numberClass,numberNodes,numberMatching,probList,nodesPresence):
    postMeasures = MultiDimList(0,assignedClasses.shape)
    if not numberClass:
        print "\n/!\ ERROR: No class assigned."
        raise ValueError
    #Equiprobability (could also be computed using the training subset, but we should have dealt with the zero probabilities)
    #with the bayesian average used for probabilities of having a node, but it would be as irrelevant, because interaction between
    #metadata values are depending on the real definition of the metadata (see data matrix)
    probBeingInClass = 1/numberClass
    #@probKnowingClass is a MDL such as, if dimList = [a1,a2, ...] is the index list for a certain class
    #@probKnowingClass[dimList][i] = @probKnowingClass[a1][a2][...][i] is the probability of having node @nodesList[i] knowing that sample is in class @assignedClasses[dimList]
    probKnowingClass = probabilityKnowingClass(nodesList,assignedClasses,dataArray,numberClass,numberNodes,probList,nodesPresence,numberMatching)
    probWithoutEvidence = MultiDimList(0,assignedClasses.shape)
    for dim in assignedClasses.shape:
        shapeCopy.append(dim)
    evidence = 0
    currDimList = [0]*len(shapeCopy)
    while currDimList:
        #product of probabilities of having a node knowing the class
        product = 1
        for nod in range(numberNodes):
            product = product*probKnowingClass.access(currDimList + [nod])
        evidence += probBeingInClass*product
        probWithoutEvidence = probWithoutEvidence.modifyMDL(currDimList,product * probBeingInClass)
        currDimList = addOne(currDimList,assignedClasses.shape)
    currDimList = [0]*len(shapeCopy)
    while currDimList:
        postMeasures = postMeasures.modifyMDL(currDimList,1/evidence * probWithoutEvidence.accessMDL(currDimList))
    return postMeasures

#Returns @assignedClasses (partition of the whole set of samples according to node population)
#and @classes (partition of the whole set of samples according to the values of metadata)
def classifyIt(dataArray,metadatum,nodesList):
    #@assignedClasses is the current partial (MDL) partition of the set of samples
    #@classes is the partition (MDL) of the whole set of samples (to compute Youden's J coefficient)
    #@unchosen is the set of samples remaining to be clustered
    #@probList is a list such as @probList[i] is the prior probability of having node @nodesList[i] in a sample
    #@nodesPresence is a list such as @nodesPresence[i][j] = 1 if node nodesList[i] matches in sample matchingNodes[j][0]
    classes,valueSets,assignedClasses,unchosen,probList,nodesPresence = trainingPart(dataArray,metadatum,nodesList)
    numberClass = classes.lenMDL()
    numberNodes = len(nodesList)
    numberMatching = len(dataArray[5])
    if not (numberClass == assignedClasses.lenMDL()):
        print "\n/!\ ERROR: Length error: classes:",numberClass,"assignedClasses",assignedClasses.lenMDL(),"."
        raise ValueError
    for sample in unchosen:
        #@postMeasures is the MDL containing class probabilities for the sample (that is, the probability that this sample is in class C knowing its node population)
        #@maxDimList is the "address" in the MDL of the highest probability
        postMeasures,maxDimList = bayesCalculus(sample,nodesList,dataArray,assignedClasses,numberClass,numberNodes,numberMatching,probList,nodesPresence,numberMatching)
        #Assigning this sample to the corresponding class
        previousClass = assignedClasses.accessMDL(maxDimList)
        assignedClasses = assignedClasses.modifyMDL(maxDimList,previousClass + [sample])
    return assignedClasses,classes,valueSets
