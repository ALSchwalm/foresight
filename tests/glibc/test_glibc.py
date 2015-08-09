from predrng.glibc import rand_r, random
from tests.utils import read_test_data


def test_rand_r():
    testcases = read_test_data("glibc/rand_r.data")

    for i, testcase in enumerate(testcases):
        gen = rand_r.generate_from_outputs(testcase.outputs[:1])
        for output in testcase.outputs[1:]:
            assert(next(gen) == output)

        gen = rand_r.generate_from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)
