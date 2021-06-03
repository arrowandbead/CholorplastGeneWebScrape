matkMetaFileText = open("finalMatkMetaCopy.csv").read()
matkFastaFileText = open("finalMatkFastaCopy.fa")
rcblMetaFileText = open("finalRcblMetaCopy.csv").read()
rcblFastaFileText = open("finalRcblFastaCopy.fa")

speciesInMatk = set()
genusesInMatk = set()
speciesInRcbl = set()
genusesInRcbl = set()

matkVersionToLineMap = {}
for line in matkMetaFileText.split('\n'):
    splitLine = line.split(',')
    if(line == ""):
        continue
    if(splitLine[0] == "extracted genus"):
        print("header matk")
        continue
    matkVersionToLineMap[splitLine[5]] = splitLine
    species = (splitLine[3], splitLine[4])
    speciesInMatk.add(species)
    genusesInMatk.add(species[0])

rcblVersionToLineMap = {}
for line in rcblMetaFileText.split('\n'):
    splitLine = line.split(',')
    if line == "":
        continue
    if(splitLine[0] == "extracted genus"):
        print("header rcbl")
        continue
    rcblVersionToLineMap[splitLine[5]] = splitLine
    species = (splitLine[3], splitLine[4])
    speciesInRcbl.add(species)
    genusesInRcbl.add(species[0])

currLine = matkFastaFileText.readline()
matkVersionFastaDict = {}
while currLine != "":
    if(currLine[0] == '>'):
        splitLine = currLine.strip('>').strip('\n').split("_")
        version = splitLine[2]
        genus = splitLine[0]
        fasta = matkFastaFileText.readline().strip('\n')
        matkVersionFastaDict[genus] = (version, fasta)
    currLine = matkFastaFileText.readline()

currLine = rcblFastaFileText.readline()
rcblVersionFastaDict = {}
while currLine !="":
    if(currLine[0] == '>'):
        splitLine = currLine.strip('>').strip('\n').split("_")
        version = splitLine[2]
        genus = splitLine[0]
        fasta = rcblFastaFileText.readline().strip('\n')
        rcblVersionFastaDict[genus] = (version, fasta)
    currLine = rcblFastaFileText.readline()

outputMeta = open("ZoutputMeta.csv", "w+")
outputMatkFasta = open("ZoutputMatkFasta.fa", "w+")
outputRcblFasta = open("ZoutputRcblFasta.fa", "w+")
outputMeta.write("genus,matk species,matk version,matk voucher,matk sequence length,rcbl species, rcbl version, rcbl voucher, rcbl sequence length \n")
genusToOutputLine = {}
for genus in genusesInMatk:
    version = matkVersionFastaDict[genus][0]
    fasta = matkVersionFastaDict[genus][1]
    line = matkVersionToLineMap[version]
    outputLine = [""]*9
    outputLine[0] = genus
    outputLine[1:5] = line[4:8]
    genusToOutputLine[genus] = outputLine
    outputMatkFasta.write(">" + genus + '\n')
    outputMatkFasta.write(fasta + '\n' + '\n')

for genus in genusesInRcbl:
    version = rcblVersionFastaDict[genus][0]
    fasta = rcblVersionFastaDict[genus][1]
    line = rcblVersionToLineMap[version]
    if(genus in genusToOutputLine):
        genusToOutputLine[genus][5:9] = line[4:8]
    else:
        outputLine = [""]*9
        outputLine[0] = genus
        outputLine[5:9] = line[4:8]
        genusToOutputLine[genus] = outputLine
    outputRcblFasta.write('>' + genus + '\n')
    outputRcblFasta.write(fasta + '\n' + '\n')

for genus in genusToOutputLine:
    outputMeta.write(','.join(genusToOutputLine[genus]) + '\n')
