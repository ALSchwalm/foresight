def next_lcg(state, a, c, m, masked_bits):
    '''
    Determine the next value of a linear congruential generator

    An LCG outputs values with the following recurrence relation:

        state_(n+1) = a * state_n + c (mod m)
        value_n = state_n >> masked_bits

    @param state: The current state of the LCG
    @return: The next state, with 'masked_bits' lower order bits removed
    '''
    return ((a * state + c) % m) >> masked_bits


def predict_state(values, a, c, m, masked_bits):
    '''
    Given a list of values from a LCG, predict the internal state

    @param values: A list of consecutive values output from the LCG
    @return: A list of possible internal state values for the LCG
    '''
    candidates = []
    for i in range(0, 2 ** masked_bits):
        possible_state = (values[0] << masked_bits) + i
        for n in range(1, len(values)):
            if next_lcg(possible_state, a, c, m, masked_bits) == values[n]:
                possible_state = next_lcg(possible_state, a, c, m, masked_bits=0)
            else:
                break
        else:
            candidates.append(possible_state)
    return candidates


def generate_values(state, a, c, m, masked_bits):
    '''
    Generate a list of values from a linear congruential algorithm.

    @param state: An initial state for the RNG
    @param a: The multiplier
    @param c: The increment
    @param m: The modulus value
    @param masked_bits: The number of lower order bits to drop
    '''

    while(True):
        state = next_lcg(state, a, c, m, masked_bits=0)
        yield state >> masked_bits


def generate_from_seed(seed, a=214013, c=2531011, m=2**31, masked_bits=16):
    '''
    Create a continuation that yields random values from an LCG with the given parameters,
    using 'seed' as the initial seed. Defaults to MSVC constants.
    '''
    yield from generate_values(seed, a, c, m, masked_bits)


def generate_from_outputs(prev_values, a=214013, c=2531011, m=2**31,
                          masked_bits=16, noexcept=False):
    '''
    Create a continuation that yields random values from an LCG with the given parameters,
    recovering the state from the given list of values. Defaults to MSVC constants.
    '''
    state = predict_state(prev_values, a, c, m, masked_bits)

    if len(state) > 1:
        if noexcept:
            yield None
        else:
            raise RuntimeError("Unable to find a unique internal state. Not enough values.")
    elif len(state) == 0:
        if noexcept:
            yield None
        else:
            raise RuntimeError("No viable candidate found. Some values may not be consecutive.")
    state = state[0]
    yield from generate_values(state, a, c, m, masked_bits)
