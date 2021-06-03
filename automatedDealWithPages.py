from BSStuff import searchProteinAndSpecies, getFastaFromURL, getDetailsFromGenBankPage

def makeSearchString(speciesTupleInfo, geneString):
    searchString = ""
    for entry in speciesTupleInfo:
        searchString += entry
        searchString += '+'
    searchString += geneString
    return searchString

def oneIsPresent(list, string):
    for thing in list:
        if string.find(thing) != -1:
            return True
    return False

def resultAcceptable(result, tuple, stringList, usedVersions):
    if result["version"] in usedVersions:
        return False
    if result["sequenceLength"] not in range(650, 1300):
        return False
    if not oneIsPresent(stringList, result["title"]):
        return False
    for thing in tuple:
        if(result["title"].find(thing) == -1):
            return False
    return True

def altResultAcceptable(result, tuple, stringList, usedSpecies):
    if result["speciesTuple"] in usedSpecies:
        return False
    if result["sequenceLength"] not in range(650, 1300):
        return False
    if not oneIsPresent(stringList, result["title"]):
        return False
    for thing in tuple:
        if(result["title"].find(thing) == -1):
            return False
    return True

def closerTo(a, b, target):
    if (abs(a - target) < abs(b - target)):
        return True
    return False
def hasVoucher(result):
    if(result["voucher"] != ""):
        return True
    return False

def betterResultThan(res, bestResult):
    if(hasVoucher(res) and not hasVoucher(bestResult)):
        return True
    if(hasVoucher(bestResult) and not hasVoucher(res)):
        return False

    return closerTo(res["sequenceLength"], bestResult["sequenceLength"], 1200)

def formatResult(result, searchMetaInfo):
    fastaText = getFastaFromURL(result["fastaLink"])
    fastaLines = fastaText.splitlines()
    fastaReturnString = ">" + result["speciesTuple"][0] + "_" + result["speciesTuple"][1] + "_" + result["version"] + '\n'
    for i in range(1, len(fastaLines)):
        fastaReturnString += fastaLines[i] + '\n'
    extractedTuple = searchMetaInfo["extractedTuple"]
    extrlitgenus = searchMetaInfo["ExtrLitGenus"]
    csvColumnElements = (extractedTuple[0], extractedTuple[1], extrlitgenus, result["speciesTuple"][0], result["speciesTuple"][1], result["version"], result["voucher"], result["sequenceLength"])
    csvReturnString = ""
    for thing in csvColumnElements:
        csvReturnString += str(thing) + ","
    csvReturnString = csvReturnString[:-1]
    csvReturnString += '\n'
    return (fastaReturnString, csvReturnString, result["version"])

def tryScrapeFor(tuple, searchMetaInfo, geneString, driver):
    searchString = makeSearchString(tuple, geneString)
    resultsList = searchProteinAndSpecies(searchString, driver)
    bestResult = None
    listStringsToFind = None
    if(geneString == "rbcL"):
        listStringsToFind = ("rbcL")
    else:
        listStringsToFind = ("maturase", "matK")

    for res in resultsList:
        if(resultAcceptable(res, tuple, listStringsToFind, searchMetaInfo["usedVersions"])):
            if(bestResult == None):
                if("voucher" in res):
                    bestResult = res
                else:
                    bestResult = getDetailsFromGenBankPage(res["genbankLink"], driver)
                continue
            if(hasVoucher(bestResult)):
                if(closerTo(bestResult["sequenceLength"], res["sequenceLength"], 1200)):
                    continue
            genBankRes = getDetailsFromGenBankPage(res["genbankLink"], driver)
            if betterResultThan(genBankRes, bestResult):
                    bestResult = genBankRes
    if(bestResult == None):
        return None

    return formatResult(bestResult, searchMetaInfo)

def valueResult(result):
    value = 0
    if(result["voucher"] != 0):
        value = 1
    value += goodnessOfSequenceLength(result['sequenceLength'])
    return value

def goodnessOfSequenceLength(sequenceLength):
    return -abs(sequenceLength-1200)/550
def tryScrapeForAlt(tuple, usedSpecies, geneString, driver):
    searchString = makeSearchString(tuple, geneString)
    resultsList = searchProteinAndSpecies(searchString, driver)
    bestResult = None
    listStringsToFind = None
    if(geneString == "rbcL"):
        listStringsToFind = ("rbcL")
    else:
        listStringsToFind = ("maturase", "matK")
    returnList = []
    bestResult = None

    for res in resultsList:
        if(altResultAcceptable(res, tuple, listStringsToFind, usedSpecies)):
            if(bestResult == None):
                if 'genbankLink' in res:
                    bestResult = getDetailsFromGenBankPage(res["genbankLink"], driver)
                else:
                    bestResult = res
            elif(bestResult["voucher"] == 0 and goodnessOfSequenceLength(res['sequenceLength']) > goodnessOfSequenceLength(bestResult['sequenceLength']) ):
                if 'genbankLink' in res:
                    bestResult = getDetailsFromGenBankPage(res["genbankLink"], driver)
                else:
                    bestResult = res
    return bestResult
