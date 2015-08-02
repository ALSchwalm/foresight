from predrng import lcg
from ctypes import c_int, c_uint


def generate_from_seed(seed):
    seed = (seed ^ 0x5DEECE66D) & ((1 << 48) - 1)
    gen = lcg.generate_from_seed(seed,
                                 25214903917,
                                 11,
                                 281474976710656,
                                 16)
    while True:
        yield c_int(next(gen)).value


def generate_from_outputs(outputs):
    outputs = [c_uint(o).value for o in outputs]
    gen = lcg.generate_from_outputs(outputs,
                                    25214903917,
                                    11,
                                    281474976710656,
                                    16)
    while True:
        yield c_int(next(gen)).value
