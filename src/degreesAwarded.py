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

    # Constants
    degree_lengths = [4, 6, 8]
    start_years = [2011, 2013]

    # Construct output dictionary in expected result format
    output = {(str(y) + "-year"):{("Began in " + str(x)):0 for x in start_years} for y in degree_lengths}

    # Populate output dictionary with graduation rates
    for degree_length in degree_lengths:
        for start_year in start_years:
            # Construct integer representations for grads and non-grads
            grad_repr = convert_to_int(True, start_year, degree_length)
            non_grad_repr = convert_to_int(False, start_year, degree_length)

            # Count number of grads and non-grads
            grads = LinCombFxp(sum([x == grad_repr for x in data]))
            non_grads = LinCombFxp(sum([x == non_grad_repr for x in data]))
            total = grads + non_grads

            grad_rate = grads / (total + (total == 0))

            output[str(degree_length) + "-year"]["Began in " + str(start_year)] = grad_rate

    # Assert results are correct
    for category in results:
        output[category]["Began in 2011"].assert_eq(results[category]["Began in 2011"])
        output[category]["Began in 2013"].assert_eq(results[category]["Began in 2013"])

def convert_to_int(graduated, start_year, degree_length):
    student_repr = degree_length * 1000 
    student_repr += (start_year % 100) * 10
    student_repr += int(graduated)
    return student_repr

if __name__ == '__main__':
    runtime.bitlength = 17

    data = json.load(open('data/Degrees Awarded/data.json', 'r'))
    # Create integer representation of data
    data = [convert_to_int(x["Graduated"], x["Began"], int(x["Degree Type"][0])) for x in data]
    # Construct private witness variables
    data = [PrivVal(x) for x in data]

    results = json.load(open('data/Degrees Awarded/results.json', 'r'))
    correct_hash = json.load(open('data/Degrees Awarded/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified average graduation rates!")
        
