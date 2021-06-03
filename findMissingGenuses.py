from selenium import webdriver
import BSStuff
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import partialSupport


import automatedDealWithPages

driver = webdriver.Chrome(executable_path='/Users/malcolmmeyerson/Documents/chloroPlastGenScrape/chromedriver')
usedSpecies = set()

missingGenusesMatk = set()
for line in open("missingGenusesMatk.txt"):
    genus = line[:-1]
    missingGenusesMatk.add(genus)

missingGenusesRbcl = set()
for line in open("missingGenusesRbcl.txt"):
    genus = line[:-1]
    missingGenusesRbcl.add(genus)

# matkGenusStillNotFound = open("matkGenusStillNotFound.txt", "w+")
# matkNewlyFoundMeta = open("matkGenusFoundMeta.txt", "w+")
# matkNewlyFoundFasta = open("matkGenusFoundFasta.txt", "w+")
# matkNewlyFoundMeta.write('genus, species, version, voucher, sequenceLength')

rcblGenusStillNotFound = open("rcblGenusStillNotFound.txt", "w+")
rcblNewlyFoundMeta = open("rcblGenusFoundMeta.txt", "w+")
rcblNewlyFoundFasta = open("rcblGenusFoundFasta.txt", "w+")
rcblNewlyFoundMeta.write('genus, species, version, voucher, sequenceLength')



for genus in missingGenusesRbcl:
    print(genus)
    #usedSpecies = usedSpeciesForEachGenus[genus]
    result = automatedDealWithPages.tryScrapeForAlt((genus,), usedSpecies, "matk", driver)
    if(result == None):
        rcblGenusStillNotFound.write(genus + '\n')
    else:
        fasta = BSStuff.getFastaFromURL(result['fastaLink'])
        processedFasta = ""
        splitFasta = fasta.split('\n')
        for line in splitFasta:
            if(line == "" or line == '\n'):
                continue
            if line[0] != '>':
                processedFasta += line.strip('\n')
        print(result)
        rcblNewlyFoundMeta.write(result['speciesTuple'][0] + ',' + result['speciesTuple'][1] + ',' + result['version'] + ',' + result['voucher'] + ',' + str(result['sequenceLength']) + '\n')
        rcblNewlyFoundFasta.write('>' + result['speciesTuple'][0] + '_' + result['speciesTuple'][1] + '_' + result['version'] + '\n' + processedFasta + '\n' + '\n')
driver.close()
