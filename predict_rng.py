#!/usr/bin/env python
"""
Usage:
  predict_rng msvc  (rand|rand_r) <count> <output>...
  predict_rng msvc  (rand|rand_r) <count> --seed=<seed>
  predict_rng glibc (rand|random|rand_r) <count> <output>...
  predict_rng glibc (rand|random|rand_r) <count> --seed=<seed>
  predict_rng php   (linux|windows) rand <count> <output>...
  predict_rng php   (linux|windows) rand <count> --seed=<seed>
  predict_rng lcg <multiplier> <increment> <modulus> <bitshift> <count> <output>...
  predict_rng lcg <multiplier> <increment> <modulus> <bitshift> <count> --seed=<seed>

Description:
  Given OUTPUTs from a random number generator (glibc's rand_r, PHP rand, etc),
  predict_rng predicts the next COUNT outputs. Alternately, predict_rng can
  be passed the SEED, which will be used to produce the first COUNT outputs
  that would be returned from the random number generator.
"""

from docopt import docopt
from predrng import lcg, glibc, php
from predrng.glibc import random, rand_r
from predrng.php import rand
from itertools import islice


def print_from_gen(generator, count):
    for v in islice(generator, 0, count):
        print(v)


def handle_msvc(args, count, outputs, seed):
    if args["rand"] or args["rand_r"]:
        if seed:
            print_from_gen(lcg.generate_from_seed(seed), count)
        else:
            print_from_gen(lcg.generate_from_outputs(outputs), count)


def handle_lcg(args, count, outputs, seed):
    a = int(args["<multiplier>"])
    c = int(args["<increment>"])
    m = int(args["<modulus>"])
    bitshift = int(args["<bitshift>"])
    if seed:
        print_from_gen(lcg.generate_from_seed(seed, a, c, m, bitshift), count)
    else:
        print_from_gen(lcg.generate_from_outputs(outputs, a, c, m, bitshift), count)


def handle_glibc(args, count, outputs, seed):
    if args["rand"] or args["random"]:
        if seed:
            print_from_gen(glibc.random.generate_from_seed(seed), count)
        else:
            print_from_gen(glibc.random.generate_from_outputs(outputs), count)
    elif args["rand_r"]:
        if seed:
            print_from_gen(glibc.rand_r.generate_from_seed(seed), count)
        else:
            print_from_gen(glibc.rand_r.generate_from_outputs(outputs), count)


def handle_php(args, count, outputs, seed):
    if args["windows"]:
        platform = "windows"
    elif args["linux"]:
        platform = "linux"

    if args["rand"]:
        if seed:
            print_from_gen(php.rand.generate_from_seed(seed, platform), count)
        else:
            print_from_gen(php.rand.generate_from_outputs(outputs, platform), count)


def main():
    args = docopt(__doc__)

    outputs = None
    if args["<output>"]:
        outputs = [int(output) for output in args["<output>"]]

    seed = None
    if args["--seed"]:
        seed = int(args["--seed"])

    count = int(args["<count>"])
    if args["msvc"]:
        handle_msvc(args, count, outputs, seed)
    elif args["lcg"]:
        handle_lcg(args, count, outputs, seed)
    elif args["glibc"]:
        handle_glibc(args, count, outputs, seed)
    elif args["php"]:
        handle_php(args, count, outputs, seed)

if __name__ == "__main__":
    main()
