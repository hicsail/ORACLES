import json
from common import flatten, count_ops
from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import LinCombFxp
from pysnark.poseidon_hash import poseidon_hash

CATEGORIES = [
    {"Full Time": 1, "First Time": 1},
    {"Full Time": 0, "First Time": 1},
    {"Full Time": 1, "First Time": 0},
    {"Full Time": 0, "First Time": 0},
]
CATEGORY_STRING = [
    "FULL-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
    "PART-TIME, FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
    "FULL-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
    "PART-TIME, NON-FIRST-TIME DEGREE/CERTIFICATE-SEEKING UNDERGRADUATES WHO ENTERED IN 2011-12",
]

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Compute outputs
    output = {}
    for i in range(len(CATEGORIES)):
        full_time = CATEGORIES[i]["Full Time"]
        first_time = CATEGORIES[i]["First Time"]

        # Compute Pell student counts
        received_bachelors_pell_repr = convert_to_int(1, True, first_time, full_time)
        different_institution_pell_repr = convert_to_int(2, True, first_time, full_time)
        same_institution_pell_repr = convert_to_int(3, True, first_time, full_time)
        other_pell_repr = convert_to_int(0, True, first_time, full_time)

        received_bachelors_pell = LinCombFxp(sum([i == received_bachelors_pell_repr for i in data]))
        different_institution_pell = LinCombFxp(sum([i == different_institution_pell_repr for i in data]))
        same_institution_pell = LinCombFxp(sum([i == same_institution_pell_repr for i in data]))
        other_pell = LinCombFxp(sum([i == other_pell_repr for i in data]))

        # Compute non-Pell student counts
        received_bachelors_non_pell_repr = convert_to_int(1, False, first_time, full_time)
        different_institution_non_pell_repr = convert_to_int(2, False, first_time, full_time)
        same_institution_non_pell_repr = convert_to_int(3, False, first_time, full_time)
        other_non_pell_repr = convert_to_int(0, False, first_time, full_time)

        received_bachelors_non_pell = LinCombFxp(sum([i == received_bachelors_pell for i in data]))
        different_institution_non_pell = LinCombFxp(sum([i == different_institution_pell for i in data]))
        same_institution_non_pell = LinCombFxp(sum([i == same_institution_pell for i in data]))
        other_non_pell = LinCombFxp(sum([i == other_non_pell_repr for i in data]))

        # Compute total counts
        num_pell = received_bachelors_pell + different_institution_pell + same_institution_pell + other_pell
        num_non_pell = received_bachelors_non_pell + different_institution_non_pell + same_institution_non_pell + other_non_pell
        num_all = num_pell + num_non_pell

        # Compute statistics
        output[CATEGORY_STRING[i]] = {
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

    # Verify result is correct
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

def convert_to_int(outcome, pell, first_time, full_time):
    student_repr = outcome
    student_repr += pell * 10
    student_repr += int(first_time) * 100
    student_repr += int(full_time) * 1000
    return student_repr

if __name__ == '__main__':
    raw_data = json.load(open('data/Education Outcomes/data.json', 'r'))

    data = []
    for student in raw_data:
        outcome = outcome_to_int(student)
        student_repr = convert_to_int(outcome, student["Pell"], student["First Time"], student["Full Time"])
        data += [PrivVal(student_repr)]

    results = json.load(open('data/Education Outcomes/results.json', 'r'))
    correct_hash = json.load(open('data/Education Outcomes/hash.json', 'r'))

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified education outcomes!")
