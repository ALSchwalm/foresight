from ctypes import c_int32
from foresight import java
from foresight.java import next_bits

__all__ = [
    "from_seed",
    "from_outputs"
]


def from_seed(seed):
    for prediction in java.next_bits.from_seed(seed, 32):
        yield c_int32(prediction).value


def from_outputs(outputs):
    for prediction in java.next_bits.from_outputs(outputs, 32):
        yield c_int32(prediction).value
