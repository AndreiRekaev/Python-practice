# Necessary modules:
import sys
import os.path
import process

# Add our files:
sys.path.append(os.path.abspath(os.pardir))


# The test functions:
def test_input_arguments():
    assert process.make_decision("dsas") == -1
    assert process.make_decision([]) == -1
    assert process.make_decision(2.2) == -1
    assert process.make_decision([]) == -1
    assert process.make_decision(20) != -1


def test_correct():
    assert process.make_decision(20) == 0
    assert process.make_decision(10) == 1
    assert process.make_decision(41) == -1
    assert process.make_decision(-5) == -1