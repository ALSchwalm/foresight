from predrng import java
from predrng.java import next_bits


def generate_from_seed(seed):
    gen = java.next_bits.generate_from_seed(seed, 1)
    while True:
        yield bool(next(gen))


def generate_from_outputs(outputs):
    gen = java.next_bits.generate_from_outputs(outputs, 1)
    while True:
        yield bool(next(gen))
