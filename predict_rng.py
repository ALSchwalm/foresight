#!/usr/bin/env python

import argparse
from textwrap import dedent
from predrng import lcg, glibc, php, java
from predrng.glibc import random, rand_r
from predrng.php import rand
from predrng.java import nextInt, nextLong, nextFloat, nextBoolean
from itertools import islice


def print_from_gen(generator, count):
    for v in islice(generator, 0, count):
        print(v)


def handle_msvc(args):
    if args.function in ("rand",):
        if args.seed:
            print_from_gen(lcg.generate_from_seed(args.seed), args.count)
        else:
            print_from_gen(lcg.generate_from_outputs(args.outputs), args.count)


def handle_java(args):
    if args.function == "nextInt":
        if args.seed:
            print_from_gen(java.nextInt.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(java.nextInt.generate_from_outputs(args.outputs),
                           args.count)
    elif args.function == "nextLong":
        if args.seed:
            print_from_gen(java.nextLong.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(java.nextLong.generate_from_outputs(args.outputs),
                           args.count)
    elif args.function == "nextFloat":
        if args.seed:
            print_from_gen(java.nextFloat.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(java.nextFloat.generate_from_outputs(args.outputs),
                           args.count)
    elif args.function == "nextBoolean":
        if args.seed:
            print_from_gen(java.nextBoolean.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(java.nextBoolean.generate_from_outputs(args.outputs),
                           args.count)


def handle_lcg(args):
    if args.seed:
        print_from_gen(lcg.generate_from_seed(args.seed,
                                              args.multiplier,
                                              args.increment,
                                              args.modulus,
                                              args.bitshift), args.count)
    else:
        print_from_gen(lcg.generate_from_outputs(args.outputs,
                                                 args.multiplier,
                                                 args.increment,
                                                 args.modulus,
                                                 args.bitshift), args.count)


def handle_glibc(args):
    if args.function in ("rand", "random"):
        if args.seed:
            print_from_gen(glibc.random.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(glibc.random.generate_from_outputs(args.outputs),
                           args.count)
    elif args.function == "rand_r":
        if args.seed:
            print_from_gen(glibc.rand_r.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(glibc.rand_r.generate_from_outputs(args.outputs),
                           args.count)


def handle_php(args):
    if args.function == "rand":
        if args.seed:
            print_from_gen(php.rand.generate_from_seed(args.seed, args.platform),
                           args.count)
        else:
            print_from_gen(php.rand.generate_from_outputs(args.outputs, args.platform),
                           args.count)

def add_basic_configuration(parser):
    parser.add_argument("count", type=int,
                        help="The number of outputs to predict")

    parser.add_argument("-s", "--seed", type=int,
                        help="The initial seed")
    parser.add_argument("outputs", nargs="*", type=int,
                        help="Outputs from this RNG", metavar="output")

def setup_glibc_parser(sp):
    sp_glibc = sp.add_parser("glibc", help="Predict outputs from GNU C Library random functions")
    sp_glibc.add_argument('function', choices=('rand', 'random', 'rand_r'),
                          help="Source of outputs")
    add_basic_configuration(sp_glibc)


def setup_msvc_parser(sp):
    sp_msvc = sp.add_parser("msvc", help="Predict outputs from Microsoft Visual C++ random functions")
    sp_msvc.add_argument('function', choices=('rand',),
                         help="Source of outputs")
    add_basic_configuration(sp_msvc)


def setup_php_parser(sp):
    sp_php = sp.add_parser("php", help="Predict outputs from PHP random functions")
    sp_php.add_argument('platform', choices=('linux', 'windows'),
                        help="Platform PHP is running on")
    sp_php.add_argument('function', choices=('rand',),
                        help="Source of outputs")
    add_basic_configuration(sp_php)


def setup_java_parser(sp):
    sp_java = sp.add_parser("java", help="Predict outputs from java.util.Random")
    sp_java.add_argument('function', choices=('nextInt', 'nextLong',
                                              'nextFloat', 'nextBoolean'),
                         help="Source of outputs")
    add_basic_configuration(sp_java)


def setup_lcg_parser(sp):
    sp_lcg = sp.add_parser("lcg", help="Predict outputs from an arbitrary linear congruential generator",
                           formatter_class=argparse.RawTextHelpFormatter,
                           description=dedent("""
    Determine the next value of a linear congruential generator
    An LCG outputs values with the following recurrence relation:

        state_(n+1) = MULTIPLIER * state_n + INCREMENT (mod MODULUS)
        value_n = state_n >> BITSHIFT"""))

    sp_lcg.add_argument("multiplier", type=int)
    sp_lcg.add_argument("increment", type=int)
    sp_lcg.add_argument("modulus", type=int)
    sp_lcg.add_argument("bitshift", type=int)

    add_basic_configuration(sp_lcg)


def main():
    parser = argparse.ArgumentParser(prog='predict_rng', description="""
    Given outputs from a random number generator (glibc's rand_r, PHP rand, etc),
    predict_rng predicts the future outputs. Alternately, predict_rng can
    be passed the seed, which will be used to produce the same values that
    would be returned from the random number generator.""",
                                     epilog="See additional help for a command with: predict_rng <command> -h")

    parser.add_argument("-m", "--modulo", type=int, nargs=1,
                        help="Output values modulo this number", metavar="MOD")

    sp = parser.add_subparsers(dest="command")
    sp.metavar = 'command'

    # Setup sub parsers
    setup_glibc_parser(sp)
    setup_msvc_parser(sp)
    setup_php_parser(sp)
    setup_java_parser(sp)
    setup_lcg_parser(sp)

    ns = parser.parse_args()

    if vars(ns).get("seed") and vars(ns).get("outputs"):
        parser.error("Outputs are unnecessary when a seed is given")

    if ns.command == "glibc":
        handle_glibc(ns)
    elif ns.command == "msvc":
        handle_msvc(ns)
    elif ns.command == "php":
        handle_php(ns)
    elif ns.command == "java":
        handle_java(ns)
    elif ns.command == "lcg":
        handle_lcg(ns)

if __name__ == "__main__":
    main()
