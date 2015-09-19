from foresight.mysql import rand
from tests.utils import read_test_data


def test_rand_r():
    testcases = read_test_data("mysql/rand.data", as_type=float)

    for i, testcase in enumerate(testcases):
        gen = rand.from_outputs(testcase.outputs[:2])
        for output in testcase.outputs[2:]:
            assert(next(gen) == output)

        gen = rand.from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)
