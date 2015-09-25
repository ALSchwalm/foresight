""" Predicts and simulates outputs from the PHP 'rand' function. This
is generally a call to the corresponding 'rand' of the platform C
implementation.
"""

import foresight.glibc.random
import foresight.msvc.rand
from foresight import lcg
from math import log, ceil


def _platform_tmax(platform):
    if platform == "windows":
        return 1 << 15
    elif platform == "linux":
        return 2147483647


def predict_state(values, platform, value_range=None):
    if value_range is None:
        if platform == "windows":
            return foresight.msvc.rand.predict_state(values)
        elif platform == "linux":
            return foresight.glibc.random.predict_state(values)
    else:
        tmax = _platform_tmax(platform)
        min = value_range[0]
        max = value_range[1]
        init = int((values[0] - min) * (tmax + 1.0) / (max - min + 1.0))
        operation = lambda x: rand_range(x, min, max, tmax)

        if platform == "windows":
            for i in range(2**ceil(16 - log(max - min, 2))):
                for lower in range(2**16):
                    num = (init << 16) | lower
                    state = lcg.verify_candidate(num, values[1:], a=214013,
                                                 c=2531011, m=2**31,
                                                 masked_bits=16,
                                                 operation=operation)
                    if state is not None:
                        return state
                init += 1
        elif platform == "linux":
            raise NotImplementedError("Linux PHP bounded rand is not yet supported")


def rand_range(n, min, max, tmax):
    '''
    If a lower and upper bound is specified, the following macro is used
    to shift the output into the target range in a more-or-less uniform
    way.

    #define RAND_RANGE(__n, __min, __max, __tmax) \
      (__n) = (__min) + (zend_long) ((double) ( (double) (__max) - (__min) + 1.0) * ((__n) / ((__tmax) + 1.0)))
    '''
    return int(min + (max - min + 1.0) * n // (tmax + 1.0))


def from_outputs(prev_values, platform, value_range=None):
    state = predict_state(prev_values, platform, value_range)

    tmax = _platform_tmax(platform)
    if platform == "windows":
        gen = foresight.msvc.rand.generate_values(state)
    elif platform == "linux":
        gen = foresight.glibc.random.generate_values(state)

    if value_range is None:
        value_range = [0, tmax]
    for prediction in gen:
        yield rand_range(prediction, value_range[0],
                         value_range[1], tmax)


def from_seed(seed, platform, value_range=None):
    tmax = _platform_tmax(platform)
    if platform == "windows":
        gen = foresight.msvc.rand.from_seed(seed)
    elif platform == "linux":
        gen = foresight.glibc.random.from_seed(seed)

    if value_range is None:
        value_range = [0, tmax]
    for prediction in gen:
        yield rand_range(prediction, value_range[0],
                         value_range[1], tmax)
