import os
import csv

def listToString(l):
    result = '"' + l[0] + '"'
    for i in range(1, len(l)):
        result += ',"' + l[i] + '"'
    return result

# given country-year-entries item, return csv string
def stringifyEntry(entry):
    region = ""
    if entry[0][0] in countryToRegion:
        region = countryToRegion[entry[0][0]]
    incomeGroup = ""
    if entry[0][0] in countryToIncomeGroup:
        incomeGroup = countryToIncomeGroup[entry[0][0]]

    # country, year, region, income group
    result = '"' + entry[0][0] + '","' + entry[0][1] + '","' + region + '","' + incomeGroup + '"'
    for v in allVariables:
        result += "," + entry[1][v]
    return result

countryIndex = 0
indicatorNameIndex = 2
firstYearIndex = 4

countryDataFilename = "data/countryMetadata.csv"
outputFilename = "data/finalData.csv"
srcDir = "./raw_data"

criCountryIndex = 4
criRegionIndex = 1
criIncomeGroupIndex = 2

countryToRegion = dict()
countryToIncomeGroup = dict()

countryYearToEntries = dict()
allVariables = []

with open(countryDataFilename) as countryDatafile:
    first = True
    csvReader = csv.reader(countryDatafile, quotechar='"')
    for row in csvReader:
        if first:
            first = False
        else:
            countryToRegion[row[criCountryIndex]] = row[criRegionIndex]
            countryToIncomeGroup[row[criCountryIndex]] = row[criIncomeGroupIndex]

for filename in os.listdir(srcDir):
    if not filename.endswith(".csv"):
        continue
    
    with open(srcDir + "/" + filename) as file:
        headerFound = False
        headerVals = []
        indicatorName = ""

        csvReader = csv.reader(file, quotechar='"')
        for row in csvReader:
            if len(row) == 0:
                continue
            vals = [v.replace('"', '') for v in row]
            if headerFound:
                # record the variable name for this file
                if indicatorName == "":
                    indicatorName = vals[indicatorNameIndex]
                    allVariables.append(indicatorName)
                    print(indicatorName)

                # go through the columns and record entry for each country,year pair
                for v in range(firstYearIndex, len(vals)):
                    # exit if list goes long or if there's no associated year
                    if v >= len(headerVals) or headerVals[v] == "":
                        break
                    # map country and year pair to dict of other values
                    countryYear = (vals[countryIndex], headerVals[v])
                    if countryYear not in countryYearToEntries:
                        countryYearToEntries[countryYear] = dict()
                    # put value of this indicator in dict
                    entries = countryYearToEntries[countryYear]
                    entries[indicatorName] = vals[v]
            else:
                # if header line, remember header values
                if vals[countryIndex] == "Country Name":
                    headerFound = True
                    headerVals = list(vals)

# write dictionary to output file
outputFile = open(outputFilename, 'w')
outputFile.write("Country,Year,Region,Income Group," + listToString(allVariables) + "\n")
for entry in sorted(countryYearToEntries.items(), key=lambda cy: cy[0][0]):
    line = stringifyEntry(entry) + "\n"
    outputFile.write(line)
outputFile.close()