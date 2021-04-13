from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
import pysnark.zkinterface.backend
import json

# set modulus specific to Dalek Bulletproof
# pysnark.zkinterface.backend.set_modulus(7237005577332262213973186563042994240857116359379907606001950938285454250989)

# modulus specific to Bellman
pysnark.zkinterface.backend.set_modulus(52435875175126190479447740508185965837690552500527637822603658699938581184513)

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