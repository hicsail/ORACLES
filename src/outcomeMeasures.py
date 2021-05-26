import json
from pysnark.runtime import snark, PrivVal, LinCombFxp, ignore_errors

@snark
def compute(data, results):
    # Compute outputs
    output = {}
    for category in data:
        num_pell = sum([i >= 10 for i in data[category]])
        num_non_pell = sum([i < 10 for i in data[category]])
        num_all = num_pell + num_non_pell

        received_bachelors_pell = LinCombFxp.fromvar(sum([i == 11 for i in data[category]]), True)
        different_institution_pell = LinCombFxp.fromvar(sum([i == 12 for i in data[category]]), True)
        same_institution_pell = LinCombFxp.fromvar(sum([i == 13 for i in data[category]]), True)

        received_bachelors_non_pell = LinCombFxp.fromvar(sum([i == 1 for i in data[category]]), True)
        different_institution_non_pell = LinCombFxp.fromvar(sum([i == 2 for i in data[category]]), True)
        same_institution_non_pell = LinCombFxp.fromvar(sum([i == 3 for i in data[category]]), True)

        output[category] = {
            "Pell": {
                "Received Bachelor's": received_bachelors_pell / num_pell, 
                "Enrolled at same institution": same_institution_pell / num_pell, 
                "Enrolled at different insitution": different_institution_pell / num_pell
            }, 
            "No Pell": {
                "Received Bachelor's": received_bachelors_non_pell / num_non_pell, 
                "Enrolled at same institution": same_institution_non_pell / num_non_pell, 
                "Enrolled at different insitution": different_institution_non_pell / num_non_pell
            }, 
            "All Students": {
                "Received Bachelor's": (received_bachelors_pell + received_bachelors_non_pell) / num_all, 
                "Enrolled at same institution": (same_institution_pell + same_institution_non_pell) / num_all, 
                "Enrolled at different insitution": (different_institution_pell + different_institution_non_pell) / num_all
            }}

    for category in results:
        for student_type in results[category]:
            for outcome in results[category][student_type]:
                output[category][student_type][outcome].assert_eq(results[category][student_type][outcome])

def outcome_to_int(student):
    if student["Received Bachelor's"]:
        return 1
    if student["Enrolled at same insitution"]:
        return 2
    if student["Enrolled at different insitution"]:
        return 3
    return 0

if __name__ == '__main__':
    data = json.load(open('data/Education Outcomes/data.json', 'r'))
    results = json.load(open('data/Education Outcomes/results.json', 'r'))
    for category in data:
        # Construct inputs for Pell and non-Pell students
        # First 10 students of every category are Pell students
        pell = [PrivVal(10 + outcome_to_int(student)) for student in data[category][:10]]
        non_pell = [PrivVal(outcome_to_int(student)) for student in data[category][10:]]
        data[category] = pell + non_pell

    compute(data, results)
    print("Successfully verified education outcomes!")
