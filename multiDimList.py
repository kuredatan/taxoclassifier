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
        mdl = MultiDimList(None,shape)
        #########################################################
    #
    #
    def modifyMDL(self,dimList,newValue):
        if not self.shape:
            print "\n/!\ ERROR: Empty list."
            raise ValueError
        if not (len(dimList) == len(self.shape)):
            print "\n/!\ ERROR: Cannot access this multi-dimensional list."
            raise ValueError
        lsList = []
        mdl = []
        for x in self.
        for dim in dimList:
            n = len(lsList[-1])
            if dim > n or 0 > dim:
                print "\n/!\ Dimension error."
                raise ValueError
            newLs = []
            if isinstance(lsList[-1][dim],list):
                for x in lsList[-1][dim]:
                    newLs.append(x)
                lsList.append(newLs)
        dimList = dimList[::-1]
        while lsList and dimList:
            ls = lsList.pop()
            ls[dimList[-1]] = newValue
            newValue = []
            for x in ls:
                newValue.append(x)
            _ = dimList.pop()
        return ls

#If a1, a2, a3, ..., ap are the elements of @mdl (in a certain order)
#Returns [ f(a1), f(a2), ..., f(ap) ]
def mapMDL(mdl,shape,f):
    resultList = []
    limitDim = []
    for dim in shape:
        limitDim.append(dim)
    for dim in limitDim:
        ()
    return 0

    
def test():
    ls = MultiDimList(0,[2,3])
    print ls.mdList
    t = ls.accessMDL([0,0])
    print t
    ls = ls.modifyMDL([1,2],4)
    return ls
