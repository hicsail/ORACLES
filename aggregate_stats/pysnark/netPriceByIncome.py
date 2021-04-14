from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
from hashlib import sha256
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)


# // Witness:  single table database (D) representing the income years, seperate income brackets, and each row in an income bracket representing the amount paid for that year
# // Public knowledge: Public IPEDS Statistics that show the average net price per each income bracket
# // Statement: the average net price paid is calculated over the data with at least N people within the dataset within each income bracket for each income year
# // 
# //

@snark
def average_paidPriceByIncome(incomeData, hashedData):
    #  Begin with just 2016-2017
    data = []
    for income in incomeData[0]["2016-2017"]: 
        private_data = map(PrivValFxp, incomeData[0]["2016-2017"][income])
        sum = PrivValFxp(0)
        len = PrivVal(0)
        for val in private_data: 
            sum = sum + val
            len = len + 1
        data.append(sum/len)
    commitment = sha256(json.dumps(incomeData).encode('utf-8')).hexdigest()
    if (commitment == hashedData):
        # array of average tuition paid for each of the five income income brackets in a year 
        return data

with open('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/rawNetPriceIncome.json', 'r') as data_json: 
    with open ('/Users/gagandeepkang/Desktop/SAIL/oracle/aggregate_stats/data/hashedNetPriceIncome.json', 'r') as hashed_data:
        print("Average Price Paid per Income in 2016-2017 ", average_paidPriceByIncome(json.load(data_json), json.load(hashed_data)))
