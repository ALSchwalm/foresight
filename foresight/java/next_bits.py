""" java.utils.Random utility functions.

These methods simulate the Random object 'next' function, and
are used to implement the other Random functions (nextInt, nextDouble, etc.)

Note that it is an error to pass a value for 'bits' that is larger than 32.
"""

from foresight import lcg
from ctypes import c_uint32


MULTIPLIER = 25214903917
INCREMENT = 11
MODULUS = 2**48
SHIFT_BITS = 16


def predict_state(values):
    return lcg.predict_state(values,
                             MULTIPLIER,
                             INCREMENT,
                             MODULUS,
                             SHIFT_BITS)


def generate_values(state, bits):
    gen = lcg.generate_values(state,
                              MULTIPLIER,
                              INCREMENT,
                              MODULUS,
                              0)
    for prediction in gen:
        yield prediction >> (48 - bits)


def from_seed(seed, bits):
    seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    gen = lcg.from_seed(seed, MULTIPLIER,
                        INCREMENT, MODULUS, 0)
    for prediction in gen:
        yield prediction >> (48 - bits)


def from_outputs(outputs, bits):
    outputs = [c_uint32(o).value for o in outputs]
    gen = lcg.from_outputs(outputs, MULTIPLIER,
                           INCREMENT, MODULUS,
                           48-bits)
    for prediction in gen:
        yield prediction & ((1 << bits) - 1)
