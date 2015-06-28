import itertools
import argparse

def lcg(state, a, c, m, masked_bits):
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
            if lcg(possible_state, a, c, m, masked_bits) == values[n]:
                possible_state = lcg(possible_state, a, c, m, masked_bits=0)
            else:
                break
        else:
            candidates.append(possible_state)
    return candidates

def generate_values(prev_values, a, c, m, masked_bits, noexcept=False):
    '''
    Generate a list of values from a linear congruential algorithm.

    @param prev_values: A list of consecutive values output by the LCG
    @param a: The multiplier
    @param c: The increment
    @param m: The modulus value
    @param masked_bits: The number of lower order bits to drop
    @param noexcept: If True, return None instead of raising an exception
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
    while(True):
        yield lcg(state, a, c, m, masked_bits)
        state = lcg(state, a, c, m, masked_bits=0)

# values = [32376, 28745, 23832]

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="lcgpred", description='Predict output from an LCG')
    parser.add_argument('count', type=int, help='Number of values to predict')
    parser.add_argument('oldvalues', type=int, nargs='+', help='Previous consecutive output from the LCG')

    parser.add_argument('-a', '--multiplier', type=int, help='The multiplier', default=214013)
    parser.add_argument('-c', '--increment', type=int, help='The increment', default=2531011)
    parser.add_argument('-m', '--modulus', type=int, help='The modulus value', default=2**31)
    parser.add_argument('-b', '--maskedbits', type=int, help='The number of lower order bits to drop', default=16)

    args = parser.parse_args()

    for i in itertools.islice(generate_values(args.oldvalues,
                                              args.multiplier,
                                              args.increment,
                                              args.modulus,
                                              args.maskedbits), 0, args.count):
        print(i)
