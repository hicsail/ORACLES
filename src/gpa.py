from pysnark.runtime import snark, PrivVal, PrivValFxp

@snark
def compute(data, expected):
    # Compute GPA
    total = sum(data)
    num_students = PrivVal(len(data))
    gpa = total / num_students

    # Assert GPAs match
    gpa.assert_eq(expected)

if __name__ == "__main__":
    data = [3.0, 3.4, 2.3, 4.0, 3.8, 2.6]
    data = [PrivValFxp(x) for x in data]
    expected = 3.18359375

    compute(data, expected)
    print("Successfully verified GPAs!")
