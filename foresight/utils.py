from math import log


def check_enough_values(num_values, value_bits, state_bits, modulus=None):
    if modulus:
        return log(modulus, 2) * num_values >= state_bits
    else:
        return num_values * value_bits >= state_bits
