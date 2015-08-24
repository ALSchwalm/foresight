""" java.utils.Random utility functions.

These methods simulate the Random object 'next' function, and
are used to implement the other Random functions (nextInt, nextDouble, etc.)

Note that it is an error to pass a value for 'bits' that is larger than 32.
"""

from foresight import lcg
from ctypes import c_uint32


def predict_state(values):
    return lcg.predict_state(values,
                             25214903917,
                             11,
                             281474976710656,
                             16)


def generate_values(state, bits):
    gen = lcg.generate_values(state,
                              25214903917,
                              11,
                              281474976710656,
                              0)
    while True:
        yield next(gen) >> (48 - bits)


def generate_from_seed(seed, bits):
    seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    gen = lcg.from_seed(seed, 25214903917,
                        11, 281474976710656, 0)
    while True:
        yield next(gen) >> (48 - bits)


def generate_from_outputs(outputs, bits):
    outputs = [c_uint32(o).value for o in outputs]
    gen = lcg.from_outputs(outputs, 25214903917,
                           11, 281474976710656,
                           48-bits)
    while True:
        yield next(gen) & ((1 << bits) - 1)
