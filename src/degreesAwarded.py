import json
from common import flatten, count_ops
from pysnark import runtime
from pysnark.runtime import snark, PrivVal, LinComb, benchmark
from pysnark.fixedpoint import LinCombFxp
from pysnark.poseidon_hash import poseidon_hash

DEGREE_LENGTHS = [4, 6, 8]
LENGTH_STRINGS = ["4-year", "6-year", "8-year"]
START_YEARS = [2011, 2013]
START_STRINGS = ["Began in 2011", "Began in 2013"]

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Construct output dictionary in expected result format
    output = {y:{x:LinComb.ZERO for x in START_STRINGS} for y in LENGTH_STRINGS}

    # Populate output dictionary with graduation rates
    for i in range(len(DEGREE_LENGTHS)):
        for j in range(len(START_YEARS)):
            degree_length = DEGREE_LENGTHS[i]
            start_year = START_YEARS[j]

            # Construct integer representations for grads and non-grads
            grad_repr = convert_to_int(True, start_year, degree_length)
            non_grad_repr = convert_to_int(False, start_year, degree_length)

            # Count number of grads and non-grads
            grads = LinCombFxp(sum([x == grad_repr for x in data]))
            non_grads = LinCombFxp(sum([x == non_grad_repr for x in data]))
            total = grads + non_grads

            grad_rate = grads / (total + (total == 0))
            output[LENGTH_STRINGS[i]][START_STRINGS[j]] = grad_rate

    # Assert results are correct
    for degree_length in results:
        for start_year in results[degree_length]:
            output[degree_length][start_year].assert_eq(results[degree_length][start_year])

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
    data = list(map(PrivVal, data))

    results = json.load(open('data/Degrees Awarded/results.json', 'r'))
    correct_hash = json.load(open('data/Degrees Awarded/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified average graduation rates!")
        
