#!/usr/bin/env python

import argparse
from textwrap import dedent
from predrng import lcg, glibc, php, java, mysql
from predrng.glibc import random, rand_r
from predrng.php import rand
from predrng.java import nextInt, nextLong
from predrng.mysql import rand
from itertools import islice


def print_from_gen(generator, count):
    for v in islice(generator, 0, count):
        print(v, end=" ")
    print()


def handle_msvc(args):
    if args.function in ("rand",):
        if args.seed:
            print_from_gen(lcg.generate_from_seed(args.seed,
                                                  output_modulus=args.modulo),
                           args.count)
        else:
            print_from_gen(lcg.generate_from_outputs(args.outputs,
                                                     output_modulus=args.modulo),
                           args.count)


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


def handle_lcg(args):
    if args.seed:
        print_from_gen(lcg.generate_from_seed(args.seed,
                                              args.multiplier,
                                              args.increment,
                                              args.modulus,
                                              args.bitshift,
                                              args.modulo), args.count)
    else:
        print_from_gen(lcg.generate_from_outputs(args.outputs,
                                                 args.multiplier,
                                                 args.increment,
                                                 args.modulus,
                                                 args.bitshift,
                                                 args.modulo), args.count)


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
            print_from_gen(glibc.rand_r.generate_from_seed(args.seed,
                                                           args.modulo),
                           args.count)
        else:
            print_from_gen(glibc.rand_r.generate_from_outputs(args.outputs,
                                                              args.modulo),
                           args.count)


def handle_php(args):
    if args.function == "rand":
        if args.seed:
            print_from_gen(php.rand.generate_from_seed(args.seed, args.platform,
                                                       args.range), args.count)
        else:
            print_from_gen(php.rand.generate_from_outputs(args.outputs,
                                                          args.platform,
                                                          args.range),
                           args.count)


def handle_mysql(args):
    if args.function == "rand":
        if args.seed:
            print_from_gen(mysql.rand.generate_from_seed(args.seed),
                           args.count)
        else:
            print_from_gen(mysql.rand.generate_from_outputs(args.outputs),
                           args.count)

def add_basic_configuration(parser):
    parser.add_argument("-c", "--count", type=int,
                        help="The number of outputs to predict")

    parser.add_argument("-s", "--seed", type=int,
                        help="The initial seed")
    parser.add_argument("-o", "--outputs", nargs="+", type=int,
                        help="Outputs from this RNG", metavar="output")


def setup_glibc_parser(sp):
    sp_glibc = sp.add_parser("glibc", help="Predict outputs from GNU C Library random functions")
    sp_glibc.add_argument('function', choices=('rand', 'random', 'rand_r'),
                          help="Source of outputs")
    sp_glibc.add_argument("-m", "--modulo", type=int,
                          help="Output values modulo this number", metavar="MOD")
    add_basic_configuration(sp_glibc)


def setup_msvc_parser(sp):
    sp_msvc = sp.add_parser("msvc", help="Predict outputs from Microsoft Visual C++ random functions")
    sp_msvc.add_argument('function', choices=('rand',),
                         help="Source of outputs")
    sp_msvc.add_argument("-m", "--modulo", type=int,
                         help="Output values modulo this number", metavar="MOD")
    add_basic_configuration(sp_msvc)


def setup_php_parser(sp):
    sp_php = sp.add_parser("php", help="Predict outputs from PHP random functions")
    sp_php.add_argument('platform', choices=('linux', 'windows'),
                        help="Platform PHP is running on")
    sp_php.add_argument('function', choices=('rand',),
                        help="Source of outputs")
    sp_php.add_argument('-r', '--range', help="Lower and upper bound (e.g. -r 1 10)"
                        " is equivalent to function(1, 10)",
                        nargs=2, type=int)
    add_basic_configuration(sp_php)


def setup_mysql_parser(sp):
    sp_mysql = sp.add_parser("mysql", help="Predict outputs from MySQL random functions",
                             conflict_handler='resolve')
    sp_mysql.add_argument('function', choices=('rand',),
                          help="Source of outputs")
    add_basic_configuration(sp_mysql)
    sp_mysql.add_argument("-o", "--outputs", nargs="+", type=float,
                          help="Outputs from this RNG", metavar="output")


def setup_java_parser(sp):
    sp_java = sp.add_parser("java", help="Predict outputs from java.util.Random")
    sp_java.add_argument('function', choices=('nextInt', 'nextLong'),
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

    sp_lcg.add_argument("-m", "--modulo", type=int,
                        help="Output values modulo this number", metavar="MOD")

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

    sp = parser.add_subparsers(dest="command", title="Valid Commands")
    sp.required = True
    sp.metavar = 'command'

    # Setup sub parsers
    setup_glibc_parser(sp)
    setup_msvc_parser(sp)
    setup_php_parser(sp)
    setup_java_parser(sp)
    setup_lcg_parser(sp)
    setup_mysql_parser(sp)

    ns = parser.parse_args()

    if not vars(ns).get("seed") and not vars(ns).get("outputs"):
        parser.error("Output or a seed must be provided")
    elif vars(ns).get("seed") and vars(ns).get("outputs"):
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
    elif ns.command == "mysql":
        handle_mysql(ns)

if __name__ == "__main__":
    main()
