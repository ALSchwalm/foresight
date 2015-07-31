"""
Predict RNG

Usage:
  predict_rng msvc (rand|rand_r) <count> (--seed=<seed> | <output>...)
  predict_rng glibc (rand|random|rand_r) <count> (--seed=<seed> | <output>...)
  predict_rng lcg <multiplier> <increment> <modulus> <bitshift> <count> (--seed=<seed> | <output>...)
"""

from docopt import docopt
from predrng import lcg, glibc
from predrng.glibc import random
from itertools import islice


def handle_msvc(args, count, outputs):
    if args["rand"] or args["rand_r"]:
        if args["--seed"]:
            seed = int(args["--seed"])
            for value in islice(lcg.generate_from_seed(seed), 0, count):
                print(value)
        else:
            for value in islice(lcg.generate_from_outputs(outputs), 0, count):
                print(value)


def handle_lcg(args, count, outputs):
    a = int(args["<multiplier>"])
    c = int(args["<increment>"])
    m = int(args["<modulus>"])
    bitshift = int(args["<bitshift>"])
    if args["--seed"]:
        seed = int(args["--seed"])
        for value in islice(lcg.generate_from_seed(seed, a, c, m, bitshift), 0,
                            count):
            print(value)
    else:
        for value in islice(lcg.generate_from_outputs(outputs, a, c, m,
                                                      bitshift), 0, count):
            print(value)


def handle_glibc(args, count, outputs):
    if args["--seed"]:
        seed = int(args["--seed"])
        for value in islice(glibc.random.generate_from_seed(seed), 0, count):
            print(value)
    else:
        for value in islice(glibc.random.generate_from_outputs(outputs), 0, count):
            print(value)


def main():
    args = docopt(__doc__)

    outputs = None
    if args["<output>"]:
        outputs = [int(output) for output in args["<output>"]]

    count = int(args["<count>"])
    if args["msvc"]:
        handle_msvc(args, count, outputs)
    elif args["lcg"]:
        handle_lcg(args, count, outputs)
    elif args["glibc"]:
        handle_glibc(args, count, outputs)

if __name__ == "__main__":
    main()
