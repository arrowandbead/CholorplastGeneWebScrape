#solvedProblem children
#matkGenus found and rcblGenus Found
from shutil import copyfile

def getGenusFromGenusFound(line):
    split = line[:-1].split(',')
    return(split[0])
def getSpeciesFromGenusFound(line):
    split = line[:-1].split(',')
    return( (split[0], split[1]))

copyfile("finalMatkMeta.csv", "finalMatkMetaCopy.csv")
finalMatkMeta = open("finalMatkMetaCopy.csv", "a")
copyfile("finalMatkFasta.fa", "finalMatkFastaCopy.fa")
finalMatkFasta = open("finalMatkFastaCopy.fa", "a")

copyfile("finalRcblMeta.csv", "finalRcblMetaCopy.csv")
finalRcblMeta = open("finalRcblMetaCopy.csv", "a")
copyfile("finalRcblFasta.fa", "finalRcblFastaCopy.fa")
finalRcblFasta = open("finalRcblFastaCopy.fa", "a")
genusInProblemChildrenMatk = set()

solvedMatkMeta = open("solvedProblemChildrenMatkMeta.txt", "r")
currLine = solvedMatkMeta.readline()
while currLine != "":
    genus = getGenusFromGenusFound(currLine)
    genusInProblemChildrenMatk.add(genus)
    finalMatkMeta.write(currLine)
    currLine = solvedMatkMeta.readline()

solvedMatkFasta = open("solvedProblemChildrenMatkFasta.txt", "r")
finalMatkFasta.write('\n\n')
currLine = solvedMatkFasta.readline()
while currLine != "":
    finalMatkFasta.write(currLine)
    currLine = solvedMatkFasta.readline()

genusInProblemChildrenRcbl = set()

solvedRcblMeta = open("solvedProblemChildrenRcblMeta.txt", "r")
currLine = solvedRcblMeta.readline()
while currLine != "":
    genus = getGenusFromGenusFound(currLine)
    genusInProblemChildrenRcbl.add(genus)
    finalRcblMeta.write(currLine)
    currLine = solvedRcblMeta.readline()

solvedRcblFasta = open("solvedProblemChildrenRcblFasta.txt", "r")
finalRcblFasta.write('\n\n')
currLine = solvedRcblFasta.readline()
while currLine != "":
    finalRcblFasta.write(currLine)
    currLine = solvedRcblFasta.readline()


matkGenusFoundMeta = open("matkGenusFoundMeta.txt", "r")
num = 0
currLine = matkGenusFoundMeta.readline()
while currLine != "":
    genus = currLine.split(',')[0]
    if genus not in genusInProblemChildrenMatk:
        num += 1
        finalMatkMeta.write("None,None,genus," + currLine)
    currLine = matkGenusFoundMeta.readline()
print("num matkGenusFound added to meta: " + str(num))
num = 0
matkGenusFoundFasta = open("matkGenusFoundFasta.txt", "r")
currLine = matkGenusFoundFasta.readline()
while currLine != "":
    if(currLine[0] == '>'):
        genus = currLine.strip('>').split('_')[0]
        if genus not in genusInProblemChildrenMatk:
            num += 1
            finalMatkFasta.write(currLine)
            finalMatkFasta.write(matkGenusFoundFasta.readline() + '\n')
    currLine = matkGenusFoundFasta.readline()
print("num matkGenusFound added to fasta: " + str(num))
num = 0

rcblGenusFoundMeta = open("rcblGenusFoundMeta.txt", "r")
currLine = rcblGenusFoundMeta.readline()
while currLine != "":
    genus = currLine.split(',')[0]
    if genus not in genusInProblemChildrenRcbl:
        num +=1
        finalRcblMeta.write("None,None,genus," + currLine)
    currLine = rcblGenusFoundMeta.readline()
print("num rcblGenusFound added to meta: " + str(num))
num = 0
rcblGenusFoundFasta = open("rcblGenusFoundFasta.txt", "r")
currLine = rcblGenusFoundFasta.readline()
while currLine != "":
    if(currLine[0] == '>'):
        genus = currLine.strip('>').split('_')[0]
        if genus not in genusInProblemChildrenRcbl:
            num += 1
            finalRcblFasta.write(currLine)
            finalRcblFasta.write(rcblGenusFoundFasta.readline() + '\n')
    currLine = rcblGenusFoundFasta.readline()
print("num rcblGenusFound added to fasta: " + str(num))
