from predrng import lcg, glibc


def predict_state(values, platform):
    pass


def rand_range(n, min, max, tmax):
    '''
    If a lower and upper bound is specified, the following macro is used
    to shift the output into the target range in a more-or-less uniform
    way.

    #define RAND_RANGE(__n, __min, __max, __tmax) \
      (__n) = (__min) + (zend_long) ((double) ( (double) (__max) - (__min) + 1.0) * ((__n) / ((__tmax) + 1.0)))
    '''
    return min + int((max - min + 1.0) * n / (tmax + 1.0))


def generate_from_outputs(prev_values, platform, range=[]):
    state = predict_state(prev_values, platform)
    if platform == "windows":
        yield from lcg.generate_values(state)
    elif platform == "linux":
        yield from glibc.random.generate_values(state)


def generate_from_seed(seed, platform, range=[]):
    if platform == "windows":
        gen = lcg.generate_from_seed(seed)
        tmax = 1 << 15
    elif platform == "linux":
        gen = glibc.random.generate_from_seed(seed)
        tmax = 2147483647

    if not range:
        range = [0, tmax]
    while True:
        if range:
            yield rand_range(next(gen), range[0], range[1], tmax)
        else:
            yield next(gen)
