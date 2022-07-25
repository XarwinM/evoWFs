"""
Operators of the text domain. These operators are from the Substring DSL.
For each of these operators we aim to learn a witness function
"""


def const_str(str_input):
    """Returns string as it is"""
    return str_input


def substring(str_input, start, end):
    """Returns a substring of input string str_input"""
    return str_input[start:end]


def concat(str_input_1, str_input_2):
    """Returns concatenation of two input strings"""
    return str_input_1 + str_input_2


def abs_pos(str_input, k):
    """Implements AbsPos operator as described in thesis"""
    if k < 0:
        return len(str_input) + k + 1
    return k - 1


# Dictionary that describes parameters and their names
# of the text operators
OPERATOR_PARAMETER_DIC = {
    abs_pos: ["str_input", "k"],
    substring: ["str_input", "start", "end"],
    const_str: ["str_input"],
    concat: ["str_input_1", "str_input_2"],
}
