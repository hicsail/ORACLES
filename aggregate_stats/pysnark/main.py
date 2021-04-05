from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import json

@snark
def average_gpa(gpas):
    private_data = map(PrivValFxp, gpas)
    sum = PrivValFxp(0)
    len = PrivVal(0)
    for d in private_data:
        sum = sum + d
        len = len + 1

    return sum/len
    #return round(sum(gpas) / len(gpas), 2)

witness = [3.0, 3.4, 2.3, 4.0, 3.8, 2.6]
print("The average of GPAs ", average_gpa(witness))
# The average of GPAs  3.18
  
# // Witness:  single table database (D) with columns representing the income years along with the seperate income brackets  
# // Public knowledge: schema of D, constraint C that limits columns used
# // Statement: the statistic s is computed as s = φ(D)
# //            where the analysis φ involves data over at least N people within the dataset,
# //            and it only uses each column in a manner that adheres to the constraint C
# //

@snark
def average_paidPriceByIncome(incomeData):
    #  Begin with just 2016-2017
    yearData = incomeData[0]["2016-2017"]
    data = []
    avg = PrivValFxp(0)
    for income in yearData: 
        incomeBracket = yearData[income]
        private_data = map(PrivValFxp, incomeBracket)
        sum = PrivValFxp(0)
        len = PrivVal(0)
        for val in private_data: 
            sum = sum + val
            len = len + 1
        avg = sum/len
        data.append(avg)
    # array of average tuition paid for each of the five income income brackets in a year 
    return avg

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawNetPriceIncome.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Price Paid per Income in 2016-2017 ", average_paidPriceByIncome(data))

@snark 
def average_distanceEducationStatus(distanceData):
    distanceObj = distanceData[0]
    ret = []
    for val in distanceObj: 
        specificData = distanceObj[val]
        # need to map our specific data for undergrad / grad into a private data
        toPrivatize = []
        for data in specificData: 
            for key in data: 
                toPrivatize.append(data[key])
        private_data = map(PrivVal, toPrivatize)
        onlyDistance = PrivValFxp(0)
        someDistance = PrivValFxp(0)
        noDistance = PrivValFxp(0)
        len = PrivVal(0)
        count = 0
        # We need to examine three values at a time for each entry (no distance, some distanace, only distance) so we need a variable to keep track 
        for val in private_data: 
            # Count: 0 - Only Distance; 1 - Some Distance; 2 - No Distance
            if count == 0: 
                onlyDistance = onlyDistance + val
                count += 1
            elif count == 1: 
                someDistance = someDistance + val
                count += 1
            else: 
                noDistance = noDistance + val
                count = 0
                len = len + 1
        ret.append({"Only Distance Education": onlyDistance / len, "Some Distance": someDistance / len, "No Distance": noDistance / len})
    return ret 
with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawDistanceEducation.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Distance Education Status", average_distanceEducationStatus(data))

@snark
def average_outcomeMeasures(outcomeData): 
    dataCategories = outcomeData[0]
    categoryObj = {}
    for category in dataCategories: 
        data = dataCategories[category]
        # Need to take our array of objects and convert it into two arrays (pell data and non pell data) that they can be mapped as private values 
        toPrivatizePell = []
        toPrivatizeNonPell = []
        for i in range(len(data)): 
            for key in data[i]: 
                if i < 10: 
                    toPrivatizePell.append(data[i][key])
                else: 
                    toPrivatizeNonPell.append(data[i][key])
        privatePellData = map(PrivVal, toPrivatizePell)
        privateNonPellData = map(PrivVal, toPrivatizeNonPell)
        
        receivedBachelorsPell = PrivValFxp(0)
        differentInstitutionPell = PrivValFxp(0)
        sameInstitutionPell = PrivValFxp(0)
        pellLen = PrivVal(0)
        count = 0
        for val in privatePellData: 
            # Count: 1 - Received Bachelor's; 2 - Enrolled at same institution; 3 - Enrolled at different institution
            if count == 0: 
                count += 1
            elif count == 1: 
                receivedBachelorsPell = receivedBachelorsPell + val
                count += 1
            elif count == 2: 
                sameInstitutionPell = sameInstitutionPell + val
                count += 1
            else: 
                differentInstitutionPell = differentInstitutionPell + val
                count = 0
                pellLen = pellLen + 1
        receivedBachelorsNonPell = PrivValFxp(0)
        differentInstitutionNonPell = PrivValFxp(0)
        sameInstitutionNonPell = PrivValFxp(0)
        nonPellLen = PrivValFxp(0)
        count = 0
        for val in privateNonPellData: 
            # Count: 1 - Received Bachelor's; 2 - Enrolled at same institution; 3 - Enrolled at different institution
            if count == 0: 
                count += 1
            elif count == 1: 
                receivedBachelorsNonPell = receivedBachelorsNonPell + val
                count += 1
            elif count == 2: 
                sameInstitutionNonPell = sameInstitutionNonPell + val
                count += 1
            else: 
                differentInstitutionNonPell = differentInstitutionNonPell + val
                count = 0
                nonPellLen = nonPellLen + 1
        categoryObj[category] = {
            "Pell": {
                "Received Bachelor's": receivedBachelorsPell / pellLen, 
                "Enrolled at same institution": sameInstitutionPell / pellLen, 
                "Enrolled at different insitution": differentInstitutionPell / pellLen
            }, 
            "No Pell": {
                "Received Bachelor's": receivedBachelorsNonPell / nonPellLen, 
                "Enrolled at same institution": sameInstitutionNonPell / nonPellLen, 
                "Enrolled at different insitution": differentInstitutionNonPell / nonPellLen
            }, 
            "All Students": {
                "Received Bachelor's": (receivedBachelorsPell + receivedBachelorsNonPell) / (pellLen + nonPellLen), 
                "Enrolled at same institution": (sameInstitutionPell + sameInstitutionNonPell) / (pellLen + nonPellLen), 
                "Enrolled at different insitution": (differentInstitutionPell + differentInstitutionNonPell )/ (pellLen + nonPellLen)
            }}
    return categoryObj
with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawOutcomeMeasures.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Outcome Measures", average_outcomeMeasures(data))
        
@snark
def degreesAwarded(data): 
    outcomes = data[0]
    totalDegreesAwarded = PrivVal(0)
    categoryObj = {}
    for category in outcomes: 

        yearData = outcomes[category]
        # Need to take our array of objects and convert it into two arrays for began in 2011 and began in 2013 and privatize those values 
        arr1 = []
        arr2 = []
        for i in range(len(yearData)): 
            if yearData[i]["Began"] == "2011": 
                arr1.append(yearData[i]["Graduated"]) 
            else: 
                arr2.append(yearData[i]["Graduated"])
        privateArr1 = map(PrivVal, arr1)
        privateArr2 = map(PrivVal, arr2)

        graduated1 = PrivValFxp(0)
        graduated2 = PrivValFxp(0)
        length1 = PrivVal(0)
        length2 = PrivVal(0)
        for val in privateArr1:
            graduated1 = graduated1 + val
            length1 = length1 + 1
        for val in privateArr2: 
            graduated2 = graduated2 + val
            length2 = length2 + 1
        if len(arr2) == 0: 
            length2 = length1
        if category == "8-year":
            totalDegreesAwarded = totalDegreesAwarded + graduated1
        if category == "6-year": 
            totalDegreesAwarded = totalDegreesAwarded + graduated2
        categoryObj[category] = {"Began in 2011": graduated1 / length1, "Began in 2013": graduated2 / length2}
    categoryObj["Degrees Awarded in 2020"] = totalDegreesAwarded
    return categoryObj 

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawGraduationRateMeasures.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Graduation Rate Measures", degreesAwarded(data))

@snark
def covidCasesByAge(data):
    covidData = data[0]
    arr = []
    sumArr = []
    categories = ["0-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"]
    retObj = {}
    for val in covidData:
        arr.append(covidData[val])
    privateCovidData = map(PrivValFxp, arr)
    sum = PrivValFxp(0)
    for x in privateCovidData:
        sumArr.append(x) 
        sum = sum + x
    for i in range(len(sumArr)): 
        sumArr[i] = sumArr[i] / sum
    for j in range(len(categories)):
        retObj[categories[j]] = sumArr[j]
    return retObj 

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawCovidCasesByAge.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Covid Cases by Age Measures in MA", covidCasesByAge(data))
