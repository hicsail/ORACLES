import json 
import random
from hashlib import sha256

def createRawIncomePriceData(): 
    dataset = []
    yearObj = {}
    years = ["2016-2017", "2017-2018", "2018-2019"]
    incomeBrackets = ["$0 to $30,000", "$30,001 to $48,000", "$48,001 to $75,000", "$75,001 to $110,000", "$110,001 and more"]
    incomeTuples = [(0, 30000), (30001, 48000), (48001, 75000), (75001, 110000), (110001, 1000000)]

    incomeDict = {
        "2016-2017": {
            "$0 to $30,000": 26482, 
            "$30,001 to $48,000": 24148, 
            "$48,001 to $75,000": 28388, 
            "$75,001 to $110,000": 33704, 
            "$110,001 and more": 47331
        }, 
        "2017-2018": {
            "$0 to $30,000": 15661, 
            "$30,001 to $48,000": 13211, 
            "$48,001 to $75,000": 20801, 
            "$75,001 to $110,000": 32265, 
            "$110,001 and more": 47586
        }, 
        "2018-2019": {
            "$0 to $30,000": 12903, 
            "$30,001 to $48,000": 13256, 
            "$48,001 to $75,000": 20231, 
            "$75,001 to $110,000": 31075, 
            "$110,001 and more": 48048
        }
    }
    for i in range(len(years)): 
        # year we are looking at 
        year = years[i]
        # all of the income brackets for that year
        incomeObj = {}
        for j in range(len(incomeBrackets)): 
            data = []
            # generate random sample of incomes that average to the incomeDict[year][incomeBracket] for that year 
            for k in range(100): 
                randomIncome = random.randint(incomeTuples[j][0], incomeTuples[j][1])
                data.append(incomeDict[year][incomeBrackets[j]])
            incomeObj[incomeBrackets[j]] = data
        yearObj[year] = incomeObj
    dataset.append(yearObj)


    with open('rawNetPriceIncome.json', 'w') as ed_json: 
        json.dump(dataset, ed_json, indent = 4)

def hashJSON(): 
    with open('rawNetPriceIncome.json', 'r') as ed_json: 
        data= json.load(ed_json)
        a = json.dumps(data)
        hashedDb = sha256(a.encode('utf-8')).hexdigest()
        with open("hashedNetPriceIncome.json", 'w') as hashed_json: 
            json.dump(hashedDb, hashed_json)
# hashJSON()


# def createOutcomeMeasures(): 
#     dataset = []
#     categories = [
#     "FULL-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12", 
#     "PART-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12", 
#     "FULL-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
#     "PART-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12"
#     ]

#     for i in range(len(categories)): 


def createDistanceEducationStatus():
    dataset = []
    categories = ["UNDERGRADUATE DISTANCE EDUCATION STATUS", "GRADUATE DISTANCE EDUCATION STATUS"]

    categoriesObj = {} 
    for i in range(len(categories)):
        # handle undegrad distance case
        if i == 0: 
            undergradData = []
            for j in range(99): 
                undergradData.append({"Enrolled in only distance education": False, "Enrolled in some distance education": False, "Not enrolled in any distance education": True})
            undergradData.append({"Enrolled in only distance education": False, "Enrolled in some distance education": True, "Not enrolled in any distance education": False})
            categoriesObj[categories[i]] = undergradData
        else: 
            gradData = []
            for j in range(81): 
                gradData.append({"Enrolled in only distance education": False, "Enrolled in some distance education": False, "Not enrolled in any distance education": True})
            for k in range(14): 
                gradData.append({"Enrolled in only distance education": True, "Enrolled in some distance education": False, "Not enrolled in any distance education": False})
            for l in range(5): 
                gradData.append({"Enrolled in only distance education": False, "Enrolled in some distance education": False, "Not enrolled in any distance education": True})
            gradData.append({"Enrolled in only distance education": False, "Enrolled in some distance education": True, "Not enrolled in any distance education": False})
            categoriesObj[categories[i]] = gradData
    dataset.append(categoriesObj)
    with open('rawDistanceEducation.json', 'w') as ed_json: 
        json.dump(dataset, ed_json, indent = 4)

createDistanceEducationStatus()