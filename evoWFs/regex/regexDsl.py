import operator
import operator
import math
import random
import string

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import numpy

import copy

from typing import Dict, Tuple
import regex

from typeClasses import *
from function_creators import *
import types

import re
UsefulRegexes = [r'\w+', r"\d+", r"\s+", r".+", r"$"]


def to_regex(a, b):
    m = min(len(a), len(b))
    out = []
    for i in range(m):
        out.append(RegexTuple(a[i], b[i]))
    return out

def cheatLeft(v):
    leftMatches = [[] for i in range(len(v)+1)]
    for r in UsefulRegexes:
        for m in re.findall(r, v):
            leftMatches[v.index(m) + len(m)].append(t2(r))
            #rightMatches[v.index(m)] = r
            #rightMatches[v.index(m)]
    return leftMatches

def cheatRight(v):
    rightMatches = [[] for i in range(len(v)+1)]
    for r in UsefulRegexes:
        for m in re.findall(r, v):
            rightMatches[v.index(m)].append(t2(r))
    return rightMatches

def cheat_total(v,i):
    a = cheatLeft(v)
    b = cheatRight(v)
    out = []
    if i >= 0 and i < len(v):
        if len(a[i]) >0 and len(b[i]) >0:
            for l in a[i]:
                for r in b[i]:
                    out.append(RegexTuple(l,r ))
        return out
    else:
        return [RegexTuple(t2(r''), t2(r''))]

def find_all(v,r):
    return re.findall(r.pattern,v)

#Filte/map maps
def match_left(v,r):
    it = regex.search(r.reg, v)
    if it == None:
        return True 
    else:
        return False 

def create_map(name):
    def map_f(liste, f):
        import pdb
        pdb.set_trace()
        return [f.f(l) for l in liste]
    map_f.__name__ = name
    return map_f

def create_id():
    def id_f(v):
        return v
    return id_f 

def create_select_from_list():
    def sel(liste, index):
        if liste == []:
            return '' 
        if index>=0 and index<len(liste):
            return liste[index]
        else:
            return liste[0]
    return sel

def create_to_list():
    def to(x):
        return [x]
    return to

def createPset(signature):

#    pset = gp.PrimitiveSetTyped("Main", [str, RegexTuple, int], int)
    pset = gp.PrimitiveSetTyped("Main", signature.getWFInput(), signature.getWFOutput())
    print('sig out', signature.getWFOutput())
    print('sig in ', signature.getWFInput())

    pset.renameArguments(**signature.argSet())
#    pset.renameArguments(ARG1='rr')
    #pset.renameArguments(ARG1='k')
#    pset.renameArguments(ARG2='out')

    t0_t0 = TypeConstructorFunction('t0_t0')
    t0_t1 = TypeConstructorFunction('t0_t1')
    t1_t1 = TypeConstructorFunction('t1_t1')
    t2_t1 = TypeConstructorFunction('t1_t1')
    t3_t1 = TypeConstructorFunction('t1_t1')
    pset.context["t0_t0"] = t0_t0 
    pset.context["t0_t1"] = t0_t1 
    pset.context["t1_t1"] = t1_t1 
    pset.context["t2_t1"] = t2_t1 
    pset.context["t3_t1"] = t3_t1 

    t1_listt0 = TypeConstructorFunction('t1_listt0')
    pset.context["t1_listt0"] = t1_listt0
    #t2 = TypeConstructorType('t2')
    #pset.context["t2"] = t2 
    #pset.context["RegexTuple"] = RegexTuple
    #pset.context["RegexTuple"] = RegexTuple
    #pset.context["RegexList"] = RegexList
    pset.context["t2"] = t2 
    pset.context["RegexList"] = RegexList
    pset.context["IntTuple"] =IntTuple 
    pset.context["t1"] = t1 
    pset.context["t0_t0"] = TypeConstructorFunction('t0_t0')
    #pset.context["FunctionTypeII"] =FunctionTypeII# 
    pset.context["ListString"] = ListString# 

    #pset.addTerminal(RegexTuple(t2(r'\s+'), t2(r'\w+')), RegexTuple)
    #pset.addTerminal([RegexTuple(TypeRegex(r''), TypeRegex(r'\w+'))], RegexList)
    #pset.addTerminal([RegexTuple(t2(r''), t2(r'\w+'))], RegexList)
    #pset.addTerminal([t2(r'')], RegexList)
    pset.addTerminal([],IntList)
    #pset.addTerminal([1],IntList)
    #pset.addTerminal([-1],IntList)
    #pset.addTerminal([1,2],IntList)
    pset.addTerminal((0,1),IntTuple)

    pset.addTerminal(t2(r'\w+') , t2)
    #pset.addTerminal(t2(r'') , t2)
    #pset.addTerminal(t2(r'\s+') , t2)
    #pset.addTerminal(t2(r'\d+') , t2)
    #pset.addTerminal(t2(r'^') , t2)
    #pset.addTerminal([t2(r'^')] , RegexListI)
    pset.addTerminal([t2(r) for r in [r'\w+', r"\d+", r"\s+", r".+", r"$"]], RegexList)

    pset.addTerminal(True, t1)
    pset.addTerminal(False, t1)
    
    id_rl = ident_f("id_RegexList")
    id_s = ident_f("id_s")
    id_sl = ident_f("id_sl")
    id_rt = ident_f("id_rt")
    id_r = ident_f("id_r")
    id_i = ident_f("id_i")

    pset.addPrimitive(id_rl, [RegexList], RegexList)
    #pset.addPrimitive(id_rt, [RegexTuple], RegexTuple)
    pset.addPrimitive(id_sl, [ListString], ListString)
    pset.addPrimitive(id_r, [t2], t2)
    pset.addPrimitive(id_s, [str], str)
    pset.addPrimitive(id_i, [int], int)


    ## If ....
    comp_r = compare_f('comp_r')
    comp_b = compare_f('comp_b')
    comp_s = compare_f('comp_s')
    comp_i = compare_f('comp_i')

    fct_comb_r = function_comb('fct_comb_r')
    fct_comb_b = function_comb('fct_comb_b')
    fct_comb_s = function_comb('fct_comb_s')
    fct_comb_i = function_comb('fct_comb_i')

    #pset.addPrimitive(comp_r, [t2,t2], BoolI)
    pset.addPrimitive(comp_r, [t2], t2_t1)
    pset.addPrimitive(comp_b, [t1], t1_t1)
    pset.addPrimitive(comp_i, [int], t0_t1)
    pset.addPrimitive(comp_s, [str], t3_t1)

    pset.addPrimitive(fct_comb_i, [int, t0_t1], t1)
    pset.addPrimitive(fct_comb_b, [t1, t1_t1], t1)
    pset.addPrimitive(fct_comb_s, [str, t3_t1], t1)
    pset.addPrimitive(fct_comb_s, [t2, t2_t1], t1)

    pset.addTerminal(comp_i(0), t0_t1 )
    pset.addTerminal(comp_b(True), t1_t1 )
    pset.addTerminal(comp_s(''), t3_t1 )
    comp_r_p = compare_f('comp_r')
    t = t2(r'\w+')
    a = comp_r_p(t)
    pset.addTerminal(a, t2_t1)

    #t0 = int
    #t1 = bool 
    #t2 = Regex 
    #t3 = str 


    ## Negate
    neg = negate('neg')
    pset.addPrimitive(comp_i, [t1], t1)

    ## Append
    app_r = append_f('app_r')
    app_rt = append_f('app_rt')
    app_s = append_f('app_s')
    app_i = append_f('app_i')
    pset.addPrimitive(app_r, [RegexList, t2], RegexList)
    #pset.addPrimitive(app_rt, [RegexList, RegexTuple], RegexList)
    pset.addPrimitive(app_s, [ListString, str], ListString)
    pset.addPrimitive(app_i, [IntList, int], IntList)

    # Element In
    elem_i = element_in('elem_i')
    #elem_s = element_in('elem_s')
    #elem_r = element_in('elem_r')
    #pset.addPrimitive(elem_i, [IntList, int], t1)
    pset.addPrimitive(elem_i, [IntList, int], t1)


    f_i = filter_f('filter_i')
    f_r = filter_f('filter_r')
    f_s = filter_f('filter_s')
    pset.addPrimitive(f_i, [IntList, t0_t1], IntList )
    pset.addPrimitive(f_r, [RegexList, t2_t1], RegexList)
    pset.addPrimitive(f_s, [ListString, t3_t1], ListString)

    def add_f_2(a, func):
        return func(a)

    add_i = add_f('add_i')

    pset.addPrimitive(add_i, [int], t0_t0)
    pset.addPrimitive(add_f_2, [int, t0_t0], int)
    pset.addTerminal(add_i(0), t0_t0  )
    #pset.addPrimitive(add_f, [int, FunctionType_int_int], int  )
    #add_s = add_s('add_s')
    #pset.addPrimitive(elem_i, [str, FunctionType_str_str], str)

    #map
    map_i = map_f('map_i')
    map_r = map_f('map_r')
    pset.addPrimitive(map_i, [IntList, t0_t0], IntList )
    #pset.addPrimitive(map_r, [IntList, t3_t0], IntList )
    #pset.addPrimitive(map_s, [StringList, t1_listt0], IntList )
    #pset.addPrimitive(map_i, [t2, t0_t0], IntList )
    ### Function TypeI: int -> 

    len_il = len_f('len_il')
    len_s = len_f('len_s')
    len_sl = len_f('len_sl')
    pset.addPrimitive(len_s, [str], int)
    pset.addPrimitive(len_il, [IntList], int)
    pset.addPrimitive(len_sl, [ListString], int)

    ##pset.addPrimitive(cheat_total, [str, int], RegexList)
    #pset.addPrimitive(cheatRight, [str ], RegexList)
    #pset.addPrimitive(cheatLeft, [str ], RegexList)

    index_il = index_f("index_il")
    index_sl = index_f("index_sl")
    #index_rl = index_f("index_rl")
    pset.addPrimitive(index_il, [int, IntList ], int)
    #pset.addPrimitive(index_sl, [str, str], ListString)
    #pset.addPrimitive(index_rl, [str, str], ListString)

    def fck(r):
        def out_fc(v):
            out = []
            for m in re.findall(r.pattern, v):
                out.append(v.index(m))
            return out
        return out_fc

    def fct_typeI(r, func):
        return func(r)

    pset.addPrimitive(fck, [t2], t1_listt0) 
    pset.addPrimitive(fct_typeI, [str, t1_listt0], IntList) 
    pset.addTerminal(fck(t2(r'\w+')), t1_listt0) 

    #def create_tuple(r1, r2):
    #    return RegexTuple(r1,r2)
    #pset.addPrimitive(create_tuple, [t2, t2], RegexTuple) 

    #JK:wpset.addTerminal(FunctionTypeI("match_left"), FunctionTypeI)
    #filer


    #pset.addTerminal(FunctionTypeI(match_right), FunctionTypeI)
    #Kpset.addTerminal(FunctionTypeI("match_left"), FunctionTypeI)
    #pset.addTerminal(FunctionTypeII("match_word"), FunctionTypeII)
    pset.addTerminal(ListString([""]), ListString)
    #pset.addTerminal(FunctionTypeI(43), FunctionTypeI)
    #pset.addTerminal(match_left, type(lambda x: list(map(f, x))))


    def matches(v,rr):
        r = "(?<=" + rr[0].pattern + ")" + rr[1].pattern
        it = regex.finditer(r, v)
        outList = []
        for i in it:
            outList.append(i.start())
        return outList
    ###CHange back
    #pset.addPrimitive(matches, [str, RegexTuple], IntList)

    for a in range(1,2):
        pset.addTerminal(a,int)
        pset.addTerminal(-a,int)
    pset.addTerminal(0,int)
    pset.addTerminal("",str)


    return pset
