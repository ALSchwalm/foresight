from predrng import lcg, glibc


def predict_state(values, platform):
    pass


def generate_from_outputs(prev_values, platform):
    state = predict_state(prev_values, platform)

    if platform == "windows":
        yield from lcg.generate_values(state)
    elif platform == "linux":
        yield from glibc.random.generate_values(state)


def generate_from_seed(seed, platform):
    if platform == "windows":
        yield from lcg.generate_from_seed(seed)
    if platform == "linux":
        yield from glibc.random.generate_from_seed(seed)
