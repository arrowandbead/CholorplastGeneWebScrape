import SpeciesListParser
import partialSupport
from selenium import webdriver

file = SpeciesListParser.createFile('/Users/malcolmmeyerson/Documents/chloroPlastGenScrape', 'species.xlsx')
genuses = set()
for row in file:
    if(partialSupport.checkFirstRow(row)):
        continue
    genus = partialSupport.genusTupleFromRow(row)[0]
    genuses.add(genus)

matkMeta = open("outputFiles/firstPassResults/matk_meta.csv")
inmatk = set()
for thing in matkMeta:
    split = thing.split(',')
    if(split[0] == "extracted genus"):
        continue
    inmatk.add(split[0])

rbclMeta = open("outputFiles/firstPassResults/rbcl_meta.csv")
inRbcl = set()
for thing in rbclMeta:
    split = thing.split(',')
    if split[0] == "extracted genus":
        continue
    inRbcl.add(split[0])

notInRbcl = set()
notInMatk = set()
for thing in genuses:
    if thing not in inRbcl:
        notInRbcl.add(thing)
    if thing not in inmatk:
        notInMatk.add(thing)

genusesMissingMatk = open("missingGenusesMatk.txt", "w+")
for thing in notInMatk:
    genusesMissingMatk.write(thing + '\n')
genusesMissingRbcl = open("missingGenusesRbcl.txt", "w+")
for thing in notInRbcl:
    genusesMissingRbcl.write(thing + '\n')
