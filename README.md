# ORACLES

This repository contains code for the SIEVE/ORACLES TA1 project, whose goal is to create verifiable computations for legally, socially, or commercially relevant scenarios by constructing intermediate representations (IRs) that can be proved in zero-knowledge. 

The code executes computations and outputs them in the zkInterface intermediate representation format. This zkInterface output can then be used by a third party to verify that the computation was executed correctly, but without revealing the input data to the third party. We assume that the input data has not been modified maliciously. Input data integrity is beyond the scope of these proofs.

## Workflow

To construct a verifiable computation, the prover runs the code in this repository using their private data as input. 

The code outputs `.zkif` zkInterface files, which are then shared to verifiers. Verifiers can verify the computation using backends such as [zkinterface](https://github.com/QED-it/zkinterface/), [Bulletproofs](https://github.com/QED-it/bulletproofs), and [Bellman](https://github.com/QED-it/zkinterface-bellman).

Alternatively, the `.zkif` files can be converted into `.sieve` files in the SIEVE IR format using the [SIEVE IR Toolbox](https://github.mit.edu/sieve-all/zkinterface-sieve) on the MIT GitHub. The computation can also then be verified using the SIEVE IR Toolbox.

## Installing

First, install Python 3 and Rust.

Next, install the PySNARK library along with its requirements:
```
pip3 install git+https://github.com/meilof/pysnark.git@master
pip3 install flatbuffers
```

Install the `zkinterface` Rust library required by PySNARK:
```
git clone https://github.com/QED-it/zkinterface.git
cargo +nightly install --path zkinterface/rust/
```

Finally, clone the ORACLES repo:
```
git clone https://github.com/hicsail/ORACLES.git
cd ORACLES
```

## Running

First, set up environment variables for PySNARK depending on what backend will be used during verification.

For zkInterface:
```
export PYSNARK_BACKEND=zkinterface
```
For Bulletproofs:
```
export PYSNARK_BACKEND=zkifbulletproofs
```
For Bellman:
```
export PYSNARK_BACKEND=zkifbellman
```

Finally, run the appropriate Python script:
```
cd aggregate_stats/pysnark
python3 gpa.py
```

## Verifying

### zkInterface

To verify using zkInterface, first install download and zkInterface:
```
git clone https://github.com/QED-it/zkinterface.git
cargo +nightly install --path zkinterface/rust/
```

Finally, navigate to the folder containing the `.zkif` files and run:
```
zkif validate
zkif simulate
```

### Bulletproofs

To verify using Bulletproofs, first install download and Bulletproofs:
```
git clone https://github.com/QED-it/bulletproofs.git
cargo +nightly install --path bulletproofs/
```

Finally, navigate to the folder containing the `.zkif` files and run:
```
zkif_bulletproofs prove < computation.zkif
zkif_bulletproofs verify < computation.zkif
```

### Bellman

To verify using Bulletproofs, first install download and Bellman:
```
git clone https://github.com/QED-it/zkinterface-bellman.git
cargo +nightly install --path zkinterface-bellman/
```

Finally, navigate to the folder containing the `.zkif` files and run:
```
zkif_bellman setup < computation.zkif
zkif_bellman prove < computation.zkif
zkif_bellman verify < computation.zkif
```

## Implementing Proofs

We use the PySNARK library to convert a computation into a circuit that can be verified. The output circuit is an arithmetic circuit. Hence, our computation must consist of only arithmetic and logical operations. All inputs and variables must also be integers or booleans. Hence, we must convert all inputs into an integer representation.

All inputs must then be converted into a PySNARK data type. `PubVal`s and `PubValFxp`s are public integers and floats respectively, while `PrivVal`s and `PrivValFxp`s are their private equivalents. We turn our secret inputs into private values and let the expected outputs be public values.

We then pass the inputs into a function that executes our computation. We apply the `@snark` decorator to the function. The decorator automatically convert all integer inputs - including those in arrays - into `PubVal`s. Note that floats and contents of dictionaries are not converted. To use these data types, convert their contents into PySNARK data types manually. To make inputs private, construct `PrivVal`s out of them manually **outside the decorated function**. 

Finally, use assertions to show that the computation reached the correct result.

### Notes on implementation

The circuit representing the computation is output as public knowledge. Hence, all operations in our computation should be applied to all inputs to prevent data being revealed. 

For example, we can find the sum of two sets of inputs as follows:
```
set1 = [PrivVal(0), PrivVal(1)]
set2 = [PrivVal(1), PrivVal(2), PrivVal(3)]

sum1 = sum(set1)
sum2 = sum(set2)
```
However, `sum1` will have an in-degree of 2, while the `sum2` gate will have an in-degree of 3. Hence, the verifier can find the number of inputs in each set.

Alternatively, we can encode the second set by multiplying their value by 10. Then, we can modify the computation as follows:
```
inputs = [PrivVal(0), PrivVal(1), PrivVal(10), PrivVal(20), PrivVal(30)]

sum1 = sum([x // 10 for x in inputs])
sum2 = sum([x % 10 for x in inputs]])
```
Here, all operations are applied to all the inputs. This construction prevents the number of inputs in each set being leaked.

### Other Notes

Some floating point operations are not implemented. See https://github.com/meilof/pysnark/blob/master/pysnark/fixedpoint.py.

For performance reasons, PySNARK's integers and floats are 16 bits long by default.
If overflows occur, increase the number of bits as follows:
```
from pysnark import runtime
runtime.bitlength = 20
```

## External Reading
* [What is a zero-knowledge proof?](https://zkp.science/)
* [R1CS](http://www.zeroknowledgeblog.com/index.php/the-pinocchio-protocol/r1cs)