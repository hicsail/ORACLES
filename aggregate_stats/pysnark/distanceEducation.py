import json
from pysnark import runtime
from pysnark.runtime import snark, PrivVal, LinCombFxp

@snark 
def compute(data, lfa_data, results):
    # Compute pre-LFA data
    output = {
        "Pre-COVID": {},
        "Post-COVID": {}
    }

    num_students = PrivVal(len(data))

    only_distance = LinCombFxp.fromvar(sum([i == 1 for i in data]), True)
    some_distance = LinCombFxp.fromvar(sum([i == 2 for i in data]), True)
    no_distance = LinCombFxp.fromvar(sum([i == 3 for i in data]), True)
    
    output["Pre-COVID"] = {
        "Only Distance Education": only_distance / num_students,
        "Some Distance": some_distance / num_students,
        "No Distance": no_distance / num_students
    }
    
    num_lfa_students = PrivVal(len(data))

    lfa_only_distance = LinCombFxp.fromvar(sum([i == 1 for i in lfa_data]), True)
    lfa_some_distance = LinCombFxp.fromvar(sum([i == 2 for i in lfa_data]), True)
    lfa_no_distance = LinCombFxp.fromvar(sum([i == 3 for i in lfa_data]), True)
    
    output["Post-COVID"] = {
        "Only Distance Education": lfa_only_distance / num_lfa_students,
        "Some Distance": lfa_some_distance / num_lfa_students,
        "No Distance": lfa_no_distance / num_lfa_students
    }

    for time_period in results:
        for distance_status in results[time_period]:
            output[time_period][distance_status].assert_eq(results[time_period][distance_status])

def status_to_int(student):
    if student["Enrolled in only distance education"]:
        return 1
    if student["Enrolled in some distance education"]:
        return 2
    if student["Not enrolled in any distance education"]:
        return 3
    return 0

if __name__ == '__main__':
    runtime.bitlength = 17

    data = json.load(open('../data/LFA/data_preLFA.json', 'r'))
    undergrad_data = [PrivVal(status_to_int(x)) for x in data["UNDERGRADUATE DISTANCE EDUCATION STATUS"]]
    graduate_data = [PrivVal(status_to_int(x)) for x in data["GRADUATE DISTANCE EDUCATION STATUS"]]
    data = undergrad_data + graduate_data

    lfa_data = json.load(open('../data/LFA/data_LFA.json', 'r'))
    undergrad_lfa_data = [PrivVal(status_to_int(x)) for x in lfa_data["UNDERGRADUATE DISTANCE EDUCATION STATUS"]]
    graduate_lfa_data = [PrivVal(status_to_int(x)) for x in lfa_data["GRADUATE DISTANCE EDUCATION STATUS"]]
    lfa_data = undergrad_data + graduate_data

    results = json.load(open('../data/LFA/results.json', 'r'))
    
    compute(data, lfa_data, results)
    print("Successfully verified LFA data!")
