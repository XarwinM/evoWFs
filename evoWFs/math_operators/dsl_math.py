"""
Operators of the mathematical domain.
For each of these operators we aim to learn a witness function
"""


def addition(summand_1, summand_2):
    """Simple addition function"""
    return summand_1 + summand_2


# Parameters that describe addition-operator.
OPERATOR_PARAMETER_DIC = {addition: ["summand_1", "summand_2"]}
