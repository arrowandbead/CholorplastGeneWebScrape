def getUsedSpecies(split):
    return( (split[3], split[4]) )
def getVersion(split):
    return split[5]
def getVersionFasta(split):
    return split[2]

# finalMatkMeta = open("finalMatkMeta.csv", "w+")
# finalMatkFasta = open("finalMatkFasta.fa", "w+")

finalRcblMeta = open("finalRcblMeta.csv", "w+")
finalRcblFasta = open("finalRcblFasta.fa", "w+")

firstPassMatkMeta = open("outputFiles/firstPassResults/matk_meta.csv", "r")
firstPassMatkFasta = open("outputFiles/firstPassResults/matk.fa", "r")
firstPassRcblMeta = open("outputFiles/firstPassResults/rbcl_meta.csv", "r")
firstPassRcblFasta = open("outputFiles/firstPassResults/rbcl.fa", "r")

versionsToRetain = set()
usedSpecies = set()
currLine = firstPassRcblMeta.readline()
while currLine != "":

    split = currLine.split(',')
    species = getUsedSpecies(split)
    version = getVersion(split)
    if(species not in usedSpecies):
        usedSpecies.add(species)
        versionsToRetain.add(version)
        finalRcblMeta.write(currLine)
    currLine = firstPassRcblMeta.readline()
currLine = firstPassRcblFasta.readline()
currFastaSequence = ""

readFasta = True
newText = ""
while(currLine != ""):
    if currLine[0] == '>':
        split = currLine.strip('\n').split('_')
        version = getVersionFasta(split)
        if version in versionsToRetain:
            newText += currLine
            readFasta = True
    elif currLine[0] == '\n':
        if newText != "":
            finalRcblFasta.write(newText + '\n' + '\n')
            readFasta = False
            newText = ""
    else:
        if(readFasta):
            newText+=currLine.strip('\n')
    currLine = firstPassRcblFasta.readline()
finalRcblFasta.write(newText)
