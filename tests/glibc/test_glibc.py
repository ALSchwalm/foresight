from foresight.glibc import rand_r, random
from tests.utils import read_test_data


def test_rand_r():
    testcases = read_test_data("glibc/rand_r.data")

    for i, testcase in enumerate(testcases):
        gen = rand_r.from_outputs(testcase.outputs[:1])
        for output in testcase.outputs[1:]:
            assert(next(gen) == output)

        gen = rand_r.from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)


def test_random():
    testcases = read_test_data("glibc/random.data")

    #TODO: add test for from_output, once growing error problem is resolved
    for testcase in testcases:
        gen = random.from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)
