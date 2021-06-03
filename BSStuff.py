from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import re



import urllib.request, urllib.error, urllib.parse

def notRedirected(soup):
    if len(soup.findAll("div", {"class" : "rprtheader"})) == 0:
        return True
    return False

def searchProteinAndSpecies(searchString, driver):
    url = 'https://www.ncbi.nlm.nih.gov/nuccore/?term=' + searchString
    driver.get(url)
    WebDriverWait(driver, 100).until(lambda driver: driver.execute_script('return document.readyState') == 'complete')
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    infoList= []
    if(notRedirected(soup)):
        for i in range(0,2):
            html = driver.page_source
            soup = BeautifulSoup(html, "html.parser")
            rsltList = soup.findAll("div", {"class": "rslt"})
            for i in range(0,len(rsltList)):
                curr = rsltList[i]

                boldList = curr.findAll("b")
                if(len(boldList)==0):
                    continue
                speciesName = boldList[0]
                accession = curr.findAll("dl", {"class" : "rprtid"})[0].findAll("dd")[0].contents[0]
                speciesTuple = tuple(speciesName.contents[0].split(' '))
                reportLinks = curr.findAll("div", {"class" : "shortcuts"})
                genBankLink = "https://www.ncbi.nlm.nih.gov" + reportLinks[0].contents[0]['href']
                fastaLink = "https://www.ncbi.nlm.nih.gov" + reportLinks[0].contents[1]['href']
                link =  curr.findAll("a")[0]
                sequenceLength = int(str.split(curr.findAll("p", {"class" : "desc"})[0].contents[0])[0].replace(",", ""))
                title = ""
                for element in link.contents:
                    if isinstance(element, str):
                        title += element
                    else:
                        title += element.contents[0]
                resDict = {
                    "version" : accession,
                    "speciesTuple" : speciesTuple,
                    "sequenceLength" : sequenceLength,
                    "title" : title,
                    "genbankLink" : genBankLink,
                    "fastaLink" : fastaLink
                }
                infoList.append(resDict)
                if(len(infoList) > 8):
                    return infoList
            nextLink = None
            if(i!=3):
                try:
                    driver.find_element_by_xpath('//*[@title="Next page of results"]').click()
                except:
                    return infoList

        return infoList
    else:
        details = getDetailsFromGenBankPage(url, driver)
        infoList.append(details)
        return infoList


def getDetailsFromGenBankPage(url, driver):
    driver.get(url)
    element = WebDriverWait(driver, 200).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "pre.genbank"))
            )
    html = driver.page_source
    soup = BeautifulSoup(html, "html.parser")
    titleElement = soup.findAll("div", {"class" : "seqrprt seqviewer"})[0].findAll("h1")[0]
    titleText = ""
    for thing in titleElement:
        if(isinstance(thing, str)):
            titleText += thing
        else:
            titleText+=thing.contents[0]
    genbank = soup.findAll("pre", {"class" : "genbank"})[0]
    intermediate = genbank.contents[0].replace('\n', ' ').split(' ')
    #speciesTuple = tuple(genbank.contents[1].contents[0].split(" "))
    temp = titleText.split(' ')
    speciesTuple = (temp[0], temp[1])
    version = ""
    sequenceLength = ""
    for i in range(0, len(intermediate)):
        if(intermediate[i] == 'bp'):
            sequenceLength = int(intermediate[i-1])
        if(intermediate[i] == 'VERSION'):
            p = i+1
            while(intermediate[p] == ''):
                p+=1
            version = intermediate[p]
            break
    if(sequenceLength == ' '):
        raise
    if(version == ' '):
        print("No version")
        raise
    featureID = "feature_" + version + "_source_0"
    featuresBlockText = soup.findAll("span", {"id": featureID})[0].contents[1]
    voucherID = '"'
    voucherLocation = featuresBlockText.find("/specimen_voucher")
    finalVoucher = ""
    if(voucherLocation != -1):
        curr = voucherLocation + 19
        try:
            while(featuresBlockText[curr] != '"'):
                voucherID += featuresBlockText[curr]
                curr += 1
            voucherID += '"'
            voucherSplit = voucherID.split("\n")
            postnewlineVoucher = ""
            for thing in voucherSplit:
                postnewlineVoucher += thing
            spaceSplit = postnewlineVoucher.split(" ")
            for thing in spaceSplit:
                if(thing != ""):
                    finalVoucher += thing + " "
            finalVoucher = finalVoucher[:-1]
        except IndexError:
            acronym = soup.findAll("acronym", {"class" : "voucher"})[0]
            finalVoucher += '"'
            finalVoucher += acronym.contents[0]
            next = acronym.nextSibling
            lastChar = None
            for char in next:
                if(char == '\n'):
                    lastChar = char
                    continue
                if(char == ' '):
                    if(lastChar == ' '):
                        continue
                finalVoucher +=  char
                if(char == '"'):
                    break
    else:
        finalVoucher = "None"
    fastaLink = "https://www.ncbi.nlm.nih.gov" + soup.findAll("a", {"class" : "dblinks"})[0]['href']

    details = {
    "version" : version,
    "voucher" : finalVoucher,
    "speciesTuple" : speciesTuple,
    "sequenceLength" : sequenceLength,
    "fastaLink" : fastaLink,
    "title" : titleText
    }
    return details
def getFastaFromURL(url):
    fasta_url = 'https://www.ncbi.nlm.nih.gov/sviewer/viewer.fcgi?id={id}&report=fasta'

    soup = BeautifulSoup(requests.get(url).content, 'html.parser')
    id_ = soup.select_one('meta[name="ncbi_uidlist"]')['content']
    fasta_txt = requests.get(fasta_url.format(id=id_)).text

    return(fasta_txt)


#searchProteinAndSpecies("dsa", driver)
# driver = webdriver.Chrome(executable_path='/Users/malcolmmeyerson/Documents/chloroPlastGenScrape/chromedriver')
# searchProteinAndSpecies("Salix+caprea+rbcL", driver)
# driver.quit()


#ha = getDetailsFromGenBankPage("https://www.ncbi.nlm.nih.gov/nuccore/182410879", driver)
#for thing in ha:
    #print(thing + " : " + str(ha[thing]))
#driver.quit()
#searchProteinAndSpecies("Daucus+carota+maturase+K", driver)
#driver.quit()
