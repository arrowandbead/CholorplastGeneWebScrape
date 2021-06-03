from selenium import webdriver
import BSStuff
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import partialSupport


import automatedDealWithPages

driver = webdriver.Chrome(executable_path='/Users/malcolmmeyerson/Documents/chloroPlastGenScrape/chromedriver')

problemChildren = open("outputFiles/firstPassResults/problemChildrenFile.csv")
matk = True
matkProblems = set()
rcblProblems = set()
totalCount = 0
for line in problemChildren:
    split = line.split(',')
    if(split[3] != 'not found\n'):
        totalCount += 1
        if(split[2] == 'matk'):
            matkProblems.add( (split[0], split[1]) )
        else:
            rcblProblems.add( (split[0], split[1]) )
print("totalCount: " + str(totalCount))
print(len(matkProblems))
print(len(rcblProblems))
usedSpecies = set()
moreProblemsMatkFasta = open("solvedProblemChildrenMatkFasta.txt", "w+")
moreProblemsMatkMeta = open("solvedProblemChildrenMatkMeta.txt", "w+")

moreProblemsRcblFasta = open("solvedProblemChildrenRcblFasta.txt", "w+")
moreProblemsRcblMeta = open("solvedProblemChildrenRcblMeta.txt", "w+")
for line in matkProblems:
    print(line)
    #usedSpecies = usedSpeciesForEachGenus[genus]
    speciesTuple = tuple(line)
    result = automatedDealWithPages.tryScrapeForAlt(speciesTuple, usedSpecies, "matk", driver)
    if(result == None):
        print("none")
    else:
        fasta = BSStuff.getFastaFromURL(result['fastaLink'])
        processedFasta = ""
        splitFasta = fasta.split('\n')
        for line in splitFasta:
            if(line == "" or line == '\n'):
                continue
            if line[0] != '>':
                processedFasta += line.strip('\n')
        csvColumnElements = (speciesTuple[0], speciesTuple[1], "extracted", speciesTuple[0], speciesTuple[1], result["version"], result["voucher"], result["sequenceLength"])
        csvReturnString = ""
        for thing in csvColumnElements:
            csvReturnString += str(thing) + ","
        moreProblemsMatkMeta.write(csvReturnString[:-1] + '\n')
        moreProblemsMatkFasta.write('>' + result['speciesTuple'][0] + '_' + result['speciesTuple'][1] + '_' + result['version'] + '\n' + processedFasta + '\n' + '\n')
for line in rcblProblems:
    print("rcbl  " + str(line))
    speciesTuple = tuple(line)

    #usedSpecies = usedSpeciesForEachGenus[genus]
    result = automatedDealWithPages.tryScrapeForAlt(speciesTuple, usedSpecies, "matk", driver)
    if(result == None):
        print("none")
    else:
        fasta = BSStuff.getFastaFromURL(result['fastaLink'])
        processedFasta = ""
        splitFasta = fasta.split('\n')
        for line in splitFasta:
            if(line == "" or line == '\n'):
                continue
            if line[0] != '>':
                processedFasta += line.strip('\n')
        csvColumnElements = (speciesTuple[0], speciesTuple[1], "extracted", speciesTuple[0], speciesTuple[1], result["version"], result["voucher"], result["sequenceLength"])
        csvReturnString = ""
        for thing in csvColumnElements:
            csvReturnString += str(thing) + ","
        moreProblemsRcblMeta.write(csvReturnString[:-1] + '\n')
        moreProblemsRcblFasta.write('>' + result['speciesTuple'][0] + '_' + result['speciesTuple'][1] + '_' + result['version'] + '\n' + processedFasta + '\n' + '\n')
