from ctypes import c_int32, c_int64, c_uint64
from foresight import java
from foresight.java import next_bits
from itertools import combinations


def generate_from_seed(seed):
    gen = java.next_bits.generate_from_seed(seed, 32)
    while True:
        num = c_int64(next(gen) << 32).value
        num += c_int32(next(gen)).value
        yield c_int64(num).value


def generate_from_outputs(outputs):
    extracted_outputs = []
    for output in outputs:
        output = c_uint64(output).value
        extracted_outputs.append(output >> 32)
        extracted_outputs.append(output & ((1 << 32) - 1))

    # Ugly hack, the upper numbers can be off by 1 due to overflow
    state = java.next_bits.predict_state(extracted_outputs)
    for i in range(1, int(len(extracted_outputs)/2)+1):
        if state:
            break
        for inds in combinations(range(0, len(extracted_outputs), 2), i):
            test_outputs = extracted_outputs[:]
            for index in inds:
                test_outputs[index] += 1
            state = java.next_bits.predict_state(test_outputs)
            if state:
                break

    if state is None:
        raise RuntimeError("Unable to recover internal state. (Not enough values?)")

    gen = java.next_bits.generate_values(state, 32)
    while True:
        num = c_int64(next(gen) << 32).value
        num += c_int32(next(gen)).value
        yield c_int64(num).value
