from pysnark.runtime import LinComb, benchmark
from pysnark.fixedpoint import LinCombFxp
from pysnark.boolean import LinCombBool

def count_ops(fn, args):
    benchmark()(fn)(*args)

def flatten(vals):
	if isinstance(vals, LinComb):
		return [vals]
	if isinstance(vals, LinCombFxp):
		return [vals]
	if isinstance(vals, LinCombBool):
		return [vals]
	if isinstance(vals, list):
		res = []
		for val in vals:
			res += flatten(val)
		return res
	if isinstance(vals, dict):
		res = []
		for val in vals.values():
			res += flatten(val)
		return res
	raise RuntimeError("Invalid type for poseidon_hash")

if __name__ == "__main__":
	from pysnark.runtime import PrivVal

	# Nested Lists
	out = flatten([
		[[PrivVal(2)]],
		[[[PrivVal(2), PrivVal(3)]]]
	])
	res = [PrivVal(2), PrivVal(2), PrivVal(3)]
	assert all([(x == y).val() == 1 for (x,y) in zip(out, res)])

	# Dictionaries
	out = flatten({"a": PrivVal(2), "b": PrivVal(2)})
	res = [PrivVal(2), PrivVal(2)]
	assert all([(x == y).val() == 1 for (x,y) in zip(out, res)])

	# Nested Dictionaries
	out = flatten({
		"a": PrivVal(2),
		"b": PrivVal(2),
		"c": {
			"a": PrivVal(1), 
			"b": PrivVal(2)
		},
		"d": {
			"a": PrivVal(3)
		}
	})
	res = [PrivVal(2), PrivVal(2), PrivVal(1), PrivVal(2), PrivVal(3)]
	assert all([(x == y).val() == 1 for (x,y) in zip(out, res)])

	# List in Dictionary
	out = flatten({
		"a": [PrivVal(2)],
		"b": PrivVal(2),
		"c": [PrivVal(1), PrivVal(2)],
		"d": {
			"a": [PrivVal(3)]
		}
	})
	res = [PrivVal(2), PrivVal(2), PrivVal(1), PrivVal(2), PrivVal(3)]
	assert all([(x == y).val() == 1 for (x,y) in zip(out, res)])

	# Dictionary in List
	out = flatten([
		[[{"a": PrivVal(2)}]],
		[[[PrivVal(2), PrivVal(3)]]],
		{"b": PrivVal(5)}
	])
	res = [PrivVal(2), PrivVal(2), PrivVal(3), PrivVal(5)]
	assert all([(x == y).val() == 1 for (x,y) in zip(out, res)])