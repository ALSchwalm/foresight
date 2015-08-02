from ctypes import c_int
from predrng import java
from predrng.java import next_bits


def generate_from_seed(seed):
    gen = java.next_bits.generate_from_seed(seed, 32)
    while True:
        yield c_int(next(gen)).value


def generate_from_outputs(outputs):
    gen = java.next_bits.generate_from_outputs(outputs, 32)
    while True:
        yield c_int(next(gen)).value
