from predrng import java
from predrng.java import next_bits
from ctypes import c_float

def generate_from_seed(seed):
    gen = java.next_bits.generate_from_seed(seed, 24)
    while True:
        yield next(gen) / c_float(1 << 24).value


def generate_from_outputs(outputs):
    gen = java.next_bits.generate_from_outputs(outputs, 24)
    while True:
        yield next(gen) / c_float(1 << 24).value
