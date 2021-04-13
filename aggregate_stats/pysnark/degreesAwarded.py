from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)

# // Witness:  multi-table database (D) for students pursuing Bachelor's degrees, seperated by their enrollment in either a 4-year, 6-year, or 8-year program and whether they
#              began in Fall 2011 or Fall 2013
# // Public knowledge: Public IPEDS Statistics that shows the graduation rate percentages for all 4-year, 6-year, or 8-year program in Fall 2011 and Fall 2013
# // Statement: the average degrees awarded are calculated over the entire dataset
# // Limitations: PySnark's Fixed Point Value only stores 16 bits for integers, therefore for the computations of a large number of rows, we are unable to calculate the appropriate 
#                 values, so we have scaled down the data in terms of 200 rows for each 4-year, 6-year, and 8-year program (100 students beginning in Fall 2011 and 100 who began in Fall 2013)
# 
@snark
def degreesAwarded(data): 
    outcomes = data[0]
    # totalDegreesAwarded = PrivVal(0)
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
        length1 = PrivVal(1)
        length2 = PrivVal(1)
        for val in privateArr1:
            graduated1 = graduated1 + val
            length1 = length1 + 1
        for val in privateArr2: 
            graduated2 = graduated2 + val
            length2 = length2 + 1
        categoryObj[category] = {"Began in 2011": graduated1 / length1, "Began in 2013": graduated2 / length2}
    return categoryObj 

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawGraduationRateMeasures.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Graduation Rate Measures", degreesAwarded(data))
