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

def match_left(v,r):
    it = regex.search(r[0].reg, v)
    if it == None:
        return True 
    else:
        return False 

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
    pset.context["IntTuple"] =IntTuple 
    pset.context["bool"] = bool
    pset.context["FunctionTypeI"] =FunctionTypeI# type(lambda x: list(map(f, x)))

    pset.addTerminal(RegexTuple(TypeRegex(r'\+s'), TypeRegex(r'\w+')), RegexTuple)
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

    #pset.addTerminal(FunctionTypeI(match_right), FunctionTypeI)
    pset.addTerminal(FunctionTypeI("match_left"), FunctionTypeI)
    #pset.addTerminal(FunctionTypeI(43), FunctionTypeI)
    #pset.addTerminal(match_left, type(lambda x: list(map(f, x))))

    def idem(v):
        #return FunctionTypeI(match_right)
        return v
    pset.addPrimitive(idem, [FunctionTypeI],FunctionTypeI)

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

    def matchLeft(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return False 
        else:
            return True 
    ###CHange back
    pset.addPrimitive(matchLeft, [str, TypeRegex], bool)


    def filter_reg(v, listeI, functionI):
        for e, l in enumerate(listeI):
            if not functionI.f(v, l):
                del listeI[e]
        return listeI
    pset.addPrimitive(filter_reg, [str, RegexList,FunctionTypeI], RegexList)

    def matchRight(v,r):
        it = regex.search(r.reg, v)
        if it == None:
            return -10
        else:
            return it.span()[1]
    ###CHange back
    pset.addPrimitive(matchRight, [str, TypeRegex], int)

    def chooseRegList_0(l, i):
        if i >=0 and i < len(l):
            return l[i][0]
        else:
            return TypeRegex(r'')
    pset.addPrimitive(chooseRegList_0, [RegexList, int],TypeRegex )

    def chooseRegList_1(l, i):
        if i >=0 and i < len(l):
            return l[i][1]
        else:
            return TypeRegex(r'')
    pset.addPrimitive(chooseRegList_1, [RegexList, int],TypeRegex )

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
    #pset.addPrimitive(concat, [IntList,IntList], IntList)

    def append(x,y):
        neu = x
        neu.append(y)
        return neu
    #pset.addPrimitive(append, [list,RegexTuple], list)
    #pset.addPrimitive(append, [RegexList,RegexTuple], RegexList)
    #pset.addPrimitive(append, [IntList,int], IntList)

    for a in range(1,2):
        pset.addTerminal(a,int)
        pset.addTerminal(-a,int)
    pset.addTerminal(0,int)
    pset.addTerminal(True,bool)
    pset.addTerminal(False,bool)


    #for a in string.ascii_letters:
    #    pset.addTerminal(a,str)
    #pset.addTerminal(' ', str)

    return pset
