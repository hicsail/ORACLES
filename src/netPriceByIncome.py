import json
from common import flatten, count_ops
from pysnark.runtime import snark, PrivVal
from pysnark.poseidon_hash import poseidon_hash

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    #  Begin with just 2016-2017
    output = {}
    for year in data:
        output[year] = {}
        for income in data[year]:
            year_data = data[year][income]
            total = sum(year_data)
            length = PrivVal(len(year_data))
            output[year][income] = total / length

    # Check equality
    for year in results:
        for income in results[year]:
            output[year][income].assert_eq(results[year][income])

if __name__ == '__main__':
    data = json.load(open('data/Net Price by Income/data.json', 'r'))
    for year in data:
        for income in data[year]:
            data[year][income] = list(map(PrivVal, data[year][income]))
    results = json.load(open ('data/Net Price by Income/results.json', 'r'))
    correct_hash = json.load(open('data/Net Price by Income/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified price paid per income bracket!")
