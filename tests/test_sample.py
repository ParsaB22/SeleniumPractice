import pytest

def func(x):
    return x + 1

@pytest.mark.skip(reason="demonstrating skipping")
def test_answer():
    assert func(2) == 3
    assert func(5) == 6
    assert func(3) != 5

# fixures happen before each test as a setup function
# yeild is like return but it pauses the function and resumes after the test
# everything before the yeild is setup, everything after is teardown
# for a test to use  fixure it must be passed as a parameter to the test function
# @pytest.fixture
# def setup_teardown():
#     # setup code
#     c = ClassName();
#     print("Setting up before test")
#     yield c
#     # teardown code
#     c.cleanup();

# pytest.mark.parametrize allows running the same test with different parameters|| it just supplies a set of test cases to plug into a dynamic test function
# @pytest.mark.parametrize("num,expected", [
#     (2, True), 
#     (3, False), 
#     (4, True)
#     ])
# def test_is_even(num, expected):
#     assert (num % 2 == 0) == expected
