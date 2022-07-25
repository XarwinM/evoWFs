"""
Custom Types for Type Based genetic Programming. Most types do not have special properties.
But they allow to distinguish whether two objects are from the same type.
So we can tell for instance whether two list objects contain only integer or string.
"""
import regex

class TypeI:
    """
    Custom Type
    """
    def __init__(self, obj):
        self.obj = obj
    def __repr__(self):
        return "TypeI(" + repr(self.obj) + ")"
    def __eq__(self, other):
        return self.obj== other

class TypeII:
    """
    Custom Type where each instantiation is a regex object
    """
    def __init__(self, obj):
        self.reg = regex.compile(obj)
        self.pattern =regex.compile(obj).pattern
        self.type = type(regex.compile(obj))
    def __repr__(self):
        return "TypeII(" + repr(self.pattern) + ")"
    def __eq__(self, other):
        return self.reg == other
    def __getitem__(self):
        return self.reg

def TypeConstructorFunction(type_name):
    """
    Constructor of new type.
    New type of name type_name allows to create functions
    """

    class TypeFunction:
        """
        New type that allows to create functions
        """
        def __init__(self, name):
            self.name = name
            self.function = globals()[self.name]
            self.__name__ = type_name
        def __repr__(self):
            return  self.name + "(" + repr(self.name) + ")"
        def __eq__(self, other):
            return self.name == other
        def __getitem__(self):
            return self.function
    return TypeFunction


class IntList(list):
    """
    Custom type. Inherits from list and each object of
    IntList hast elements of same type
    """
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "IntList(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __eq__(self, other):
        return self.liste== other

class ListString(list):
    """
    Custom type. Inherits from list and each object of
    IntList hast elements of same type.
    """
    def __init__(self,liste):
        self.liste = liste
    def __repr__(self):
        return "ListString(" + repr(self.liste) + ")"
    def __getitem__(self, i):
        return self.liste[i]
    def __eq__(self, other):
        return self.liste== other

class RegexTuple:
    """
    Custom type. Constitutes Tuple for regexes. 
    RegexTuplehas elements of same type.
    """
    def __init__(self, reg1, reg2):
        self.tup = (reg1, reg2)
    def __repr__(self):
        return "RegexTuple(" + repr(self.tup[0])+',' +repr(self.tup[1]) + ")"
    def __eq__(self, other):
        return self.tup == other
    def __getitem__(self, i):
        return self.tup[i]
