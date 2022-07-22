import operator
import math
import random
import string

import numpy

import copy

from typing import Dict, Tuple
import regex

def match_left(v,r):
    it = regex.search(r.reg, v)
    if it == None:
        return False 
    else:
        return True 

def match_word(v,r):
    it = regex.search(r.reg, v)
    if it == None:
        return '' 
    else:
        return it.group()

class BoolI:
    def __init__(self, b):
        self.b = b 
    def __repr__(self):
        return "BoolI(" + repr(self.b) + ")" 
    def __eq__(self, other):
        return self.b== other

class t1:
    def __init__(self, b):
        self.b = b 
    def __repr__(self):
        return "t1(" + repr(self.b) + ")" 
    def __eq__(self, other):
        return self.b== other

class t3:
    def __init__(self, b):
        self.b = b 
    def __repr__(self):
        return "t3(" + repr(self.b) + ")" 
    def __eq__(self, other):
        return self.b== other

class IntTuple:
    def __init__(self, num1, num2):
        self.tup = (num1,num2)
    def __repr__(self):
        return self.tup 
    def __eq__(self, other):
        return self.tup== other

def TypeConstructorType(t):

    class TypeT: 
        def __init__(self, name):
            self.name = name 
            self.__name__ = t
        def __repr__(self):
            return  self.__name__ + "(" + repr(self.name) + ")"
        def __eq__(self, other):
            return self.name == other
    #def __getitem__(self):
    #    return self.f
    return TypeT 

def TypeConstructorFunction(t):

    class TypeF: 
        def __init__(self, name):
            self.name = name 
            self.f= globals()[self.name]#f 
            self.__name__ = t
        def __repr__(self):
            return  self.name + "(" + repr(self.name) + ")"
        def __eq__(self, other):
            return self.name == other
        def __getitem__(self):
            return self.f
    return TypeF

class FunctionTypeII:
    def __init__(self, name):
        self.name = name 
        self.f= globals()[self.name]#f 
    def __repr__(self):
        return  "FunctionTypeI(" + repr(self.name) + ")"
    def __eq__(self, other):
        return self.name == other
    def __getitem__(self):
        return self.f

class FunctionTypeI:
    def __init__(self, name):
        self.name = name 
        self.f= globals()[self.name]#f 
    def __repr__(self):
        return  "FunctionTypeI(" + repr(self.name) + ")"
    def __eq__(self, other):
        return self.name == other
    def __getitem__(self):
        return self.f

class t2:
    def __init__(self, s):
        self.reg = regex.compile(s)
        self.pattern =regex.compile(s).pattern
        self.type = type(regex.compile(s))
    def __repr__(self):
        return "t2(" + repr(self.pattern) + ")" 
    def __eq__(self, other):
        return self.reg == other
    def __getitem__(self):
        return self.reg

class TypeRegex:
    def __init__(self, s):
        self.reg = regex.compile(s)
        self.pattern =regex.compile(s).pattern
        self.type = type(regex.compile(s))
    def __repr__(self):
        return "TypeRegex(" + repr(self.pattern) + ")" 
    def __eq__(self, other):
        return self.reg == other
    def __getitem__(self):
        return self.reg

class RegexTuple:
    def __init__(self, reg1, reg2):
        self.tup = (reg1, reg2)
    def __repr__(self):
        return "RegexTuple(" + repr(self.tup[0])+',' +repr(self.tup[1]) + ")" 
    def __eq__(self, other):
        return self.tup == other
    def __getitem__(self, i):
        return self.tup[i]

class RegexList(list):
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "RegexList(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __len__(self):
        return len(self.liste)
    def append(self, value):
        self.insert(len(self) + 1, value)
    def __getitem__(self, index):
        return self.liste.__getitem__(index)
    def __eq__(self, other):
        return self.liste== other


class RegexListI(list):
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "RegexList(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __eq__(self, other):
        return self.liste== other

class IntList(list):
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "RegexList(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __eq__(self, other):
        return self.liste== other

class ListString(list):
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "RegexList(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __eq__(self, other):
        return self.liste== other
