import json
from pysnark.runtime import snark, PrivValFxp

# Witness:  single table database (D) for COVID Cases in Massachusetts based on the following age ranges: "0-19", "20-29", "30-39", "40-49", "50-59", "60-69", "70-79", "80+"
# Public knowledge: Public IPEDS Statistics that shows the raw total cases for each age range
# Statement: Percentage of total COVID Cases in MA attributed to an age-group is calculated over the entire dataset
# Limitations: PySnark's Fixed Point Value only stores 16 bits for integers, therefore for the computations of a large number of rows, we are unable to calculate the appropriate
# values, so we have scaled down the data so that the sum of all the age ranges is 100 and we scaled each age-range's number of cases proportional to 100.
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
