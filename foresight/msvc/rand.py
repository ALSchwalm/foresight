from foresight import lcg


def predict_state(values, output_modulus=None):
    return lcg.predict_state(values, a=214013, c=2531011,
                             m=2**31, masked_bits=16,
                             output_modulus=output_modulus)


def generate_values(state, output_modulus=None):
    yield from lcg.generate_values(state, a=214013, c=2531011,
                                   m=2**31, masked_bits=16,
                                   output_modulus=output_modulus)


def from_outputs(prev_values, output_modulus=None):
    yield from lcg.from_outputs(prev_values, a=214013, c=2531011, m=2**31,
                                masked_bits=16, output_modulus=output_modulus)


def from_seed(seed, output_modulus=None):
    yield from lcg.from_seed(seed, a=214013, c=2531011, m=2**31,
                             masked_bits=16, output_modulus=output_modulus)
