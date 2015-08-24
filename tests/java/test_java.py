from foresight.java import nextInt, nextLong
from tests.utils import read_test_data


def test_nextInt():
    testcases = read_test_data("java/nextInt.data")

    for testcase in testcases:
        gen = nextInt.from_outputs(testcase.outputs[:5])
        for output in testcase.outputs[5:]:
            assert(next(gen) == output)

        gen = nextInt.from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)


def test_nextLong():
    testcases = read_test_data("java/nextLong.data")

    for testcase in testcases:
        gen = nextLong.from_outputs(testcase.outputs[:1])
        for output in testcase.outputs[1:]:
            assert(next(gen) == output)

        gen = nextLong.from_seed(testcase.seed)
        for i, output in enumerate(testcase.outputs):
            assert(next(gen) == output)
