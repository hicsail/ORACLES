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


    with open('../data/rawNetPriceIncome.json', 'w') as ed_json: 
        json.dump(dataset, ed_json, indent = 4)

def createOutcomeMeasures(): 
    dataset = []
    categories = [
    "FULL-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12", 
    "PART-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12", 
    "FULL-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
    "PART-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12"
    ]

    categoriesObj = {} 
    for i in range(len(categories)): 
        data = []
        if i == 0: 
            # Add Pell Grant Data
            for j in range(10): 
                if j < 8: 
                    data.append({"Pell": 1, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif j >= 8 and j < 9 : 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                else: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
            # Non-pell grant data 
            for k in range(90):
                if k < 79: 
                    data.append({"Pell": 0, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif k >= 79 and k < 86: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                else: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})                    
        elif i == 1: 
            # Add Pell Grant Data
            for j in range(10): 
                if j < 5: 
                    data.append({"Pell": 1, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                else: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
            # Non-pell grant data 
            for k in range(90):
                if k < 30: 
                    data.append({"Pell": 0, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                else: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
        elif i==2: 
            # Add Pell Grant Data
            for j in range(10): 
                if j < 8: 
                    data.append({"Pell": 1, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif j >= 8 and j < 9: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                else: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
            # Non-pell grant data 
            for k in range(90):
                if k < 77: 
                    data.append({"Pell": 0, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif k >= 77 and k < 84: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                else: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
        else: 
            # Add Pell Grant Data
            for j in range(10): 
                if j < 5: 
                    data.append({"Pell": 1, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif j >= 5 and j < 8: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                else: 
                    data.append({"Pell": 1, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})

            # Non-pell grant data 
            for k in range(90):
                if k < 45: 
                    data.append({"Pell": 0, "Received Bachelor's": 1, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
                elif k >= 45 and k < 63: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 1})
                elif k >= 63 and k < 63: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 1, "Enrolled at different insitution": 0})
                else: 
                    data.append({"Pell": 0, "Received Bachelor's": 0, "Enrolled at same insitution": 0, "Enrolled at different insitution": 0})
        categoriesObj[categories[i]] = data
    dataset.append(categoriesObj)
    with open("../data/rawOutcomeMeasures.json", 'w') as outcome_json:
        json.dump(dataset, outcome_json, indent=4)
        


def createDistanceEducationStatus():
    dataset = []
    categories = ["UNDERGRADUATE DISTANCE EDUCATION STATUS", "GRADUATE DISTANCE EDUCATION STATUS"]

    categoriesObj = {} 
    for i in range(len(categories)):
        # handle undegrad distance case
        if i == 0: 
            undergradData = []
            for j in range(99): 
                undergradData.append({"Enrolled in only distance education": 0, "Enrolled in some distance education": 0, "Not enrolled in any distance education": 1})
            undergradData.append({"Enrolled in only distance education": 0, "Enrolled in some distance education": 1, "Not enrolled in any distance education": 0})
            categoriesObj[categories[i]] = undergradData
        else: 
            gradData = []
            for j in range(81): 
                gradData.append({"Enrolled in only distance education": 0, "Enrolled in some distance education": 0, "Not enrolled in any distance education": 1})
            for k in range(14): 
                gradData.append({"Enrolled in only distance education": 1, "Enrolled in some distance education": 0, "Not enrolled in any distance education": 0})
            for l in range(5): 
                gradData.append({"Enrolled in only distance education": 0, "Enrolled in some distance education": 1, "Not enrolled in any distance education": 0})
            categoriesObj[categories[i]] = gradData
    dataset.append(categoriesObj)
    with open('../data/rawDistanceEducation.json', 'w') as ed_json: 
        json.dump(dataset, ed_json, indent = 4)

def createGraduationRateMeasures(): 
    dataset = []
    categories = ["4-year", "6-year", "8-year"]
    categoriesObj = {}
    for i in range(len(categories)): 
        yearData = []
        # handle 4-year case
        if i == 0:             
            # Began in 2011
            for j in range(100): 
                if j <= 80: 
                    yearData.append({"Began": "2011", "Graduated": 1})
                else: 
                    yearData.append({"Began": "2011", "Graduated": 0})
            # Began in 2013
            for k in range(100): 
                if k <= 83: 
                    yearData.append({"Began": "2013", "Graduated": 1})
                else: 
                    yearData.append({"Began": "2013", "Graduated": 0})
        elif i == 1:
            # handle 6-year case
            # Began in 2011
            for j in range(100): 
                if j <= 86: 
                    yearData.append({"Began": "2011", "Graduated": 1})
                else: 
                    yearData.append({"Began": "2011", "Graduated": 0})
            # Began in 2013
            for k in range(100): 
                if k < 88: 
                    yearData.append({"Began": "2013", "Graduated": 1})
                else: 
                    yearData.append({"Began": "2013", "Graduated": 0})
        else: 
            # handle 8-year case
            # Began in 2011
            for j in range(100): 
                if j < 88: 
                    yearData.append({"Began": "2011", "Graduated": 1})
                else: 
                    yearData.append({"Began": "2011", "Graduated": 0})
        categoriesObj[categories[i]] = yearData
    dataset.append(categoriesObj)
    with open('../data/rawGraduationRateMeasures.json', 'w') as ed_json: 
        json.dump(dataset, ed_json, indent = 4)

def covidCasesAge(): 
    dataset = [{"0-19": 6, "20-29": 15, "30-39": 15, "40-49": 14, "50-59": 16, "60-69": 13, "70-79": 8, "80+": 13}]
    with open("../data/rawCovidCasesByAge.json", 'w') as covid_json:
        json.dump(dataset, covid_json, indent=4)

def hashJSON(currentFileName, hashedFileName): 
    with open(currentFileName, 'r') as ed_json: 
        data= json.load(ed_json)
        a = json.dumps(data)
        hashedDb = sha256(a.encode('utf-8')).hexdigest()
        with open(hashedFileName, 'w') as hashed_json: 
            json.dump(hashedDb, hashed_json)

createOutcomeMeasures()
hashJSON('../data/rawOutcomeMeasures.json', '../data/hashedOutcomeMeasures.json')