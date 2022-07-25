"""
Functions that define the DSL on which we use an evolutionary algorithm
to learn the witnesss function.
The DSL is designed to learn witness functions for operators that work on math data.
See also following https://deap.readthedocs.io/
"""
# import math
# import random
# import string
# import operator

# from deap import algorithms
# from deap import base
# from deap import creator
# from deap import tools
from deap import gp

# import numpy

# import copy

# from typing import Dict, Tuple
# import regex

from evoWFs.type_classes import IntList, TypeConstructorFunction, t1

# from evoWFs.function_creators import *
# import types

# import re

UsefulRegexes = [r"\w+", r"\d+", r"\s+", r".+", r"$"]


def create_pset(signature):
    """Returns a primitive set for strongly typed genetic programming
    (see alsohttps://deap.readthedocs.io/en/master/examples/gp_spambase.html)
    The primitive set characterizes the DSL on which we learn
    the witness function.
    The argument signature describes the witness function (output type etc.)
    """

    #    pset = gp.PrimitiveSetTyped("Main", [str, RegexTuple, int], int)
    pset = gp.PrimitiveSetTyped(
        "Main", signature.get_wf_input(), signature.get_wf_output()
    )
    print("sig out", signature.get_wf_output())
    print("sig in ", signature.get_wf_input())

    pset.renameArguments(**signature.arg_set())

    t0_t0 = TypeConstructorFunction("t0_t0")
    # t0_t1 = TypeConstructorFunction('t0_t1')
    # t1_t1 = TypeConstructorFunction('t1_t1')
    # pset.context["t0_t1"] = t0_t1
    # pset.context["t1_t1"] = t1_t1

    pset.context["IntList"] = IntList  #
    pset.context["int"] = int  #
    pset.context["t0_t0"] = t0_t0

    pset.addTerminal([], IntList)
    pset.addTerminal([0], IntList)

    # pset.addTerminal(True, t0)
    # pset.addTerminal(False, t0)

    def id_int(a1):
        """
        Identity mapping for integers
        """
        return a1

    pset.addPrimitive(id_int, [int], int)

    '''
    def id_t0_t0(a2):
        """
        Identity mapping for int->int (functions that map int to int)
        """
        return a
    '''

    pset.addPrimitive(id_int, [t0_t0], t0_t0)

    def negate(a2):
        """
        Negate input integer
        """
        return -a2

    pset.addPrimitive(negate, [int], int)

    def int_to_list(a4):
        """Takes input integer and wraps it in a list
        Argument:
            a4: integer
        Return
            list of one integer
        """
        return [a4]

    pset.addPrimitive(int_to_list, [int], IntList)

    def execute(f1, b1):
        return f1(b1)

    pset.addPrimitive(execute, [t0_t0, int], int)

    def addition(a5):
        def add_f(b2):
            return b2 + a5

        return add_f

    pset.addPrimitive(addition, [int], t0_t0)

    def int_map(f2, l1):
        """Represents map operator
        Arguments:
            f2: Function that maps int to int
            l1: list of ints
        Return:
            List of ints
        """
        return [f2(i) for i in l1]

    pset.addPrimitive(int_map, [t0_t0, IntList], IntList)

    def add_to_list(l2, a6):
        """
        Extends list
        """
        return l2 + [a6]

    pset.addPrimitive(add_to_list, [IntList, int], IntList)

    def h(b1):
        return b1

    pset.addTerminal(h, t0_t0)

    for a7 in range(1, 10):
        pset.addTerminal(a7, int)
        pset.addTerminal(-a7, int)
    pset.addTerminal(0, int)

    return pset