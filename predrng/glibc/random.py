class State(object):
    def __init__(self, value, lsb):
        self.value = value
        self.lsb = lsb
        self.uncertain = True

    def predicted(self):
        return (self.value << 1) | self.lsb


def predict_state(values):
    values = [State(i, 0) for i in values]

    for i, value in enumerate(values):
        if i < 31:
            continue

        predicted_value = values[i-3].predicted()
        predicted_value += values[i-31].predicted()
        predicted_value = (predicted_value % 2**32) >> 1

        # Sanity check
        if (not values[i-3].uncertain) and (not values[i-31].uncertain):
            assert(value.value == predicted_value)

        if value.value == predicted_value:
            values[i-3].lsb = 0
            values[i-3].uncertain = False
            values[i-31].lsb = 0
            values[i-31].uncertain = False
        elif value.value == predicted_value+1:
            if not values[i-31].uncertain:
                values[i-3].lsb = not values[i-31].lsb
                values[i-3].uncertain = False
            else:
                # this can be wrong
                values[i-3].lsb = not values[i-31].lsb
        elif value.value == predicted_value+2:
            values[i-3].lsb = 1
            values[i-3].uncertain = False
            values[i-31].lsb = 1
            values[i-31].uncertain = False
        else:
            # Sanity check
            assert(False)

    for v in values[i-34:i-3]:
        if v.uncertain:
            raise RuntimeError("Unable to find a unique internal state. Not enough values.")
    else:
        return [v.predicted() for v in values[i-34:i-3]]


def generate_values(state):
    while(True):
        predicted_value = state[28]
        predicted_value += state[0]
        predicted_value = predicted_value % 2**32
        state = state[1:] + [predicted_value]
        yield predicted_value >> 1


def generate_from_outputs(prev_values):
    state = predict_state(prev_values)
    gen = generate_values(state)
    for _ in range(4):
        next(gen)
    yield from gen
