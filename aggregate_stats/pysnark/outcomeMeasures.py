from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
from hashlib import sha256
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)


# // Witness:  multi-table database (D) for full-time and part-time first-time degree seekers and full-time and part-time non-first-time degree seekers
#              measuring whether they received their bachelor's degree when entering in 2011-2012
# // Public knowledge: Public IPEDS Statistics that shows the percentages for each cohort, and seperates all students, students who received a Pell Grant, and students who
# //                   did not receive a pell grant
# // Statement: the average outcome measures are calculated over the data with at least N people within the dataset for all full-time first-time degree seekers, part-time 
# //            first-time degree seekers, full-time non-first-time degree seekers, and part-time non-first-time degree seekers
# // Limitations: PySnark's Fixed Point Value only stores 16 bits for integers, therefore for the computations of a large number of rows, we are unable to calculate the appropriate 
#                 values, so we have scaled down the data in terms of 100 for each category (10 pell grant recipients and 90 non-pell grant students)
# //
@snark
def average_outcomeMeasures(outcomeData, hashedData): 
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
        pellLen = PrivVal(1)
        count = 0
        for val in privatePellData: 
            # Count: 0 - Received Bachelor's; 1 - Enrolled at same institution; 2 - Enrolled at different institution
            if count == 0: 
                receivedBachelorsPell = receivedBachelorsPell + val
                count += 1
            elif count == 1: 
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
            # Count: 0 - Received Bachelor's; 1 - Enrolled at same institution; 2 - Enrolled at different institution
            if count == 0: 
                receivedBachelorsNonPell = receivedBachelorsNonPell + val
                count += 1
            elif count == 1: 
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
    commitment = sha256(json.dumps(outcomeData).encode('utf-8')).hexdigest()
    if (commitment == hashedData):
        return categoryObj

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawOutcomeMeasures.json', 'r') as data_json: 
    with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/hashedOutcomeMeasures.json', 'r') as hashedData: 
        print("Average Outcome Measures", average_outcomeMeasures(json.load(data_json), json.load(hashedData)))