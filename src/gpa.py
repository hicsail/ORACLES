from common import flatten, count_ops
from pysnark.runtime import snark, PrivVal
from pysnark.fixedpoint import PrivValFxp
from pysnark.poseidon_hash import poseidon_hash

@snark
def compute(data, results, correct_hash):
    # Compute commitment
    hashed_data = poseidon_hash(flatten(data))
    [x.assert_eq(y) for (x,y) in zip(hashed_data, correct_hash)]

    # Compute GPA
    total = sum(data)
    num_students = PrivVal(len(data))
    gpa = total / num_students

    # Assert GPAs match
    gpa.assert_eq(results)

if __name__ == "__main__":
    data = [3.0, 3.4, 2.3, 4.0, 3.8, 2.6]
    data = [PrivValFxp(x) for x in data]
    results = 3.1796875
    correct_hash = [14881611281449098881494411741949295589753503020288873600598525691590595578845,
                    3435532317483150868219412711120858263178735851271792327085056805091609162997,
                    6678028067310553066516917272138683945237950974535046093126817351999384698723,
                    1190464966308886353495781666839595039502310509909317614817781318509062364533]

    compute(data, results, correct_hash)
    # count_ops(lambda x,y,z: compute(x,y,z), (data, results, correct_hash))
    print("Successfully verified GPAs!")
