def predict_state(values):
    def find_components(value):
        r1 = value >> 20                  # 11 most significant bits
        r2 = (2**10 - 1) & (value >> 10)  # 10 middle bits
        r3 = (2**10 - 1) & value          # 10 least significant bits
        return r1, r2, r3

    candidates = []
    r1, r2, r3 = find_components(values[0])

    for i in range(2**16):
        if i % 2048 != r1:
            continue
        for j in range(2**16):
            next = i * 65536 + j
            if r1 != (next // 65536) % 2048:
                continue
            next *= 1103515245
            next += 12345
            next %= 2**32

            if r2 != (next // 65536) % 1024:
                continue
            next *= 1103515245
            next += 12345
            next %= 2**32
            if r3 == (next // 65536) % 1024:
                candidates.append(next)

    for candidate in candidates:
        next = candidate
        for value in values[1:]:
            r1, r2, r3 = find_components(value)
            next *= 1103515245
            next += 12345
            next %= 2**32

            if r1 != (next // 65536) % 2048:
                break
            next *= 1103515245
            next += 12345
            next %= 2**32

            if r2 != (next // 65536) % 1024:
                break

            next *= 1103515245
            next += 12345
            next %= 2**32

            if r3 != (next // 65536) % 1024:
                break
        else:
            return next


def generate_values(state):
    next = state

    while(True):
        next *= 1103515245
        next += 12345
        next %= 2**32
        result = (next // 65536) % 2048

        next *= 1103515245
        next += 12345
        next %= 2**32
        result <<= 10
        result ^= (next // 65536) % 1024

        next *= 1103515245
        next += 12345
        next %= 2**32
        result <<= 10
        result ^= (next // 65536) % 1024
        yield result


def generate_from_outputs(prev_values):
    state = predict_state(prev_values)
    yield from generate_values(state)


def generate_from_seed(seed):
    yield from generate_values(seed)
