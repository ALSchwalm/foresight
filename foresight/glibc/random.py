""" Predicts and simulates outputs from the GNU C Library 'random' function.
This is also (generally) the behavior of the 'rand' implementation under
glibc.

The algorithm used is well-documented here:
http://www.mathstat.dal.ca/~selinger/random/

"""

__all__ = [
    "from_seed",
    "from_outputs"
]


class State(object):
    """ A simple type representing a numeric value, where the least
    significant bit may be currently unknown.
    """
    def __init__(self, value, lsb):
        self.value = value
        self.lsb = lsb
        self.uncertain = True

    def predicted(self):
        """ Returns the value represented by this state, as though the
        least significant bit is correct."""

        return (self.value << 1) | self.lsb


def predict_state(values):
    values = [State(i, 0) for i in values]

    for i, value in enumerate(values):
        if i < 31:
            continue

        predicted_value = values[i-3].predicted()
        predicted_value += values[i-31].predicted()
        predicted_value = (predicted_value % 2**32) >> 1

        if value.value == predicted_value:
            if not values[i-31].uncertain and values[i-31].lsb:
                values[i-3].lsb = 0
                values[i-3].uncertain = False
        elif value.value == predicted_value+1:
            values[i-3].lsb = 1
            values[i-3].uncertain = False
            values[i-31].lsb = 1
            values[i-31].uncertain = False
        else:
            # Sanity check
            assert(False)

        # Sanity check
        if (not values[i-3].uncertain) and (not values[i-31].uncertain):
            predicted_value = values[i-3].predicted()
            predicted_value += values[i-31].predicted()
            predicted_value = (predicted_value % 2**32) >> 1
            assert(value.value == predicted_value)

    #TODO: remove this once I can figure out why the predictions are sometimes
    # incorrect even when there is no remaining uncertainty (around 500 inputs)
    print("\nWarning: Some predictions my be incorrect.\n")
    return [v.predicted() for v in values[-38:-4]]


def generate_values(state):
    def inner(state):
        while True:
            predicted_value = state[31]
            predicted_value += state[3]
            predicted_value = predicted_value % 2**32
            state = state[1:] + [predicted_value]
            yield predicted_value >> 1
    gen = inner(state)
    for _ in range(4):
        next(gen)
    yield from gen


def from_outputs(prev_values):
    state = predict_state(prev_values)
    yield from generate_values(state)


def from_seed(seed):
    state = [seed]
    for i in range(1, 31):
        state.append((16807 * state[i-1]) % (2**31-1))
    state += state[0:3]
    gen = generate_values(state)

    # 4 are skipped by generate_values, so skip remaining 306
    for _ in range(306):
        next(gen)
    yield from gen
