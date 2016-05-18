
Foresight
=========

`foresight` is a python library for predicting the output of random number
generators across a variety of platforms and languages including:

- glibc
- MSVC
- PHP
- Java
- MySQL

This repository also contains a simple wrapper (called `foresee`) around this
library that provides a CLI.

Installation
============

To install `foresight`, clone this repository and run `python setup.py install`.

Library Usage
=============

The library is divided into subpackages for each supported platform. These
subpackages then provide submodules for each supported function. For example,the
following sample will predict the output of the glibc `rand_r` from some
prior outputs:

    from foresight.glibc import rand_r

    prior_outputs = [int(i) for i in input().split()]
    future_outputs = rand_r.from_outputs(prior_outputs)

    for output in future_outputs:
        print(output)

Generally, each module provides the following functions:

- `from_seed(seed)`: get a generator to the future values returned by the RNG when
seeded with the given value.

- `from_outputs(prev_values)`: attempt to predict the internal state of the RNG from
the given prior outputs. If successful, returns a generator to the future values
returned by the RNG.

CLI Usage
=========

Command line usage of the library has the following general form:

    foresee <platform> <function> [<options>]

For example, the above script is equivalent to the following `foresee` command:

    foresee glibc rand_r -o <the prior outputs>

By default, an infinite stream is generated. The output may be limited to the next
`N` outputs with `-c N`.

Tests
=====

Tests can be run with `nose` by first installing the package with `pip install nose`,
and then running `nosetest` in the project root.

License
=======

This project is licensed under the terms of the MIT license. See the LICENSE file
for details

Contributing
============

Keeping in mind that this project is still fairly unstable, contributions are
welcome.
