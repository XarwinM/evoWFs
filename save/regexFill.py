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
            leftMatches[v.index(m) + len(m)].append(TypeRegex(r))
            #rightMatches[v.index(m)] = r
            #rightMatches[v.index(m)]
    return leftMatches

def cheatRight(v):
    rightMatches = [[] for i in range(len(v)+1)]
    for r in UsefulRegexes:
        for m in re.findall(r, v):
            rightMatches[v.index(m)].append(TypeRegex(r))
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
        return [RegexTuple(TypeRegex(r''), TypeRegex(r''))]

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

    pset.context["TypeRegex"] =TypeRegex 
    pset.context["RegexTuple"] = RegexTuple
    pset.context["RegexList"] = RegexList
    pset.context["RegexListI"] = RegexList
    pset.context["IntTuple"] =IntTuple 
    pset.context["BoolI"] = BoolI 
    pset.context["FunctionTypeI"] =FunctionTypeI# type(lambda x: list(map(f, x)))
    pset.context["FunctionTypeII"] =FunctionTypeII# type(lambda x: list(map(f, x)))
    pset.context["ListString"] = ListString# type(lambda x: list(map(f, x)))

    pset.addTerminal(RegexTuple(TypeRegex(r'\s+'), TypeRegex(r'\w+')), RegexTuple)
    pset.addTerminal([RegexTuple(TypeRegex(r''), TypeRegex(r'\w+'))], RegexList)
    pset.addTerminal([],IntList)
    pset.addTerminal([1],IntList)
    pset.addTerminal([-1],IntList)
    pset.addTerminal([1,2],IntList)
    pset.addTerminal((0,1),IntTuple)

    pset.addTerminal(TypeRegex(r'\w+') , TypeRegex)
    pset.addTerminal(TypeRegex(r'') , TypeRegex)
    pset.addTerminal(TypeRegex(r'\s+') , TypeRegex)
    pset.addTerminal(TypeRegex(r'\d+') , TypeRegex)
    pset.addTerminal(TypeRegex(r'^') , TypeRegex)
    pset.addTerminal([TypeRegex(r'^')] , RegexListI)
    pset.addTerminal([TypeRegex(r) for r in [r'\w+', r"\d+", r"\s+", r".+", r"$"]], RegexListI)

    pset.addTerminal(True, BoolI)
    pset.addTerminal(False, BoolI)

    #pset.addTerminal(FunctionTypeI(match_right), FunctionTypeI)
    pset.addTerminal(FunctionTypeI("match_left"), FunctionTypeI)
    pset.addTerminal(FunctionTypeII("match_word"), FunctionTypeII)
    pset.addTerminal(ListString([""]), ListString)
    #pset.addTerminal(FunctionTypeI(43), FunctionTypeI)
    #pset.addTerminal(match_left, type(lambda x: list(map(f, x))))

    def idem(v):
        return v
    def idem0(v):
        return v
    pset.addPrimitive(idem, [FunctionTypeI],FunctionTypeI)
    pset.addPrimitive(create_id(), [FunctionTypeII],FunctionTypeII)
    pset.addPrimitive(idem0, [ListString],ListString)

    def idem2(v):
        #return FunctionTypeI(match_right)
        return v
    pset.addPrimitive(idem2, [BoolI],BoolI)

    def idem3(v):
        #return FunctionTypeI(match_right)
        return v
    pset.addPrimitive(idem3, [RegexListI],RegexListI)

    #KJji#def idem4(v,int):
    #    return v
    #pset.addPrimitive(idem3, [RegexListI, int], TypeRegex)

    def matches(v,rr):
        r = "(?<=" + rr[0].pattern + ")" + rr[1].pattern
        it = regex.finditer(r, v)
        outList = []
        for i in it:
            outList.append(i.start())
        return outList
    ###CHange back
    pset.addPrimitive(matches, [str, RegexTuple], IntList)

    def matchesTrue(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return TypeRegex(r'')
        else:
            return r
    ###CHange back
    pset.addPrimitive(matchesTrue, [str, TypeRegex], TypeRegex)

    def toRegexTuple(r1,r2):
        return RegexTuple(r1,r2)
    pset.addPrimitive(toRegexTuple, [TypeRegex, TypeRegex], RegexTuple)

    def select_from_list(l,i):
        if i>=0 and i<len(l):
            return l[i]
        else:
            return RegexTuple(TypeRegex(r''), TypeRegex(r''))

    pset.addPrimitive(select_from_list, [RegexList,int], RegexTuple)

    pset.addPrimitive( create_to_list(), [str], ListString)
    pset.addPrimitive( create_select_from_list(), [ListString, int], str)

    def matchLeft(v,r,b):
        it = regex.search(r.reg, v)
        if it == None:
            return -10 
        else:
            return it.span()[int(b)] 
    ###CHange back
    pset.addPrimitive(matchLeft, [str, TypeRegex, BoolI], int)
    pset.addPrimitive(find_all, [str, TypeRegex], ListString)


    #pset.addPrimitive(to_regex, [RegexListI, RegexListI], RegexList)
    #pset.addPrimitive(cheat_total, [str, int], RegexList)
    
    pset.addPrimitive(cheatLeft, [str], list)
    pset.addPrimitive(cheatRight, [str], list)
    def matchesStr(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return '' 
        else:

            if type(it.group()) != str:
                print('Err')
            return it.group()
    ###CHange back
    pset.addPrimitive(matchesStr, [str, TypeRegex], str)

    def filter_reg(v,b,b2,  listeI, functionI):
        for e, l in enumerate(listeI):
            if not functionI.f(v, l[int(b)]) and b2:
                del listeI[e]
            elif not b2 and functionI.f(v, l[int(b)]):
                del listeI[e]
        return listeI
    pset.addPrimitive(filter_reg, [str, BoolI, BoolI, RegexList,FunctionTypeI], RegexList)

    def to_regex_list(v):
        return [v]
    pset.addPrimitive(to_regex_list, [RegexTuple], RegexList)

    def map_regII(listeI, b, s, functionI):
        out = [functionI.f(s,l[int(b)]) for l in listeI]
        return out
    #pset.addPrimitive(filter_regI, [RegexList,FunctionTypeI], bool)

    map_regII = create_map('new')
    pset.addPrimitive(map_regII, [RegexList,FunctionTypeII], ListString)
    #pset.addPrimitive(map_regII, [RegexList, BoolI, str, FunctionTypeII], ListString)

    def chooseRegList_0(l, i):
        if i >=0 and i < len(l):
            return l[i][0]
        else:
            return TypeRegex(r'')
    pset.addPrimitive(chooseRegList_0, [RegexList, int],TypeRegex )

    def chooseRegList_1(l, i, b):
        if i >=0 and i < len(l):
            return l[i][b]
        else:
            return TypeRegex(r'')
    pset.addPrimitive(chooseRegList_1, [RegexList, int, BoolI],TypeRegex )

    def map_fct(li, fu):
        out = [fu(l) for l in li]
        return out
    #pset.addPrimitive(map_fct, [RegexList, FunctionTypeI],RegexList)

    def indexOf(c, cL):
        #import pdb
        #pdb.set_trace()
        if c in cL:
            return cL.index(c)  
        else:
            return -10 
    pset.addPrimitive(indexOf, [int, IntList], int)

    def strId(dic):
        return dic
    pset.addPrimitive(strId, [str], str)

    def regId(r):
        return r
    pset.addPrimitive(regId, [TypeRegex], TypeRegex)

    def regTupId(r):
        return r
    pset.addPrimitive(regTupId, [RegexTuple], RegexTuple)

    def regTupList(r):
        return [r]
    pset.addPrimitive(regTupList, [RegexTuple], RegexList)

    def regexToTuple(r1, r2):
        return RegexTuple(r1, r2)
    pset.addPrimitive(regexToTuple, [TypeRegex, TypeRegex], RegexTuple)

    def subString(x, s1, s2):
        return x[s1:s2]
    pset.addPrimitive(subString, [str, int, int], str)

    def occurPosition(s1,s2):
        if s2 in s1:
            return s1.index(s2) 
        else:
            return 0 
    pset.addPrimitive(occurPosition, [str,str], int)

    def lenStr(s):
        return len(s)
    pset.addPrimitive(lenStr, [str], int)

    def addInt(x,t):
        return x+t
    pset.addPrimitive(addInt, [int, int], int)

    def subInt(x,t):
        return x-t
    pset.addPrimitive(subInt, [int, int], int)

    def intToList(x):
        return [x]
    pset.addPrimitive(intToList, [int], IntList)

    def listToInt(x):
        if len(x)==1:
            return x[0]
        else:
            return -1
    pset.addPrimitive(listToInt, [IntList], int)

    def intToTuple(i1, i2):
        return (i1, i2) 
    pset.addPrimitive(intToTuple, [int, int], IntTuple)

    def strToList(x):
        return [x]
    #pset.addPrimitive(strToList, [str], list)

    def concat(x,y):
        return x+y 
    #pset.addPrimitive(concat, [list , list], list)
    pset.addPrimitive(concat, [RegexList , RegexList], RegexList)
    def concat2(x,y):
        return x+y 
    pset.addPrimitive(concat2, [ListString, ListString], ListString)

    def concat3(x,y):
        return x+y 
    pset.addPrimitive(concat3, [IntList,IntList], IntList)

    def append(x,y):
        neu = x
        neu.append(y)
        return neu
    def append2(x,y):
        neu = x
        neu.append(y)
        return neu
    def append3(x,y):
        neu = x
        neu.append(y)
        return neu
    pset.addPrimitive(append, [ListString,str], ListString)
    pset.addPrimitive(append2, [RegexList,RegexTuple], RegexList)
    pset.addPrimitive(append3, [IntList,int], IntList)

    for a in range(1,2):
        pset.addTerminal(a,int)
        pset.addTerminal(-a,int)
    pset.addTerminal(0,int)



    #for a in string.ascii_letters:
    #    pset.addTerminal(a,str)
    #pset.addTerminal(' ', str)

    return pset
