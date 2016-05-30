import os
from collections import Counter
import re
import math

pathtocandidatefile = "C:\\USC\\Applied Natural Language Processing\\Assignments\\8_BLEUScore_MachineTranslationEvaluation\\candidate-4.txt"
pathtoreferencedirectory = "C:\\USC\\Applied Natural Language Processing\\Assignments\\8_BLEUScore_MachineTranslationEvaluation\\reference-4"
listofreferencefiledata = []
candidatefiledata = []
# Parameters
wn = float(1)/float(4)
PrecisionofAllNGrams = 0
ValueofC = 1
BP = 1

def getWordsinFileByLine(filename):
    listofwordsbyline=[]
    with open(filename, "rb") as f:
        for line in f.readlines():
            wordsinline = []
            for word in line.split():
                wordsinline.append(word)
            listofwordsbyline.append(wordsinline)
#     print listofwordsbyline
    return listofwordsbyline

def getCandidateandReferenceFileData():
    global candidatefiledata
    global listofreferencefiledata
    
    with open(pathtocandidatefile, "rb") as f:
        candidatefiledata = getWordsinFileByLine(pathtocandidatefile)
        
    if os.path.isdir(pathtoreferencedirectory):
        for subdir, dirs, files in os.walk(pathtoreferencedirectory):
            for filename in files:
                listofreferencefiledata.append(getWordsinFileByLine(os.path.join(subdir, filename)))
    else:
        listofreferencefiledata.append(getWordsinFileByLine(pathtoreferencedirectory))
        
def getNGramContent(listofwordsinfilebyline, n):
    d = {}
    str = ""
    ListofNGramsAndCountInFileByLine = []
    for wordsinline in listofwordsinfilebyline:
        d = {}
        lengthofline = len(wordsinline)
        for i in range(0, lengthofline-n+1):
            str=""
            for j in range(i, i + n):
                str += wordsinline[j]
            if str in d:
                d[str] += 1
            else: 
                d[str] = 1
        ListofNGramsAndCountInFileByLine.append(d)
    return ListofNGramsAndCountInFileByLine

def calculateModifiedPrecisionPn():
    global ValueofC
    ModifiedPrecisionPn = 0    
    for n in range(1, 5):
        CandidateFileNGramData = getNGramContent(candidatefiledata, n)
        ReferenceFilesNGramData = [] 
        for referencefiledata in listofreferencefiledata: 
            ReferenceFilesNGramData.append(getNGramContent(referencefiledata, n))
        numerator = 0 
        denominator = 0
        for i in range(0, len(CandidateFileNGramData)):
#             print i
            for word, count in CandidateFileNGramData[i].iteritems():
                denominator += count            
                maxmatchcount = 0            
                for referencefile in ReferenceFilesNGramData:
                    if word not in referencefile[i]:
                        val = 0
                    else:
                        val = referencefile[i][word]
                    if(maxmatchcount < val):
                        maxmatchcount = val
                if count < maxmatchcount:
                    numerator += count
                else: 
                    numerator += maxmatchcount
#         print str(numerator)+"n - " + str(n)+"--" + str(denominator) 
#         print str((numerator * 1.0) / denominator) + "P" + str(n)
        ModifiedPrecisionPn += (math.log(float(numerator)/float(denominator)))/4
        if(n == 1):
            ValueofC = denominator
    return ModifiedPrecisionPn
   
def calculateR():
    R = 0
    for i in range(0, len(candidatefiledata)):
#         print candidatefiledata
        CountInCandidateFile = len(candidatefiledata[i])
#         print len(candidatefiledata[i])
        CountInReferenceFile = 0
        matchedlength = 0
        diff = float("inf")
        for referencefile in listofreferencefiledata:
            CountInReferenceFile = len(referencefile[i])
#             print referencefile[i]
#             print CountInReferenceFile
            if diff > (CountInReferenceFile - CountInCandidateFile):
                diff = CountInReferenceFile - CountInCandidateFile
                matchedlength = CountInReferenceFile
#         print str(matchedlength)+"matched"
        R += matchedlength
#     print "r - " +str(R)
    return R
                
        
def calculateBP():
    global BP
#     print "BP"
#     print ValueofC
#     print ValueofR
    if ValueofC <= ValueofR:
        BP = math.exp(1 - (ValueofR * 1.0/ValueofC))
#     print str(BP)+"BP"  
    return BP



def calculateBlueScore(BP):
    bluescore = BP * math.exp(PrecisionofAllNGrams)
    return bluescore

getCandidateandReferenceFileData()
PrecisionofAllNGrams = calculateModifiedPrecisionPn()
ValueofR = calculateR()
BP = calculateBP()
BlueScore = calculateBlueScore(BP)
# print "BlueScore" + str(BlueScore)
with open("bleu_out.txt", "wb") as f:
    f.write(str(BlueScore))

