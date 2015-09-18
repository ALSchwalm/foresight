""" Predicts and simulates outputs from the Microsoft Visual C++ (MSVC)
compiler implementation of the standard 'rand' function.

This function is implemented using a standard linear congruential
generator with the following constants:

MULTIPLIER=214013
INCREMENT=2531011
MODULUS=2^31
USED_BITS=16

"""


from foresight import lcg

__all__ = [
    "from_seed",
    "from_outputs"
]

# LCG Constants
MULTIPLIER = 214013
INCREMENT = 2531011
MODULUS = 2**31
SHIFT_BITS = 16


def predict_state(values, output_modulus=None):
    return lcg.predict_state(values, a=MULTIPLIER, c=INCREMENT,
                             m=MODULUS, masked_bits=SHIFT_BITS,
                             output_modulus=output_modulus)


def generate_values(state, output_modulus=None):
    yield from lcg.generate_values(state, a=MULTIPLIER, c=INCREMENT,
                                   m=MODULUS, masked_bits=SHIFT_BITS,
                                   output_modulus=output_modulus)


def from_outputs(prev_values, output_modulus=None):
    yield from lcg.from_outputs(prev_values, a=MULTIPLIER, c=INCREMENT,
                                m=MODULUS, masked_bits=SHIFT_BITS,
                                output_modulus=output_modulus)


def from_seed(seed, output_modulus=None):
    yield from lcg.from_seed(seed, a=MULTIPLIER, c=INCREMENT, m=MODULUS,
                             masked_bits=SHIFT_BITS,
                             output_modulus=output_modulus)
