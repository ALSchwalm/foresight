from ctypes import c_int32
from foresight import java
from foresight.java import next_bits


def generate_from_seed(seed):
    gen = java.next_bits.generate_from_seed(seed, 32)
    while True:
        yield c_int32(next(gen)).value


def generate_from_outputs(outputs):
    gen = java.next_bits.generate_from_outputs(outputs, 32)
    while True:
        yield c_int32(next(gen)).value
