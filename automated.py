import SpeciesListParser
import partialSupport
from automatedDealWithPages import tryScrapeFor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import traceback
from webdriver_manager.chrome import ChromeDriverManager

driver = webdriver.Chrome(ChromeDriverManager().install())

def checkContents(thing):
    counts = {'A':0, 'G': 0, 'C': 0, 'T': 0}
    for t in thing:
        if(t in counts):
            counts[t] += 1
    total = 0
    for g in counts:
        total += counts[g]
    if(total/len(thing) < 0.75):
        return False
    return True


matkFastaFile = open("outputFiles/" + "matk.fa", "w+")
rbcLFastaFile = open("outputFiles/" + "rbcL.fa", "w+")
matk_meta_excel_file = open("outputFiles/" + "matk_meta.csv", "w+")
matk_meta_excel_file.write("extracted genus,extracted species,extracted/literature/genus,actual species,actual genus,genbank version number,voucher,sequence length" + '\n')
rbcL_meta_excel_file = open("outputFiles/" + "rbcL_meta.csv", "w+")
rbcL_meta_excel_file.write("extracted genus,extracted species,extracted/literature/genus,actual species,actual genus,genbank version number,voucher,sequence length" + '\n')
problemChildFileMatk = open("outputFiles/" + "problemChildrenFileMatk.csv", "w+")
problemChildFileMatk.write("extracted genus,extracted species,error" + '\n')
problemChildFileRCBL = open("outputFiles/" + "problemChildrenFileRCBL.csv", "w+")
problemChildFileRCBL.write("extracted genus,extracted species,error" + '\n')



rowNullCheck = lambda i : i or ''
extractedDict = {}

WebDriverWait(driver, 100).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
usedmatKVersions = set()
usedrcbLVersions = set()

usedGenusMatk = set()
usedGenusRbcl = set()


file = SpeciesListParser.createFile(r'C:\Users\14014\Documents\chloroPlastGenScrape', 'species.xlsx')

print("starting off")
start = time.time()

thing = set()
for row in file.iter_rows():
    thing.add(row)

#Download things
#If it fails try again
#check output to see if its valid output (make sure mostly AGCTs)

foundForRcbl = set()
foundForMatk = set()

i = 0
for row in thing:
    print(i/len(thing))
    i+=1
    if(partialSupport.checkFirstRow(row)):
        continue
    elif partialSupport.primaryDictStringFromRow(row) in extractedDict:
        continue
    else:
        extractedDict[partialSupport.primaryDictStringFromRow(row)] = 1



    extractedDifferentFromLit = False

    if(partialSupport.primaryDictStringFromRow(row) != partialSupport.secondaryDictStringFromRow(row)):
        extractedDifferentFromLit = True

    extractedTuple = partialSupport.primarySpeciesTupleFromRow(row)
    litTuple = partialSupport.secondarySpeciesTupleFromRow(row)
    genusTuple = partialSupport.genusTupleFromRow(row)

    print(extractedTuple)

    keepGoing = True
    numTries = 0

    while keepGoing:
        if(extractedTuple in foundForMatk):
            print("already got it for matk")
            break

        try:

            searchMetaInfo = {
                "extractedTuple" : extractedTuple,
                "ExtrLitGenus" : "extracted",
                "usedVersions" : usedmatKVersions
            }
            result = tryScrapeFor(extractedTuple, searchMetaInfo, "maturase+K", driver)

            if(result == None and extractedDifferentFromLit):
                searchMetaInfo["ExtrLitGenus"] = "literature"
                result = tryScrapeFor(litTuple, searchMetaInfo, "maturase+K", driver)
            if(result == None):
                searchMetaInfo["ExtrLitGenus"] = "genus"
                if(genusTuple in usedGenusMatk):
                    print(str(genusTuple) + " already used for matk")
                    break
                result = tryScrapeFor(genusTuple, searchMetaInfo, "maturase+K", driver)
            if(result == None):
                if(numTries == 2):
                    keepGoing = False
                    print(str(genusTuple) + " genus not found for matk")
                    if(searchMetaInfo['ExtrLitGenus'] == 'genus'):
                        usedGenusMatk.add(genusTuple)
                    problemChildFileMatk.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "not found" + '\n')
                else:
                    numTries += 1
            else:
                if(checkContents(result[0])):
                    usedGenusMatk.add(genusTuple)
                    foundForMatk.add(extractedTuple)
                    matkFastaFile.write(result[0])
                    matk_meta_excel_file.write(result[1])
                    usedmatKVersions.add(result[2])
                    keepGoing = False
                else:
                    if(numTries==2):
                        keepGoing = False
                        print("bad seq ouput for matk " + str(extractedTuple))
                        problemChildFileMatk.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "bad seq output" + '\n')
                    else:
                        numTries += 1
        except Exception as e:
            just_the_string = traceback.format_exc()
            print(just_the_string)
            if(numTries == 2):
                keepGoing = False
                problemChildFileMatk.write(extractedTuple[0] + "," + extractedTuple[1] + "," + str(e) + '\n')
            else:
                numTries += 1

    keepGoing = True
    numTries = 0

    while(keepGoing):
        if(extractedTuple in foundForRcbl):
            print("already got it for rbcl")
            break
        try:
            searchMetaInfo = {
                "extractedTuple" : extractedTuple,
                "ExtrLitGenus" : "extracted",
                "usedVersions" : usedrcbLVersions
            }
            result = tryScrapeFor(extractedTuple, searchMetaInfo, "rbcL", driver)
            if(result == None and extractedDifferentFromLit):
                searchMetaInfo["ExtrLitGenus"] = "literature"
                result = tryScrapeFor(litTuple, searchMetaInfo, "rbcL", driver)
            if(result == None):
                searchMetaInfo["ExtrLitGenus"] = "genus"
                if(genusTuple in usedGenusRbcl):
                    print(str(genusTuple) + " already used for rbcl")
                    break
                result = tryScrapeFor(genusTuple, searchMetaInfo, "rbcL", driver)
            if(result == None):
                if(numTries == 2):
                    print(str(genusTuple) + " genus not found for rcbl")
                    problemChildFileRCBL.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "not found" + '\n')
                    if(searchMetaInfo['ExtrLitGenus'] == 'genus'):
                        usedGenusRbcl.add(genusTuple)
                    keepGoing = False
                else:
                    numTries += 1
            else:
                if(checkContents(result[0])):
                    usedGenusRbcl.add(genusTuple)
                    foundForRcbl.add(extractedTuple)
                    rbcLFastaFile.write(result[0])
                    rbcL_meta_excel_file.write(result[1])
                    usedrcbLVersions.add(result[2])
                    keepGoing = False
                else:
                    if(numTries==2):
                        keepGoing = False
                        print("bad seq ouput for rcbl " + str(extractedTuple))
                        problemChildFileRCBL.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "bad seq output" + '\n')
                    else:
                        numTries += 1
        except Exception as e:
            just_the_string = traceback.format_exc()
            print(just_the_string)
            if numTries == 2:
                keepGoing = False
                problemChildFileRCBL.write(extractedTuple[0] + "," + extractedTuple[1] + "," + str(e) + '\n')
            else:
                numTries += 1
driver.quit()


    #Try extracted
        #Accept if 1100 - 1400 and species name matches
        #Find one with a voucher if you can
    #Try Lit
        #Accept if 1100 - 1400 and species name matches
        #Find one with a voucher if you can
    #Go for genus
        #Accept if 1100 - 1400
        #Find named species with voucher if u can

    #CSV Structure
        #rbcL csv
            #extracted genus, extracted species, used extracted lit or genus, actual species, actual genus, genbank accession numbers, voucher status + numbers

        #Matk csv
            #extracted genus, extracted species, used extracted lit or genus, actual species, actual genus, genbank accession numbers, voucher status + numbers
