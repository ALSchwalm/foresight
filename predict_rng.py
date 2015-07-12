"""
Predict RNG

Usage:
  predict_rng msvc rand <count> <output>...
  predict_rng glibc (rand|random|rand_r) <count> <output>...
  predict_rng lcg <multiplier> <increment> <modulus> <bitshift> <count> <output>...
"""

from docopt import docopt
from predrng import lcg
from itertools import islice

def handle_msvc(args, outputs):
    if args["rand"]:
        for i in islice(lcg.generate_values(outputs), 0, int(args["<count>"])):
            print(i)

def handle_lcg(args, outputs):
    a=int(args["<multiplier>"])
    c=int(args["<increment>"])
    m=int(args["<modulus>"])
    bitshift=int(args["<bitshift>"])
    for i in islice(lcg.generate_values(outputs, a, c, m, bitshift),
                    0, int(args["<count>"])):
        print(i)

def main():
    args = docopt(__doc__)
    outputs = [int(output) for output in args["<output>"]]

    if args["msvc"]:
        handle_msvc(args, outputs)
    elif args["lcg"]:
        handle_lcg(args, outputs)

if __name__ == "__main__":
    main()
