from parsingMatch import parseAllMatch
from parsingFasta import parseFasta

#Creates for each patient the corresponding features vector, that is:
#@name: name of sample/patient
#for each metadatum, (metadatum,value for this patient in the data matrix)
#a list of couples (node,ID of read such as node matches this read)
#(this is more efficient than an array of all nodes)

def getCorrespondingID(sequenceID,idSequences):
    i = 0
    n = len(idSequences)
    while i < n and not idSequences[i] == sequenceID:
        i += 1
    if (i == n):
        print "\n/!\ ERROR: sequence not in idSequences."
        raise ValueError
    return i

#Returns a list of features vectors
def featuresCreate(sampleInfoList,infoList,filenames=["BC_M0_good","DC_M0_good","GC_M0_good","TR_M0_good","BC_M3_good","DC_M3_good","GC_M3_good","TR_M3_good","BJ_M0_good","EY_M0_good","GM_M0_good","BJ_M3_good","EY_M3_good","GM_M3_good"],fastaFileName="GREENGENES_gg16S_unaligned_10022015"):
    featuresVectorList = []
    idPatients,allMatches = parseAllMatch(filenames)
    idSequences,phyloSequences = parseFasta(FastaFileName)
    #Link between file name and sample name?
    #As it is for now unknown, @featuresCreate returns the features vector list @featuresVectorList
    #+ the list of couples (node,ID reads) apart @matchingSequences
    for sample in sampleInfoList:
        n = len(sample)
        if n < 1:
            print "\n/!\ ERROR: Sample info incorrect."
            raise ValueError
        #@name of sample
        featuresVector = [sample[0]]
        metadataList = []
        for i in range(1,n):
            metadataList.append((infoList[i],sample[i]))
        featuresVector += metadataList
        featuresVectorList.append(featuresVector)
    n = len(allMatches)
    #For each patient @idPatient[i]
    matchingSequences = []
    for i in range(n):
        matching = [idPatient[i]]
        
    return featuresVectorList
