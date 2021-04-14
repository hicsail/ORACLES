from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
from hashlib import sha256
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)

# # // Witness:  single table database (D) for COVID Cases in Massachusetts based on the following age ranges: "0-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"
# # // Public knowledge: Public IPEDS Statistics that shows the raw total cases for each age range
# # // Statement: Percentage of total COVID Cases in MA attributed to an age-group is calculated over the entire dataset
# # // Limitations: PySnark's Fixed Point Value only stores 16 bits for integers, therefore for the computations of a large number of rows, we are unable to calculate the appropriate 
# #                 values, so we have scaled down the data so that the sum of all the age ranges is 100 and we scaled each age-range's number of cases proportional to 100.
# # 
@snark
def covidCasesByAge(data, hashedData):
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
    commitment = sha256(json.dumps(data).encode('utf-8')).hexdigest()
    if (commitment == hashedData):
        return retObj 

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawCovidCasesByAge.json', 'r') as data_json: 
    with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/hashedCovidCasesByAge.json', 'r') as hashedData: 
        print("Average Covid Cases by Age Measures in MA", covidCasesByAge(json.load(data_json), json.load(hashedData)))
