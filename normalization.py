#Centralization-reduction for a list of values
import numpy as np

from misc import inf

#Hypothesis of uniform probability for the occurrence of any bacteria whatever the clinic data may be (which is a strong hypothesis...)
#Returns expectation and standard deviation
def expectSTDevList(vArray):
    vProductArray = [x*x for x in vArray]
    expProd = expectList(vProductArray)
    exp = expectList(vArray)
    expS = exp*exp
    return exp,np.sqrt(expProd-expS)

def normalizeList(valueList):
    exp,stDev = expectSTDevList(valueList)
    if not stDev:
        print "\n/!\ ERROR: Math problem (Division by zero)."
        raise ValueError
    normList = []
    for value in valueList:
        normList.append((value-exp)/stDev)
    return normList
