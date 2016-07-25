1import sys as s
import subprocess as sb
from time import time

from parsingInfo import parseInfo
from actions import userNodeSelectionAct,randomSubSamplingAct,parseList
from featuresVector import featuresCreate
from misc import mergeList
from preformat import process

#/!\ The list of samples ID is supposed to be the same as the list of .match files! Each .match file must correspond to one single sample!

def main():
    iMatrix = raw_input("Write down the CSV file name of the data matrix in the folder \"meta\" [ without the extension .csv ]\n")
    if (iMatrix == ""):
        iMatrix = "Info"
    fastaFileName = raw_input("Write down the FASTA file names in the folder \"meta\" [ without the extension .fasta ]\n")
    if (fastaFileName == ""):
        fastaFileName = "GREENGENES_gg16S_unaligned_10022015"
    print "/!\ Data getting parsed..."
    try:
        samplesInfoList,infoList = parseInfo(iMatrix)
        filenames = [sample[0] for sample in samplesInfoList]
    except IOError:
        print "\nERROR: Maybe the filename",iMatrix,".csv does not exist in \"meta\" folder.\n"
        s.exit(0)
    print "-- End of parsing\n"
    sb.call("ls ./meta/match > sampleidlist",shell=True)
    sampleidlist = sb.check_output("sed 's/.match//g' sampleidlist | sed 's/testfiles//g' | sed '/^$/d'",shell=True).split()
    sb.call("rm -f sampleidlist",shell=True)
    result = sb.check_output("ls ./meta/match/testfiles",shell=True)
    if not result:
        print "/!\ Pre-processing files for parsing..."
        process(sampleidlist)
        print "/!\ Pre-processing done."
    print "/!\ Constructing the features vectors..."
    sampleList = mergeList(sampleidlist,filenames)
    try:
        matchingNodes,idSequences,_,_ = featuresCreate(sampleList,fastaFileName)
    except ValueError:
        print "/!\ ERROR: Please look at the line above."
        print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
        s.exit(0)
    print "-- End of construction\n"
    dataArray = [samplesInfoList,infoList,idSequences,sampleList,matchingNodes]
    answer = ""
    while not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
        try:
            print "What do you want to do?"
            print "[Write down the number matching with the action required. Details are in README file]"
            print "   1: User node selection"
            print "   2: Random sub-sampling"
            print "[To quit, write down exit]"
            answer = raw_input("Your answer?\n")
            if (answer =="1"):
                userNodeSelectionAct(dataArray)
                print "-- End \n"
            elif (answer == "2"):
                randomSubSamplingAct(dataArray)
                print "-- End \n"
            elif not ((answer == "exit") or (answer == "exit()") or (answer == "quit")):
                print "\n/!\ ERROR: Please enter a number between 1 and 2 included, or 'exit' if you want to quit."
                raise ValueError
        except ValueError:
            print "/!\ ERROR: Please look at the line above."
            print "/!\ ERROR: If the line above is blank, it may be an uncatched ValueError.\n"
