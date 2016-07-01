import copy as cp
from time import time

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
        self.shape = shape
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
        shapeCopy = []
        for dim in self.shape:
            shapeCopy.append(dim)
        mdl = []
        for element in self.mdList:
            mdl.append(element)
        while dimList and shapeCopy:
            dim1 = dimList.pop()
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
        shapeCopy = []
        for dim in self.shape:
            shapeCopy.append(dim)
        mdlCopy = []
        for element in self.mdList:
            mdlCopy.append(element)
        mdlObject.shape = shapeCopy
        mdlObject.mdList = mdlCopy
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
        dimListCopy = []
        dimList = dimList[::-1]
        for dim in dimList:
            dimListCopy.append(dim)
        shapeCopy = []
        for dim in self.shape:
            shapeCopy.append(dim)
        mdlCopy = []
        for element in self.mdList:
            mdlCopy.append(cp.deepcopy(element))
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
    #TODO
    def nextMDL(self):
        if not self.shape:
            print "\n/!\ ERROR: Empty list."
            raise ValueError
        if not isinstance(self.shape,list):
            return None
        shapeCopy = []
        for dim in self.shape:
            shapeCopy.append(dim)
        mdl = []
        for element in self.mdList:
            mdl.append(element)
        lsList = [ mdl ]
        while not (len(shapeCopy) == 1):
            _ = shapeCopy.pop()
            mdl = mdl[0]
            lsList.append(mdl)
        element = mdl[0]
        lsList[-1] = mdl[1:]
        newValue = lsList.pop()
        shape = []
        if newValue and (self.shape[-1] - 1 > 1):
            self.shape = self.shape[:-1] + [ self.shape[-1] - 1 ]
        elif newValue:
            self.shape = self.shape[:-1]
        while lsList and not newValue:
            newValue = lsList.pop()[1:]
            num = self.shape[-1] - 1
            if (num >= 1):
                shape = [num] + shape
        while lsList:
            lsList[-1] = newValue
            newValue = lsList.pop()
        self.mdList = newValue
        self.shape = self.shape[0] - 1
        return element


def searchMDL(self,element):
    () #returns dimList
        
    #If a1, a2, a3, ..., ap are the elements of @mdl (from left to right and top to bottom)
    #Returns [ f(a1), f(a2), ..., f(ap) ]
def auxMapMDL(self,f,shape,mdList):
    ()
    
def mapMDL(self,f):
    ()
    
def test():
    ls = MultiDimList([],[2,3])
    ls2 = ls.copyMDL()
    t = ls.accessMDL([0,0])
    ls = ls.modifyMDL([1,2],[4])
    ls = ls.modifyMDL([0,0],[2])
    ls = ls.modifyMDL([1,1],[10])
    print ls.mdList
    print ls.nextMDL()
    print ls.mdList
    print ls.nextMDL()
    print ls.mdList
    print ls2.mdList
