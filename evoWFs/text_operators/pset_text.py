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

    pset = gp.PrimitiveSetTyped(
        "Main", signature.get_wf_input(), signature.get_wf_output()
    )
    print("sig out", signature.get_wf_output())
    print("sig in ", signature.get_wf_input())

    pset.renameArguments(**signature.arg_set())

    t0_t0 = TypeConstructorFunction("t0_t0")
    t0_TypeI = TypeConstructorFunction("t0_TypeI")
    TypeI_TypeI = TypeConstructorFunction("TypeI_TypeI")
    t3_TypeI = TypeConstructorFunction("t3_TypeI")
    t3_t3 = TypeConstructorFunction("t3_t3")

    t0_t3 = TypeConstructorFunction("t0_t3")

    pset.context["t0_t0"] = t0_t0
    pset.context["t0_TypeI"] = t0_TypeI
    pset.context["TypeI_TypeI"] = TypeI_TypeI
    pset.context["t3_TypeI"] = t3_TypeI
    pset.context["t3_t3"] = t3_t3
    pset.context["t0_t3"] = t0_t3

    TypeI_listt0 = TypeConstructorFunction("TypeI_listt0")
    pset.context["TypeI_listt0"] = TypeI_listt0
    # pset.context["IntTuple"] =IntTuple
    pset.context["TypeI"] = TypeI
    pset.context["t3"] = str
    pset.context["t0_t0"] = TypeConstructorFunction("t0_t0")
    pset.context["ListString"] = ListString  #

    pset.addTerminal([], IntList)
    # pset.addTerminal((0,1),IntTuple)

    pset.addTerminal(True, TypeI)
    pset.addTerminal(False, TypeI)

    id_s = ident_f("id_s")
    id_sl = ident_f("id_sl")
    # id_rt = ident_f("id_rt")
    id_r = ident_f("id_r")
    id_i = ident_f("id_i")
    id_t0_t3 = ident_f("id_t0_t3")

    pset.addPrimitive(id_sl, [ListString], ListString)
    pset.addPrimitive(id_r, [TypeII], TypeII)
    pset.addPrimitive(id_s, [str], str)
    pset.addPrimitive(id_i, [int], int)
    pset.addPrimitive(id_t0_t3, [t0_t3], t0_t3)

    def create_range(i, j):
        if i <= 0 or i >= j:
            return []
        elif i > 0 and j > i:
            return list(range(i, j))
        return []

    pset.addPrimitive(create_range, [int, int], IntList)

    #'''
    def subset_sel(i, j):
        def new_subset(v):
            if i >= 0 and j > i and len(v) >= j:
                return v[i:j]
            else:
                return ""

        return new_subset

    pset.addPrimitive(subset_sel, [int, int], t3_t3)
    #'''
    def subset_sel_1(v, i):
        def new_subset(j):
            if len(v) >= j and j > 0 and j >= i and i >= 0:
                return v[i:j]
            else:
                return ""

        return new_subset

    def t0_t3_t(x):
        return ""

    pset.addTerminal(t0_t3_t, t0_t3)
    pset.addPrimitive(subset_sel_1, [str, int], t0_t3)

    ## If ....
    comp_b = compare_f("comp_b")
    comp_s = compare_f("comp_s")
    comp_i = compare_f("comp_i")

    fct_comb_b = function_comb("fct_comb_b")
    fct_comb_s = function_comb("fct_comb_s")
    fct_comb_i = function_comb("fct_comb_i")

    # pset.addPrimitive(comp_r, [TypeII,TypeII], BoolI)
    pset.addPrimitive(comp_b, [TypeI], TypeI_TypeI)
    pset.addPrimitive(comp_i, [int], t0_TypeI)
    pset.addPrimitive(comp_s, [str], t3_TypeI)

    pset.addPrimitive(fct_comb_i, [int, t0_TypeI], TypeI)
    pset.addPrimitive(fct_comb_b, [TypeI, TypeI_TypeI], TypeI)
    pset.addPrimitive(fct_comb_s, [str, t3_TypeI], TypeI)

    pset.addTerminal(comp_i(0), t0_TypeI)
    pset.addTerminal(comp_b(True), TypeI_TypeI)
    pset.addTerminal(comp_s(""), t3_TypeI)

    ## Negate
    # neg = negate("neg")

    def neg_int(number):
        return -number

    pset.addPrimitive(neg_int, [int], int)
    pset.addPrimitive(comp_i, [TypeI], TypeI)

    ## Append
    # app_r = append_f("app_r")
    # app_rt = append_f("app_rt")
    app_s = append_f("app_s")
    app_i = append_f("app_i")
    # pset.addPrimitive(app_rt, [RegexList, RegexTuple], RegexList)
    pset.addPrimitive(app_s, [ListString, str], ListString)
    pset.addPrimitive(app_i, [IntList, int], IntList)

    # Element In
    elem_i = element_in("elem_i")
    # elem_s = element_in('elem_s')
    # elem_r = element_in('elem_r')
    # pset.addPrimitive(elem_i, [IntList, int], TypeI)
    pset.addPrimitive(elem_i, [IntList, int], TypeI)

    f_i = filter_f("filter_i")
    # f_r = filter_f("filter_r")
    f_s = filter_f("filter_s")
    pset.addPrimitive(f_i, [IntList, t0_TypeI], IntList)
    pset.addPrimitive(f_s, [ListString, t3_TypeI], ListString)

    def add_f_2(a, func):
        return func(a)

    add_i = add_f("add_i")

    pset.addPrimitive(add_i, [int], t0_t0)
    pset.addPrimitive(add_f_2, [int, t0_t0], int)
    pset.addTerminal(add_i(0), t0_t0)
    # pset.addPrimitive(add_f, [int, FunctionType_int_int], int  )
    # add_s = add_s('add_s')
    # pset.addPrimitive(elem_i, [str, FunctionType_str_str], str)

    # map
    map_i = map_f("map_i")
    map_s = map_f("map_s")
    map_s_i = map_f("map_s_i")
    pset.addPrimitive(map_i, [IntList, t0_t0], IntList)
    pset.addPrimitive(map_s, [ListString, t3_t3], ListString)
    pset.addPrimitive(map_s_i, [IntList, t0_t3], ListString)

    def map_add_terminal(terminal):
        return terminal

    pset.addTerminal(map_add_terminal, t3_t3)

    len_il = len_f("len_il")
    len_s = len_f("len_s")
    len_sl = len_f("len_sl")
    pset.addPrimitive(len_s, [str], int)
    pset.addPrimitive(len_il, [IntList], int)
    pset.addPrimitive(len_sl, [ListString], int)

    index_il = index_f("index_il")
    index_sl = index_f("index_sl")
    pset.addPrimitive(index_il, [int, IntList], int)
    pset.addPrimitive(index_sl, [str, str], int)

    for a in range(1, 2):
        pset.addTerminal(a, int)
        pset.addTerminal(-a, int)
    pset.addTerminal(0, int)
    pset.addTerminal("", str)
    pset.addTerminal([], ListString)

    return pset
