from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
from hashlib import sha256
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)

# // Witness:  multi-table table database (D) for undergraduate and graduate students representing if they were enrolled in any distance education
# // Public knowledge: Public IPEDS Statistics that show the percentage of Undergraduate / Graduate students enrolled in distance education
# // Statement: the average distance education is calculated over the data with at least N people within the dataset for undergraduate and graduate students
# // 
# //
@snark 
def average_distanceEducationStatus(distanceData, lfaData, hashedData):
    distanceObj = distanceData[0]
    lfaObj = lfaData[0]
    ret = {}
    for val in distanceObj: 
        specificData = distanceObj[val]
        lfa = lfaObj[val]
        # need to map our specific data for undergrad / grad into a private data
        toPrivatize = []
        lfaPrivatize = []
        for data in specificData: 
            for key in data: 
                toPrivatize.append(data[key])
        for data in lfa: 
            for key in data: 
                lfaPrivatize.append(data[key])
        private_data = map(PrivVal, toPrivatize)
        private_lfa = map(PrivVal, lfaPrivatize)
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
        ret["Pre-COVID"] = {"Only Distance Education": onlyDistance / len, "Some Distance": someDistance / len, "No Distance": noDistance / len}        
        
        onlyDistanceLFA = PrivValFxp(0)
        someDistanceLFA = PrivValFxp(0)
        noDistanceLFA = PrivValFxp(0)
        lenLFA = PrivVal(0)
        countLFA = 0
        for val in private_lfa:
        # Count: 0 - Only Distance; 1 - Some Distance; 2 - No Distance
            if countLFA == 0: 
                onlyDistanceLFA = onlyDistanceLFA + val
                countLFA += 1
            elif countLFA == 1: 
                someDistanceLFA = someDistanceLFA + val
                countLFA += 1
            else: 
                noDistanceLFA = noDistanceLFA + val
                countLFA = 0
                lenLFA = lenLFA + 1
        ret["COVID"] = {"Only Distance Education": onlyDistanceLFA / lenLFA, "Some Distance": someDistanceLFA / lenLFA, "No Distance": noDistanceLFA / lenLFA}        
    commitment = sha256(json.dumps(distanceData).encode('utf-8')).hexdigest()
    if (commitment == hashedData):
        return ret

with open('../data/rawDistanceEducation.json', 'r') as data_json, \
    open('../data/rawDistanceEducation.json', 'r') as lfa_data, \
    open('../data/hashedDistanceEducation.json', 'r') as hashedData: 
        print("Average Distance Education Status", average_distanceEducationStatus(json.load(data_json), json.load(lfa_data), json.load(hashedData)))
