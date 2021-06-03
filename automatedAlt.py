import SpeciesListParser
import partialSupport
from automatedDealWithPages import tryScrapeFor
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import traceback
from thing import getRowsToReexamine, getGenusesRepresented, getVersionsUsedAlready




matkFastaFile = open("outputFiles/" + "matk.fa", "w+")
rbcLFastaFile = open("outputFiles/" + "rbcL.fa", "w+")
matk_meta_excel_file = open("outputFiles/" + "matk_meta.csv", "w+")
matk_meta_excel_file.write("extracted genus,extracted species,extracted/literature/genus,actual species,actual genus,genbank version number,voucher,sequence length" + '\n')
rbcL_meta_excel_file = open("outputFiles/" + "rbcL_meta.csv", "w+")
rbcL_meta_excel_file.write("extracted genus,extracted species,extracted/literature/genus,actual species,actual genus,genbank version number,voucher,sequence length" + '\n')
problemChildFile = open("outputFiles/" + "problemChildrenFile.csv", "w+")
problemChildFile.write("extracted genus,extracted species,protein,error" + '\n')

rowNullCheck = lambda i : i or ''
extractedDict = {}

rowsToReexamine = getRowsToReexamine("outputFiles/firstPassResults/problemChildrenFile.csv", "not found")

genusesRepresentedMatk = getGenusesRepresented("outputFiles/firstPassResults/matk.fa")
genusesRepresentedrbcL = getGenusesRepresented("outputFiles/firstPassResults/rbcl.fa")
usedmatKVersions = getVersionsUsedAlready("outputFiles/firstPassResults/matk.fa")
if("KX290988.1" in usedmatKVersions):
    print("True")
exit()
usedrcbLVersions = getVersionsUsedAlready("outputFiles/firstPassResults/rbcl.fa")

driver = webdriver.Chrome(executable_path='/Users/malcolmmeyerson/Documents/chloroPlastGenScrape/chromedriver')
WebDriverWait(driver, 100).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')


print("starting off")

for row in rowsToReexamine[0]:
    if partialSupport.primaryDictStringFromRow(row) in extractedDict:
        continue
    else:
        extractedDict[partialSupport.primaryDictStringFromRow(row)] = 1

    print(row[0].value)

    extractedDifferentFromLit = False

    if(partialSupport.primaryDictStringFromRow(row) != partialSupport.secondaryDictStringFromRow(row)):
        extractedDifferentFromLit = True

    extractedTuple = partialSupport.primarySpeciesTupleFromRow(row)
    litTuple = partialSupport.secondarySpeciesTupleFromRow(row)
    genusTuple = partialSupport.genusTupleFromRow(row)
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
        if(result == None and genusTuple[0] in genusesRepresentedMatk):
            result = "gap"
            problemChildFile.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "matk" + "," + "genus already represented" + '\n')
        else:
            print("genus isn't in there, trying to find it again: " + genusTuple[0])
            searchMetaInfo["ExtrLitGenus"] = "genus"
            result = tryScrapeFor(genusTuple, searchMetaInfo, "maturase+K", driver)
        if(result == None):
            problemChildFile.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "matk" + "," + "not found for genus" + '\n')
        elif result == "gap":
            continue
        else:
            matkFastaFile.write(result[0])
            matk_meta_excel_file.write(result[1])
            usedmatKVersions.add(result[2])
    except Exception as e:
        just_the_string = traceback.format_exc()
        print(just_the_string)
        problemChildFile.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "matk" + "," + str(e) + '\n')
driver.quit()
exit()
for row in rowsToReexamine[1]:
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
            result = tryScrapeFor(genusTuple, searchMetaInfo, "rbcL", driver)
        if(result == None):
            problemChildFile.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "rbcL" + "," + "not found" + '\n')
        else:
            rbcLFastaFile.write(result[0])
            rbcL_meta_excel_file.write(result[1])
            usedrcbLVersions.add(result[2])
    except Exception as e:
        just_the_string = traceback.format_exc()
        print(just_the_string)
        problemChildFile.write(extractedTuple[0] + "," + extractedTuple[1] + "," + "rbcL" + "," + str(e) + '\n')
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
