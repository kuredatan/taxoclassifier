from __future__ import division
from misc import truncate,mem
from multiDimList import MultiDimList

#Compute the TP,TN,FN,FP rates (see README)
#@n is the number of samples
#Returns the sum of J(C) for all classes C (see README)
#@classes and @assignedClasses are MDL
def countYouden(classes,assignedClasses,n):
    if not (classes.shape == assignedClasses.shape):
        print "\n/!\ ERROR: Length error : classes",classes.shape,"and assignedClasses",assignedClasses.shape,"."
        raise ValueError
    youdenCoeffList = []
    classesCopy = classes.copyMDL()
    assignedClassesCopy = assignedClasses.copyMDL()
    class1,nextClasses = classesCopy.nextMDL()
    asClass1,nextAssignedClasses = assignedClasses.nextMDL()
    while nextClasses and nextAssignedClasses:
        #@class1 and @asClass1 are lists
        tp,fp,fn = 0,0,0
        #TN = @n - FP - TP - FN
        for sample in class1:
            if mem(sample,asClass1):
                tp += 1
            else:
                fn += 1
        for sample in asClass1:
            if not mem(sample,class1):
                fp += 1
        tn = n - tp - fp - fn
        j = tp/(tp + fn) + tn/(tn + fp) - 1
        if j < -1 or j > 1:
            print "\n/!\ ERROR: Inconsistent value of Youden's J coefficient:",j,"."
            raise ValueError
        youdenCoeffList.append(j)
        class1,asClass1 = nextClasses.pop(),nextAssignedClasses.pop()
    s = 0
    for j in youdenCoeffList:
        s += j
    return s
    

def interpretIt(youdenJ):
    print youdenJ
