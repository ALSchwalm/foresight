""" Simulates and predicts outputs from the GNU C Library function `rand_r`.
"""

from math import log

__all__ = [
    "from_seed",
    "from_outputs"
]


MULTIPLIER = 1103515245
INCREMENT = 12345
MODULUS = 2**32


def find_components(value):
    """ Extract the three values which have been combined to
    form the given output.
    """
    r1 = value >> 20                  # 11 most significant bits
    r2 = (2**10 - 1) & (value >> 10)  # 10 middle bits
    r3 = (2**10 - 1) & value          # 10 least significant bits
    return r1, r2, r3


def verify_candidate(candidate, values, output_modulus):
    """ For a given possible state (candidate), determine whether
    it is a possible true state, given a list of outputs and modulus.

    Returns None if candidate is non-viable; otherwise, returns the
    state after outputting the given values (i.e., the current state).
    """
    next = candidate
    for value in values:
        r1, r2, r3 = find_components(value)
        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        r1 = (next // 2**16) % 2**11

        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        r2 = (next // 2**16) % 2**10

        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        r3 = (next // 2**16) % 2**10

        output = r1 << 20
        output |= (r2 << 10)
        output |= r3
        if not output_modulus:
            if output != value:
                return None
        else:
            if output % output_modulus != value:
                return None
    return next


def predict_state(values, output_modulus=None):
    r1, r2, r3 = find_components(values[0])

    for i in range(2**16):
        if i % 2**11 != r1:
            continue
        for j in range(2**16):
            next = i * 2**16 + j
            if r1 != (next // 2**16) % 2**11:
                continue
            next *= MULTIPLIER
            next += INCREMENT
            next %= MODULUS

            if r2 != (next // 2**16) % 2**10:
                continue
            next *= MULTIPLIER
            next += INCREMENT
            next %= MODULUS
            if r3 == (next // 2**16) % 2**10:
                state = verify_candidate(next, values[1:], output_modulus)
                if state is not None:
                    return state


def generate_values(state, output_modulus=None):
    next = state

    while(True):
        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        result = (next // 2**16) % 2**11

        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        result <<= 10
        result ^= (next // 2**16) % 2**10

        next *= MULTIPLIER
        next += INCREMENT
        next %= MODULUS
        result <<= 10
        result ^= (next // 2**16) % 2**10
        if not output_modulus:
            yield result
        else:
            yield result % output_modulus


def from_outputs(prev_values, output_modulus=None):
    if output_modulus:
        for i in range(2**(32 - int(log(output_modulus, 2)))):
            initial = output_modulus * i + prev_values[0]
            state = verify_candidate(initial, prev_values[1:], output_modulus)
            if state:
                break
    else:
        state = predict_state(prev_values, output_modulus)

    if state is None:
        raise RuntimeError("No viable candidate found. Some values may"
                           " not be consecutive.")
    yield from generate_values(state, output_modulus)


def from_seed(seed, output_modulus=None):
    yield from generate_values(seed, output_modulus)
