import json
from common import flatten, count_ops
from pysnark import runtime
from pysnark.runtime import snark, PrivVal
from pysnark.poseidon_hash import poseidon_hash

INCOME_BRACKETS = [(0, 30000), (30001, 48000), (48001, 75000), (75001, 110000), (110001,)]
BRACKET_STRINGS = ["$0 to $30,000", "$30,001 to $48,000", "$48,001 to $75,000", "$75,001 to $110,000", "$110,001 and more"]

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    output = {year:{} for year in data}
    for year in data:
        output[year] = {}

        # Compute average net tuition for all income brackets except last
        for i in range(len(INCOME_BRACKETS) - 1):
            (bracket_min, bracket_max) = INCOME_BRACKETS[i]

            # Select students in the current bracket
            select_bit = [(bracket_min <= x) & (x <= bracket_max) for x in data[year]["Incomes"]]
            # Get the total net tuition paid by current bracket
            total = sum([x*y for (x,y) in zip(select_bit, data[year]["Tuitions"])])
            # Count the number of students in the current bracket
            num_students = sum(select_bit)

            # Calculate average tuition paid by current bracket
            average_net_tuition = total / (num_students + (num_students == 0))
            output[year][BRACKET_STRINGS[i]] = average_net_tuition

        # Compute average net tuition for $110,001+ bracket
        select_bit = [x >= 110001 for x in data[year]["Incomes"]]
        total = sum([x*y for (x,y) in zip(select_bit, data[year]["Tuitions"])])
        num_students = sum(select_bit)
        average_net_tuition = total / (num_students + (num_students == 0))
        output[year][BRACKET_STRINGS[4]] = average_net_tuition

    # Check equality
    for year in results:
        for income in results[year]:
            output[year][income].assert_eq(results[year][income])

if __name__ == '__main__':
    runtime.bitlength = 20

    raw_data = json.load(open('data/Net Price by Income/data.json', 'r'))

    data = {year:{} for year in raw_data}
    for year in raw_data:
        incomes = [PrivVal(x["Income"]) for x in raw_data[year]]
        tuitions = [PrivVal(x["Net Tuition"]) for x in raw_data[year]]
        data[year] = {
            "Incomes": incomes,
            "Tuitions": tuitions
        }

    results = json.load(open ('data/Net Price by Income/results.json', 'r'))
    correct_hash = json.load(open('data/Net Price by Income/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified price paid per income bracket!")
