"""
Functions that define the DSL on which we use an evolutionary algorithm
to learn the witnesss function.
The DSL is designed to learn witness functions for operators that work on text data.
See also following https://deap.readthedocs.io/
"""
from deap import gp

from evoWFs.type_classes import IntList, TypeConstructorFunction, ListString, TypeI, TypeII
from evoWFs.function_creators import (
    filter_f,
    compare_f,
    function_comb,
    append_f,
    element_in,
    len_f,
    index_f,
    add_f,
    map_f,
    ident_f,
)

def create_pset(signature):
    """
    Returns a primitive set for strongly typed genetic programming
    (see alsohttps://deap.readthedocs.io/en/master/examples/gp_spambase.html)
    The primitive set characterizes the DSL on which we learn
    the witness function.
    The argument signature describes the witness function (output type etc.)
    Here we define a DSL to learn witness function for text operators
    """

    pset = gp.PrimitiveSetTyped(
        "Main", signature.get_wf_input(), signature.get_wf_output()
    )

    # Use own parameter naming for learning problem
    pset.renameArguments(**signature.arg_set())

    # Create function type that maps from one type to the same
    t0_t0 = TypeConstructorFunction("t0_t0")

    # Create function type that maps from one type t0 to TypeI
    t0_TypeI = TypeConstructorFunction("t0_TypeI")

    # Create function type that maps from one TypeI to TypeI
    TypeI_TypeI = TypeConstructorFunction("TypeI_TypeI")

    # Create function type that maps from one type t3 to TypeI
    t3_TypeI = TypeConstructorFunction("t3_TypeI")

    # Create function type that maps from one type t3 to t3
    t3_t3 = TypeConstructorFunction("t3_t3")

    # Create function type that maps from one type t0 to t3
    t0_t3 = TypeConstructorFunction("t0_t3")

    TypeI_listt0 = TypeConstructorFunction("TypeI_listt0")

    # Register Types
    pset.context["t0_t0"] = t0_t0
    pset.context["t0_TypeI"] = t0_TypeI
    pset.context["TypeI_TypeI"] = TypeI_TypeI
    pset.context["t3_TypeI"] = t3_TypeI
    pset.context["t3_t3"] = t3_t3
    pset.context["t0_t3"] = t0_t3

    pset.context["TypeI_listt0"] = TypeI_listt0
    pset.context["TypeI"] = TypeI

    # t3 ist defined to be a string
    pset.context["t3"] = str
    pset.context["t0_t0"] = TypeConstructorFunction("t0_t0")
    pset.context["ListString"] = ListString  #


    pset.addTerminal([], IntList)
    # TypeI is defined to be a bool
    pset.addTerminal(True, TypeI)
    pset.addTerminal(False, TypeI)

    id_s = ident_f("id_s")
    id_sl = ident_f("id_sl")
    id_r = ident_f("id_r")
    id_i = ident_f("id_i")
    id_t0_t3 = ident_f("id_t0_t3")

    # Add identity functions
    pset.addPrimitive(id_sl, [ListString], ListString)
    pset.addPrimitive(id_r, [TypeII], TypeII)
    pset.addPrimitive(id_s, [str], str)
    pset.addPrimitive(id_i, [int], int)
    pset.addPrimitive(id_t0_t3, [t0_t3], t0_t3)

    pset.addPrimitive(create_range, [int, int], IntList)

    pset.addPrimitive(subset_sel, [int, int], t3_t3)

    pset.addPrimitive(subset_sel_1, [str, int], t0_t3)

    pset.addTerminal(t0_t3_t, t0_t3)

    # Compare functions
    comp_b = compare_f("comp_b")
    comp_s = compare_f("comp_s")
    comp_i = compare_f("comp_i")

    pset.addPrimitive(comp_b, [TypeI], TypeI_TypeI)
    pset.addPrimitive(comp_i, [int], t0_TypeI)
    pset.addPrimitive(comp_s, [str], t3_TypeI)

    fct_comb_b = function_comb("fct_comb_b")
    fct_comb_s = function_comb("fct_comb_s")
    fct_comb_i = function_comb("fct_comb_i")

    pset.addPrimitive(fct_comb_i, [int, t0_TypeI], TypeI)
    pset.addPrimitive(fct_comb_b, [TypeI, TypeI_TypeI], TypeI)
    pset.addPrimitive(fct_comb_s, [str, t3_TypeI], TypeI)

    pset.addTerminal(comp_i(0), t0_TypeI)
    pset.addTerminal(comp_b(True), TypeI_TypeI)
    pset.addTerminal(comp_s(""), t3_TypeI)

    pset.addPrimitive(neg_int, [int], int)
    pset.addPrimitive(comp_i, [TypeI], TypeI)

    # Append Functions
    app_s = append_f("app_s")
    app_i = append_f("app_i")
    pset.addPrimitive(app_s, [ListString, str], ListString)
    pset.addPrimitive(app_i, [IntList, int], IntList)

    # Element in function
    elem_i = element_in("elem_i")
    pset.addPrimitive(elem_i, [IntList, int], TypeI)

    # Filter operations
    f_i = filter_f("filter_i")
    f_s = filter_f("filter_s")
    pset.addPrimitive(f_i, [IntList, t0_TypeI], IntList)
    pset.addPrimitive(f_s, [ListString, t3_TypeI], ListString)

    add_i = add_f("add_i")

    pset.addPrimitive(add_i, [int], t0_t0)
    pset.addPrimitive(add_f_2, [int, t0_t0], int)
    pset.addTerminal(add_i(0), t0_t0)

    # Map operators
    map_i = map_f("map_i")
    map_s = map_f("map_s")
    map_s_i = map_f("map_s_i")
    pset.addPrimitive(map_i, [IntList, t0_t0], IntList)
    pset.addPrimitive(map_s, [ListString, t3_t3], ListString)
    pset.addPrimitive(map_s_i, [IntList, t0_t3], ListString)

    pset.addTerminal(map_add_terminal, t3_t3)

    # Length function ons differen types
    len_il = len_f("len_il")
    len_s = len_f("len_s")
    len_sl = len_f("len_sl")
    pset.addPrimitive(len_s, [str], int)
    pset.addPrimitive(len_il, [IntList], int)
    pset.addPrimitive(len_sl, [ListString], int)

    # Index of function on different types
    index_il = index_f("index_il")
    index_sl = index_f("index_sl")
    pset.addPrimitive(index_il, [int, IntList], int)
    pset.addPrimitive(index_sl, [str, str], int)

    # Add Terminals
    for i in range(1, 2):
        pset.addTerminal(i, int)
        pset.addTerminal(-i, int)
    pset.addTerminal(0, int)
    pset.addTerminal("", str)
    pset.addTerminal([], ListString)

    return pset

# Functions for the DSL above

def create_range(i, j):
    """ Create a list integer from i to j"""
    if i <= 0 or i >= j:
        return []
    elif i > 0 and j > i:
        return list(range(i, j))
    return []

def map_add_terminal(map_terminal):
    """Returns map function as it is"""
    return map_terminal

def add_f_2(element, func):
    """Executes func on element"""
    return func(element)

def subset_sel_1(v, i):
    """
    Returns a function that selects a substring, based on an end value
    """
    def new_subset(end):
        if len(v) >= end and end > 0 and end >= i and i >= 0:
            return v[i:end]
        return ""

    return new_subset

def subset_sel(i, j):
    """Returns a function that selects a sub-string from element i to j"""
    def new_subset(input_string):
        if i >= 0 and j > i and len(input_string) >= j:
            return input_string[i:j]
        else:
            return ""
    return new_subset

def t0_t3_t(x):
    """Return empty string"""
    return ""

def neg_int(number):
    """Negates integer"""
    return -number
