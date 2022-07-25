"""
Functions that define the DSL on which we use an evolutionary algorithm
to learn the witness function.
The DSL is designed to learn witness functions for operators that work on math data.
See also following https://deap.readthedocs.io/
"""
from deap import gp

from evoWFs.type_classes import IntList, TypeConstructorFunction


def create_pset(signature):
    """
    Returns a primitive set for strongly typed genetic programming
    (see alsohttps://deap.readthedocs.io/en/master/examples/gp_spambase.html)
    The primitive set characterizes the DSL on which we learn
    the witness function.
    The argument signature describes the witness function (output type etc.)
    Here we define a DSL in order to learn a witness function for math operations
    """

    pset = gp.PrimitiveSetTyped(
        "Main", signature.get_wf_input(), signature.get_wf_output()
    )

    # Use own parameter naming for learning problem
    pset.renameArguments(**signature.arg_set())

    # Create function type that maps from one type to the same
    t0_t0 = TypeConstructorFunction("t0_t0")

    # Define types for learning problem
    pset.context["IntList"] = IntList
    pset.context["int"] = int
    pset.context["t0_t0"] = t0_t0

    pset.addTerminal([], IntList)
    pset.addTerminal([0], IntList)


    def id_int(input_int):
        """
        Identity mapping for integers
        """
        return input_int
    pset.addPrimitive(id_int, [int], int)
    pset.addPrimitive(id_int, [t0_t0], t0_t0)

    def negate(input_int_neg):
        """
        Negate input integer
        """
        return - input_int_neg
    pset.addPrimitive(negate, [int], int)

    def int_to_list(input_int_to_list):
        """Takes input integer and wraps it in a list
        Argument:
            input_int_to_list: integer
        Return
            list of one integer
        """
        return [input_int_to_list]
    pset.addPrimitive(int_to_list, [int], IntList)

    def execute(func_1, element_1):
        """Execute function func_1 on element_1"""
        return func_1(element_1)
    pset.addPrimitive(execute, [t0_t0, int], int)

    def addition(summand_1):
        """Returns function that ads input to summand_1"""
        def add_f(summand_2):
            """Return sum"""
            return summand_1 + summand_2
        return add_f
    pset.addPrimitive(addition, [int], t0_t0)

    def int_map(func, list_ints):
        """Represents map operator
        Arguments:
            func: Function that maps int to int
            list_ints: list of ints
        Return:
            List of ints
        """
        return [func(i) for i in list_ints]
    pset.addPrimitive(int_map, [t0_t0, IntList], IntList)

    def add_to_list(list_ints, element):
        """
        Extends list
        """
        return list_ints + [element]
    pset.addPrimitive(add_to_list, [IntList, int], IntList)

    def id_t0_t0(func_element):
        """
        Identity function that maps function to same function
        """
        return func_element
    pset.addTerminal(id_t0_t0, t0_t0)

    # Add constant integers to pset
    for i in range(1, 10):
        pset.addTerminal(i, int)
        pset.addTerminal(-i, int)
    pset.addTerminal(0, int)

    return pset
