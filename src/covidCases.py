import json
from common import flatten, count_ops
from pysnark.runtime import snark
from pysnark.fixedpoint import PrivValFxp
from pysnark.poseidon_hash import poseidon_hash

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Compute percentage per category
    total_cases = sum([data[x] for x in data])
    percentage_per_category = {x:data[x] * 100 / total_cases for x in data}

    # Check output
    for x in data:
        percentage_per_category[x].assert_eq(results[x])

if __name__ == '__main__':
    data = json.load(open('data/COVID/data.json', 'r'))
    data = {x:PrivValFxp(data[x]) for x in data}
    results = json.load(open('data/COVID/results.json', 'r'))
    correct_hash = json.load(open('data/COVID/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified COVID cases by age!")