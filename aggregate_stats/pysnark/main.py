# // Witness:  single table database (D)
# // Public knowledge: schema of D, constraint C that limits columns used
# // Statement: the statistic s is computed as s = φ(D)
# //            where the analysis φ involves data over at least N people within the dataset,
# //            and it only uses each column in a manner that adheres to the constraint C
# //

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

@snark
def average_paidPriceByIncome(incomeData):
    #  Begin with just 2016-2017
    yearData = incomeData[0]["2016-2017"]
    data = []
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
    return data 

with open('../data/rawNetPriceIncome.json', 'r') as data_json: 
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
        onlyDistance = PrivVal(0)
        someDistance = PrivVal(0)
        noDistance = PrivVal(0)
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
        ret.append({"Only Distance Education": onlyDistance, "Some Distance": someDistance, "No Distance": noDistance})
    return ret 
with open('../data/rawDistanceEducation.json', 'r') as data_json: 
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
                if i < 100: 
                    toPrivatizePell.append(data[i][key])
                else: 
                    toPrivatizeNonPell.append(data[i][key])
        privatePellData = map(PrivVal, toPrivatizePell)
        privateNonPellData = map(PrivVal, toPrivatizeNonPell)
        
        receivedBachelorsPell = PrivVal(0)
        differentInstitutionPell = PrivVal(0)
        sameInstitutionPell = PrivVal(0)
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

        receivedBachelorsNonPell = PrivVal(0)
        differentInstitutionNonPell = PrivVal(0)
        sameInstitutionNonPell = PrivVal(0)
        nonPellLen = PrivVal(0)
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
                "Received Bachelor's": receivedBachelorsPell, 
                "Enrolled at same institution": sameInstitutionPell, 
                "Enrolled at different insitution": differentInstitutionPell
            }, 
            "No Pell": {
                "Received Bachelor's": receivedBachelorsNonPell, 
                "Enrolled at same institution": sameInstitutionNonPell, 
                "Enrolled at different insitution": differentInstitutionNonPell
            }, "All Students": {
                "Received Bachelor's": receivedBachelorsPell + receivedBachelorsNonPell, 
                "Enrolled at same institution": sameInstitutionPell + sameInstitutionNonPell, 
                "Enrolled at different insitution": differentInstitutionPell + differentInstitutionNonPell
            }}
    return categoryObj
with open('../data/rawOutcomeMeasures.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Outcome Measures", average_outcomeMeasures(data))
        
