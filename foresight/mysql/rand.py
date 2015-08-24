from ctypes import c_uint32


def predict_state(values):
    values = [int(round(v * 0x3FFFFFFF, 0)) for v in values]
    seed1 = values[0]
    for i in range(2**30):
        if (seed1 * 3 + i) % 0x3FFFFFFF == values[1]:
            seed2 = i
            break
    return [seed1, seed2]


def generate_values(state):
    # from password.c
    #   max_value = 0x3FFFFFFFL
    #   max_value_dbl=(double) rand_st->max_value;

    # from my_rnd.cc
    #   rand_st->seed1= (rand_st->seed1*3+rand_st->seed2) % rand_st->max_value;
    #   rand_st->seed2= (rand_st->seed1+rand_st->seed2+33) % rand_st->max_value;
    #   return (((double) rand_st->seed1) / rand_st->max_value_dbl);
    seed1, seed2 = state

    while(True):
        seed1 = (seed1 * 3 + seed2) % 0x3FFFFFFF
        seed2 = (seed1 + seed2 + 33) % 0x3FFFFFFF
        yield seed1 / 0x3FFFFFFF


def from_outputs(prev_values):
    state = predict_state(prev_values)
    gen = generate_values(state)

    # only 2 values are needed, so advance past any others we were given
    for _ in prev_values[1:]:
        next(gen)
    while True:
        yield next(gen)


def from_seed(seed):
    seed1 = c_uint32(seed*0x10001+55555555).value
    seed2 = c_uint32(seed*0x10000001).value
    yield from generate_values([seed1, seed2])
