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
        avg = PrivValFxp(sum/len)
        data.append(avg)
    # array of average tuition paid for each of the five income income brackets in a year 
    return data 

with open('../rawNetPriceIncome.json', 'r') as data_json: 
    data = json.load(data_json)
print("Average Price Paid per Income in 2016-2017 ", average_paidPriceByIncome(data))
