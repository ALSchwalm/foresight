from math import log, ceil
from foresight.utils import check_enough_values

__all__ = [
    "from_seed",
    "from_outputs"
]


def next_state(state, a, c, m, masked_bits):
    '''
    Determine the next value of a linear congruential generator

    An LCG outputs values with the following recurrence relation:

        state_(n+1) = a * state_n + c (mod m)
        value_n = state_n >> masked_bits

    @param state: The current state of the LCG
    @return: The next state, with 'masked_bits' lower order bits removed
    '''
    return ((a * state + c) % m) >> masked_bits


def verify_candidate(possible_state, values, a, c, m, masked_bits, operation=None):
    for value in values:
        if operation is not None:
            if operation(next_state(possible_state, a, c, m, masked_bits)) == value:
                possible_state = next_state(possible_state, a, c, m, masked_bits=0)
            else:
                break
        else:
            if next_state(possible_state, a, c, m, masked_bits) == value:
                possible_state = next_state(possible_state, a, c, m, masked_bits=0)
            else:
                break
    else:
        return possible_state


def predict_state(values, a, c, m, masked_bits, output_modulus=None):
    '''
    Given a list of values from a LCG, predict the internal state

    @param values: A list of consecutive values output from the LCG
    @return: A list of possible internal state values for the LCG
    '''
    if check_enough_values(len(values), log(m, 2) - masked_bits, log(m, 2),
                           output_modulus) is False:
        print("WARNING: Not enough outputs for unique answer. Result may be incorrect.")

    if output_modulus is not None:
        for i in range(ceil(log(m, 2) - masked_bits - log(output_modulus, 2))+1):
            initial = values[0] + i * output_modulus
            for lower_bits in range(2 ** masked_bits):
                possible_state = (initial << masked_bits) + lower_bits
                checked_state = verify_candidate(possible_state,
                                                 values[1:],
                                                 a, c, m, masked_bits,
                                                 lambda x: x % output_modulus)
                if checked_state:
                    return checked_state

    else:
        for lower_bits in range(2 ** masked_bits):
            possible_state = (values[0] << masked_bits) + lower_bits
            checked_state = verify_candidate(possible_state,
                                             values[1:],
                                             a, c, m, masked_bits,
                                             output_modulus)
            if checked_state:
                return checked_state


def generate_values(state, a, c, m, masked_bits, output_modulus=None):
    '''
    Generate a list of values from a linear congruential algorithm.

    @param state: An initial state for the RNG
    @param a: The multiplier
    @param c: The increment
    @param m: The modulus value
    @param masked_bits: The number of lower order bits to drop
    '''

    while(True):
        state = next_state(state, a, c, m, masked_bits=0)
        if output_modulus:
            yield (state >> masked_bits) % output_modulus
        else:
            yield state >> masked_bits


def from_seed(seed, a, c, m, masked_bits, output_modulus=None):
    '''
    Create a continuation that yields random values from an LCG with the given parameters,
    using 'seed' as the initial seed.
    '''
    yield from generate_values(seed, a, c, m, masked_bits, output_modulus)


def from_outputs(prev_values, a, c, m, masked_bits,
                 output_modulus=None, noexcept=False):
    '''
    Create a continuation that yields random values from an LCG with the given parameters,
    recovering the state from the given list of values. Defaults to MSVC constants.
    '''
    state = predict_state(prev_values, a, c, m, masked_bits, output_modulus)

    if state is None:
        if noexcept:
            yield None
        else:
            raise RuntimeError("No viable candidate found. Some values may not be consecutive.")
    yield from generate_values(state, a, c, m, masked_bits, output_modulus)
