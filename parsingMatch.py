from misc import sanitize

#Returns the list of pairs (identifier of read,list of identifiers of sequences matching this read) associated to patient whose MATCH file is @filename
def parseMatch(filename):
    allReads = []
    file_match = open("meta/match/" + filename + ".match","r")
    lines = file_match.readlines()
    file_match.close()
    #Each line corresponds to a read of this patient
    for read in lines:
        lsDirty = read.split(" ")
        lsClean = []
        #Last string is "\n"
        for string in lsDirty[:-1]:
            lsClean.append(sanitize(string))
        if len(lsClean) < 1:
            print "\n/!\ ERROR: MATCH parsing error:",len(lsClean),"."
            raise ValueError
        allReads.append((lsClean[0],lsClean[1:]))
    return allReads

#Returns the list of identifiers of patients @idPatients in the file
#and the array @allMatches such as @allMatches[i] is a pair (identifier of read,list of identifiers of sequences matching this read) associated to patient @idPatients[i]
def parseAllMatch():
    idPatients = ["BC_M0_good","DC_M0_good","GC_M0_good","TR_M0_good","BC_M3_good","DC_M3_good","GC_M3_good","TR_M3_good","BJ_M0_good","EY_M0_good","GM_M0_good","BJ_M3_good","EY_M3_good","GM_M3_good"]
    allMatches = []
    for ident in idPatients:
        allMatches.append(parseMatch(ident))
    return idPatients,allMatches
    
