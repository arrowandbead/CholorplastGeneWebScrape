speciesInMatk = set()
matkMeta = open("finalMatkMetaCopy.csv", "r")
rbclMeta = open("finalRcblMetaCopy.csv", "r")
rbclInBothMeta = open("rcblInBothMeta.csv", "r")
rbclInBothFasta = open("rcblInBothFasta.fa", "r")
currRbcl = rbclInBothMeta.readline()
currFasta = rbclInBothFasta.readline()
while(currRbcl != "" and currFasta != ""):
    metaVersion = currRbcl.split(',')[5]
    fastaVersion = currFasta.strip('\n').split('_')[2]
    print(fastaVersion)
    if(metaVersion != fastaVersion):
        print(metaVersion)
        print(fastaVersion)
        exit()
    currRbcl = rbclInBothMeta.readline()
    currFasta = rbclInBothFasta.readline()
    currFasta = rbclInBothFasta.readline()
    currFasta = rbclInBothFasta.readline()
exit()
matkFasta = open("finalMatkFastaCopy.fa", "r")
currLine = matkMeta.readline()
while(currLine != ""):
    split = currLine.split(',')
    if(split[2] == 'extracted' or split[2] == 'literature'):
        speciesInMatk.add( (split[0], split[1]))
        speciesInMatk.add( (split[3], split[4]))
    currLine = matkMeta.readline()
rcblMeta = open("finalRcblMetaCopy.csv", "r")
rcblFasta = open("finalRcblFastaCopy.fa", "r")

currLine = rcblMeta.readline()
rcblInBothMeta = open("rcblInBothMeta.csv", "w+")
inBoth = set()
while(currLine != ""):
    split = currLine.split(',')
    if(split[2] == 'extracted' or split[2] == 'literature'):
        if (split[0], split[1]) in  speciesInMatk or (split[3], split[4]) in speciesInMatk:
            rcblInBothMeta.write(currLine)
            inBoth.add( (split[0], split[1]))
            inBoth.add( (split[3], split[4]))
    currLine = rcblMeta.readline()
rcblInBothFasta = open("rcblInBothFasta.fa", "w+")
rcblFasta = open("finalRcblFastaCopy.fa", "r")
currLine = rcblFasta.readline()
while(currLine != ""):
    if(currLine[0] == '>'):
        split = currLine.strip('>').split('_')
        if( (split[0], split[1]) in inBoth):
            rcblInBothFasta.write(currLine)
            rcblInBothFasta.write(rcblFasta.readline() + '\n')
    currLine = rcblFasta.readline()
matkMeta.close()
matkMeta = open("finalMatkMetaCopy.csv", "r")
currLine = matkMeta.readline()
matkInBothMeta = open("matkInBothMeta.csv", "w+")
matkInBothFasta = open("matkInBothFasta.fa", "w+")
while(currLine != ""):
    split = currLine.split(',')
    if (split[0], split[1]) in inBoth or (split[3], split[4]) in inBoth:
        matkInBothMeta.write(currLine)
    currLine = matkMeta.readline()
matkFasta.close()
matkFasta = open("finalMatkFastaCopy.fa", "r")
currLine = matkFasta.readline()
while(currLine != ""):
    if(currLine[0] == '>'):
        split = currLine.strip('>').split('_')
        if( (split[0], split[1]) in inBoth):
            matkInBothFasta.write(currLine)
            matkInBothFasta.write(matkFasta.readline() + '\n')
    currLine = matkFasta.readline()
