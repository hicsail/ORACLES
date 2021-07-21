import json
from common import flatten, count_ops
from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import LinCombFxp
from pysnark.poseidon_hash import poseidon_hash

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Compute percentage per category
    total_cases = len(data)

    data = {
        "0-19": LinCombFxp(sum([(0 <= x) & (x <= 19) for x in data])),
        "20-29": LinCombFxp(sum([(20 <= x) & (x <= 29) for x in data])),
        "30-39": LinCombFxp(sum([(30 <= x) & (x <= 39) for x in data])),
        "40-49": LinCombFxp(sum([(40 <= x) & (x <= 49) for x in data])),
        "50-59": LinCombFxp(sum([(50 <= x) & (x <= 59) for x in data])),
        "60-69": LinCombFxp(sum([(60 <= x) & (x <= 69) for x in data])),
        "70-79": LinCombFxp(sum([(70 <= x) & (x <= 79) for x in data])),
        "80+": LinCombFxp(sum([80 <= x for x in data]))
    }
    
    percentage_per_category = {x:data[x] / total_cases for x in data}

    # Check output
    for x in data:
        percentage_per_category[x].assert_eq(results[x])

if __name__ == '__main__':
    data = json.load(open('data/COVID/data.json', 'r'))
    data = [PrivVal(x['age']) for x in data if x['covid'] == True]
    results = json.load(open('data/COVID/results.json', 'r'))
    correct_hash = json.load(open('data/COVID/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified COVID cases by age!")