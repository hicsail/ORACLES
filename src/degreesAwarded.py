import json
from common import flatten, count_ops
from pysnark import runtime
from pysnark.runtime import snark, PrivVal, benchmark
from pysnark.fixedpoint import LinCombFxp
from pysnark.poseidon_hash import poseidon_hash

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Compute graduation rates by category
    output = {}
    for category in data:
        graduated2011 = LinCombFxp(sum([x == 1 for x in data[category]]))
        graduated2013 = LinCombFxp(sum([x == 11 for x in data[category]]))
        
        length2011 = sum([x < 10 for x in data[category]])
        length2013 = sum([x >= 10 for x in data[category]])

        gradrate2011 = graduated2011 / (length2011 + (length2011 == 0))
        gradrate2013 = graduated2013 / (length2013 + (length2013 == 0))

        output[category] = {
            "Began in 2011": gradrate2011,
            "Began in 2013": gradrate2013
        }

    # Assert results are correct
    for category in results:
        output[category]["Began in 2011"].assert_eq(results[category]["Began in 2011"])
        output[category]["Began in 2013"].assert_eq(results[category]["Began in 2013"])

if __name__ == '__main__':
    runtime.bitlength = 17

    data = json.load(open('data/Degrees Awarded/data.json', 'r'))
    for category in data:
        students = []
        for student in data[category]:
            num = int(student["Graduated"])
            if student["Began"] == 2013:
                num += 10
            students.append(PrivVal(num))
        data[category] = students
    results = json.load(open('data/Degrees Awarded/results.json', 'r'))
    correct_hash = json.load(open('data/Degrees Awarded/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified average graduation rates!")
        
