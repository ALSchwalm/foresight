from foresight.msvc import rand
from tests.utils import read_test_data


def test_rand():
    testcases = read_test_data("msvc/rand.data")

    for i, testcase in enumerate(testcases):
        gen = rand.from_outputs(testcase.outputs[:4])
        for output in testcase.outputs[4:]:
            assert(next(gen) == output)

        gen = rand.from_seed(testcase.seed)
        for output in testcase.outputs:
            assert(next(gen) == output)
