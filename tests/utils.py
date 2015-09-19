from collections import namedtuple
from nose.tools import nottest

TestCase = namedtuple('TestCase', ['seed', 'outputs'])


@nottest
def read_test_data(filename, as_type=int):
    def parse_line(line):
        seed, outputs = line.split(":")
        outputs = [as_type(output) for output in outputs.split()]
        return TestCase(int(seed), outputs)

    with open("tests/" + filename) as data_file:
        data = [line for line in data_file.readlines()
                if line.strip() and not line.startswith("#")]
        data = [parse_line(line) for line in data]
        return data
