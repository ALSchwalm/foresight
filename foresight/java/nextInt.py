from ctypes import c_int32
from foresight import java
from foresight.java import next_bits

__all__ = [
    "from_seed",
    "from_outputs"
]


def from_seed(seed):
    gen = java.next_bits.from_seed(seed, 32)
    while True:
        yield c_int32(next(gen)).value


def from_outputs(outputs):
    gen = java.next_bits.from_outputs(outputs, 32)
    while True:
        yield c_int32(next(gen)).value
