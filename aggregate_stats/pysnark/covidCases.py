import json
from pysnark.runtime import snark, PrivValFxp

@snark
def compute(data, correct_result):
    # Compute percentage per category
    total_cases = sum([data[x] for x in data])
    percentage_per_category = {x:data[x]/total_cases for x in data}

    # Check output
    for x in data:
        percentage_per_category[x].assert_eq(correct_result[x])

if __name__ == '__main__':
    data = json.load(open('../data/COVID/data.json', 'r'))
    data = {x:PrivValFxp(data[x]) for x in data}
    result = json.load(open('../data/COVID/results.json', 'r'))

    compute(data, result)
    print("Successfully verified COVID cases by age!")
