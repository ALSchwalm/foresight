""" Predicts and simulates outputs from the Microsoft Visual C++ (MSVC)
compiler implementation of the standard 'rand' function.

"""


from foresight import lcg

__all__ = [
    "from_seed",
    "from_outputs"
]


def predict_state(values, output_modulus=None):
    return lcg.predict_state(values, a=214013, c=2531011,
                             m=2**31, masked_bits=16,
                             output_modulus=output_modulus)


def generate_values(state, output_modulus=None):
    yield from lcg.generate_values(state, a=214013, c=2531011,
                                   m=2**31, masked_bits=16,
                                   output_modulus=output_modulus)


def from_outputs(prev_values, output_modulus=None):
    yield from lcg.from_outputs(prev_values, a=214013, c=2531011, m=2**31,
                                masked_bits=16, output_modulus=output_modulus)


def from_seed(seed, output_modulus=None):
    yield from lcg.from_seed(seed, a=214013, c=2531011, m=2**31,
                             masked_bits=16, output_modulus=output_modulus)
