from selenium import webdriver
import BSStuff
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import partialSupport


import automatedDealWithPages

driver = webdriver.Chrome(executable_path='/Users/malcolmmeyerson/Documents/chloroPlastGenScrape/chromedriver')

moreProblems = open("outputFiles/moreProblems.txt")
matk = True
matkProblems = set()
rcblProblems = set()
for line in moreProblems:
    if(line == 'rbcL\n'):
        print("dsad")
        matk = False
    if '_' not in line:
        continue
    split = line.strip(">#").split('_')
    yuple = (split[0], split[1])
    if(matk):
        matkProblems.add(yuple)
    else:
        rcblProblems.add(yuple)

usedSpecies = set()
moreProblemsRcblFasta = open("moreProblemsRcblFasta.txt", "w+")
moreProblemsRcblMeta = open("moreProblemsRcblMeta.txt", "w+")
for line in rcblProblems:
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
        moreProblemsRcblMeta.write(csvReturnString + '\n')
        moreProblemsRcblFasta.write('>' + result['speciesTuple'][0] + '_' + result['speciesTuple'][1] + '_' + result['version'] + '\n' + processedFasta + '\n' + '\n')

moreProblemsMatkFasta = open("moreProblemsMatkFasta.txt", "w+")
moreProblemsMatkMeta = open("moreProblemsMatkMeta.txt", "w+")
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
        moreProblemsMatkMeta.write(csvReturnString + '\n')
        moreProblemsMatkFasta.write('>' + result['speciesTuple'][0] + '_' + result['speciesTuple'][1] + '_' + result['version'] + '\n' + processedFasta + '\n' + '\n')
