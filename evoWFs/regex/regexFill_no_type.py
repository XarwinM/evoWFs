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
    if type(v) == str and type(i) == int:
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
    else:
        return None


#Filte/map maps
def match_left(v,r):
    it = regex.search(r.reg, v)
    if it == None:
        return True 
    else:
        return False 

def create_map(name):
    def map(liste, f):
        return [f.f(l) for l in liste]
    return map

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
    #pset = gp.PrimitiveSetTyped("Main", signature.getWFInput(), signature.getWFOutput())
    pset = gp.PrimitiveSet("Main", 2)
    print('sig out', signature.getWFOutput())
    print('sig in ', signature.getWFInput())

    pset.renameArguments(**signature.argSet())
    '''

    pset.context["TypeRegex"] =TypeRegex 
    pset.context["RegexTuple"] = RegexTuple
    pset.context["RegexList"] = RegexList
    pset.context["RegexListI"] = RegexList
    pset.context["IntTuple"] =IntTuple 
    pset.context["BoolI"] = BoolI 
    pset.context["FunctionTypeI"] =FunctionTypeI# type(lambda x: list(map(f, x)))
    pset.context["FunctionTypeII"] =FunctionTypeII# type(lambda x: list(map(f, x)))
    pset.context["ListString"] = ListString# type(lambda x: list(map(f, x)))
    '''

    ab = [TypeRegex(r) for r in [r'\w+', r"\d+", r"\s+", r".+", r"$"]]
    pset.addTerminal(ab)

    pset.addTerminal( [RegexTuple(TypeRegex(r''), TypeRegex(r'\w+'))], name='x1')
    #pset.addTerminal(True )
    #pset.addTerminal(False)

    #pset.addTerminal(FunctionTypeI("match_left") )
    #pset.addTerminal(FunctionTypeII("match_word") )
    #pset.addTerminal(ListString([""]))

    def idem(v):
        return v
    pset.addPrimitive(idem, 1)

    def create_list(li):
        if li == None:
            return None
        return [li]
    pset.addPrimitive(create_list, 1)

    def matches(v,rr):
        try:
            if type(rr[0]) == TypeRegex and len(rr) == 2 and type(v) == str: 
                r = "(?<=" + rr[0].pattern + ")" + rr[1].pattern
                it = regex.finditer(r, v)
                outList = []
                for i in it:
                    outList.append(i.start())
                return outList
            else:
                return None
        except:
            return None
    ###CHange back
    pset.addPrimitive(matches,2)

    def find_all(v,r):
        if type(v) == str and type(r) == TypeRegex:
            return re.findall(r.pattern,v)
        else:
            return None
    pset.addPrimitive(find_all,2)

    def matchesTrue(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return TypeRegex(r'')
        else:
            return r

    def map_f(li, f):
        if type(f) == type(find_all) and type(li) == list: 
            return [f(l) for l in li]
        else:
            return None
    pset.addPrimitive(map_f, 2)
    ###CHange back

    #pset.addPrimitive( create_to_list(), [str], ListString)
    #pset.addPrimitive( create_select_from_list(), [ListString, int], str)

    def matchLeft(v,r,b):
        it = regex.search(r.reg, v)
        if it == None:
            return -10 
        else:
            return it.span()[int(b)] 
    ###CHange back
    #pset.addPrimitive(matchLeft, [str, TypeRegex, BoolI], int)
    #pset.addPrimitive(find_all, [str, TypeRegex], ListString)


    #pset.addPrimitive(to_regex, [RegexListI, RegexListI], RegexList)
    #pset.addPrimitive(cheat_total,2)
    
    #pset.addPrimitive(cheatLeft, [str], list)
    #pset.addPrimitive(cheatRight, [str], list)
    def matchesStr(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return '' 
        else:

            if type(it.group()) != str:
                print('Err')
            return it.group()
    ###CHange back
    #pset.addPrimitive(matchesStr, [str, TypeRegex], str)

    def filter_reg(v,b,b2,  listeI, functionI):
        for e, l in enumerate(listeI):
            if not functionI.f(v, l[int(b)]) and b2:
                del listeI[e]
            elif not b2 and functionI.f(v, l[int(b)]):
                del listeI[e]
        return listeI
    #pset.addPrimitive(filter_reg, [str, BoolI, BoolI, RegexList,FunctionTypeI], RegexList)


    def map_fct(li, fu):
        out = [fu(l) for l in li]
        return out
    #pset.addPrimitive(map_fct, [RegexList, FunctionTypeI],RegexList)

    def indexOf(c, cL):
        if c in cL:
            return cL.index(c)  
        else:
            return -10 
    #pset.addPrimitive(indexOf, [int, IntList], int)


    def regexToTuple(r1, r2):
        return RegexTuple(r1, r2)
    #pset.addPrimitive(regexToTuple, [TypeRegex, TypeRegex], RegexTuple)

    def subString(x, s1, s2):
        return x[s1:s2]
    #pset.addPrimitive(subString, [str, int, int], str)

    def occurPosition(s1,s2):
        if s2 in s1:
            return s1.index(s2) 
        else:
            return 0 
    #pset.addPrimitive(occurPosition, [str,str], int)

    def lenStr(s):
        if type(s) == list or type(s) ==RegexList:
            return len(s)
        else:
            return None
    #pset.addPrimitive(lenStr, 2)

    def concat(x,t):

        if type(x) == type(t) and type(x) in [str, RegexList, list, ListString, IntList]:
            return x+t
        else:return None
    #pset.addPrimitive(addInt, 2)

    def append(x,y):
        neu = x
        neu.append(y)
        return neu
    #pset.addPrimitive(append, [ListString,str], ListString)

    for a in range(1,2):
        pset.addTerminal(a)
        pset.addTerminal(-a)
    pset.addTerminal(0,name='0')


    return pset
