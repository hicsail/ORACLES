import json
from pysnark import runtime
from pysnark.runtime import snark, PrivVal, LinCombFxp

@snark
def compute(data, results):
    # Compute graduation rates by category
    for category in data:
        arr2011 = [x == 1 for x in data[category]]
        arr2013 = [x == 11 for x in data[category]]
        
        graduated2011 = LinCombFxp.fromvar(sum(arr2011), True)
        graduated2013 = LinCombFxp.fromvar(sum(arr2013), True)
        length2011 = PrivVal(len(arr2011))
        length2013 = PrivVal(len(arr2013))

        gr2011 = graduated2011 / (length2011 + (length2011 == 0))
        gr2013 = graduated2013 / (length2013 + (length2013 == 0))

        data[category] = {
            "Began in 2011": gr2011,
            "Began in 2013": gr2013
        }

    # Assert results are correct
    for category in results:
        data[category]["Began in 2011"].assert_eq(results[category]["Began in 2011"])
        data[category]["Began in 2013"].assert_eq(results[category]["Began in 2013"])

if __name__ == '__main__':
    runtime.bitlength = 17

    data = json.load(open('data/Degrees Awarded/data.json', 'r'))
    for category in data:
        students = []
        for student in data[category]:
            num = student["Graduated"]
            if student["Began"] == "2013":
                num += 10
            students.append(PrivVal(num))
        data[category] = students
    results = json.load(open('data/Degrees Awarded/results.json', 'r'))

    compute(data, results)
    print("Successfully verified average graduation rates!")
        
