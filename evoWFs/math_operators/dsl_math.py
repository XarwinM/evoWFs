"""
Operators of the mathematical domain.
For each of these operators we aim to learn a witness function
"""


def addition(a, b):
    """Simple addition function"""
    return a + b


# OPERATOR_PARAMETER_DIC = {AbsPos: ['v', 'k'], Substring:['v', 'start', 'end'], RelPos:['v', 'rr']}
OPERATOR_PARAMETER_DIC = {addition: ["a", "b"]}
