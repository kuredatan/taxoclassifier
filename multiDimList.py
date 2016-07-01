import copy as cp
from time import time
from misc import addOne

class MultiDimList(object):
    #
    #
    #@shape is a list of dimensions (integers)
    #Returns a multi-dimensionnal list initialized with @init's
    def __init__(self,init,shape):
        if not shape:
            return None
        mdList = init
        shape = shape[::-1]
        for dim in shape:
            if mdList == init:
                mdList = [ init for _ in range(dim) ]
            else:
                mdListsMultiplied = []
                #To avoid an expensive deepcopy
                for i in range(dim):
                    mdListCopy = []
                    for element in mdList:
                        mdListCopy.append(element)
                    mdListsMultiplied.append(mdListCopy)
                mdList = [ mdListsMultiplied[i] for i in range(dim)]
        self.mdList = mdList
        self.shape = shape[::-1]
    #
    #
    def lenMDL(self):
        length = 1
        for dim in self.shape:
            length = length*dim
        return length
    #
    #
    def accessMDL(self,dimList):
        if not self.shape:
            print "\n/!\ ERROR: Empty list."
            raise ValueError
        if not (len(dimList) == len(self.shape)):
            print "\n/!\ ERROR: Cannot access this multi-dimensional list."
            raise ValueError
        dimListCopy = [x for x in dimList[::-1]]
        shapeCopy = [dim for dim in self.shape[::-1]]
        mdl = [element for element in self.mdList]
        while dimListCopy and shapeCopy:
            dim1 = dimListCopy.pop()
            dim2 = shapeCopy.pop()
            if dim1 > dim2 or 0 > dim1:
                print "\n/!\ Dimension error: i =",dim1,"."
                raise ValueError
            mdl = mdl[dim1]
        return mdl
    #
    #
    def copyMDL(self):
        mdList = self.mdList
        shape = self.shape
        if not mdList:
            return None
        mdlObject = MultiDimList(None,shape)
        mdlObject.shape = [dim for dim in self.shape]
        mdlObject.mdList = [element for element in self.mdList]
        return mdlObject
    #
    #
    def modifyMDL(self,dimList,newValue):
        if not self.shape:
            print "\n/!\ ERROR: Empty list."
            raise ValueError
        if not (len(dimList) == len(self.shape)):
            print "\n/!\ ERROR: Cannot access this multi-dimensional list."
            raise ValueError
        dimList = dimList[::-1]
        dimListCopy = [dim for dim in dimList]
        shapeCopy = [dim for dim in self.shape[::-1]]
        mdlCopy = [cp.deepcopy(element) for element in self.mdList]
        lsList = [ mdlCopy ]
        #len(dimList) = len(shape)
        while not (len(dimList) == 1):
            dim = dimList.pop()
            shapeDim = shapeCopy.pop()
            if dim >= shapeDim:
                print "\n/!\ ERROR: dimensions do not match(1):",dim,shapeDim,"."
                raise ValueError
            mdlCopy = cp.deepcopy(mdlCopy[dim])
            lsList.append(mdlCopy)
        dim = dimList.pop()
        shapeDim = shapeCopy.pop()
        if dim >= shapeDim:
            print "\n/!\ ERROR: dimensions do not match(2):",dim,shapeDim,"."
            raise ValueError
        dimListCopy = dimListCopy[::-1]
        while dimListCopy and lsList:
            dim = dimListCopy.pop()
            lsList[-1][dim] = newValue
            newValue = lsList.pop()
        self.mdList = newValue
        return self
    #
    #
    #Pops out first element (in position [0,0,0,...,0]) of MDL
    #and returns the list of the remaining elements in the MDL
    #"column" by "column", from top to bottom
    def nextMDL(self):
        elements = []
        currDimList = [0]*len(self.shape)
        while currDimList:
            elements.append(self.accessMDL(currDimList))
            currDimList = addOne(currDimList,self.shape)
        return (elements[0],elements[1:][::-1])
    #
    #
    def searchMDL(self,element):
        currDimList = [0]*len(self.shape)
        getElement = self.accessMDL(currDimList)
        while currDimList and not (getElement == element):
            currDimList = addOne(currDimList,self.shape)
            getElement = self.accessMDL(currDimList)
        return currDimList[::-1]
    #
    #
    #If a1, a2, a3, ..., ap are the elements of @mdl (in a certain order)
    #Returns [ f(a1), f(a2), ..., f(ap) ] (we do not care about order)
    #@f takes into argument an element of the MDL
    def mapIntoListMDL(self,f):
        resultList = []
        currDimList = [0]*len(self.shape)
        while currDimList:
            element = self.accessMDL(currDimList)
            resultList.append(f(element))
            currDimList = addOne(currDimList,self.shape)
        return resultList

    
