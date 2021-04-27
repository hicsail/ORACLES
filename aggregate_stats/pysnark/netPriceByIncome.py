import json
from pysnark.runtime import snark, PrivVal

@snark
def compute(data, results):
    #  Begin with just 2016-2017
    data = {}
    for year in data:
        data[year] = {}
        for income in data[year]:
            year_data = data[year][income]
            total = sum(year_data)
            length = PrivVal(len(year_data))
            data[year][income] = total / length

    # Check equality
    for year in results:
        for income in results[year]:
            data[year][income].assert_eq(results[year][income])

if __name__ == '__main__':
    data = json.load(open('../data/Net Price by Income/data.json', 'r'))
    for year in data:
        for income in data[year]:
            data[year][income] = list(map(PrivVal, data[year][income]))
    results = json.load(open ('../data/Net Price by Income/results.json', 'r'))

    compute(data, results)
    print("Successfully verified price paid per income bracket!")
