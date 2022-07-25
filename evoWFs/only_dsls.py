"""
j
"""
import regex

from evoWFs.type_classes import IntList, ListString
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


app_i = append_f("app_i")
index_il = index_f("index_il")
index_sl = index_f("index_sl")
map_i = map_f("map_i")
map_s = map_f("map_s")
map_s_i = map_f("map_s_i")


len_il = len_f("len_il")
len_s = len_f("len_s")
len_sl = len_f("len_sl")

id_s = ident_f("id_s")
id_sl = ident_f("id_sl")
id_rt = ident_f("id_rt")
id_r = ident_f("id_r")
id_i = ident_f("id_i")

add_i = add_f("add_i")

app_r = append_f("app_r")
app_rt = append_f("app_rt")
app_s = append_f("app_s")


def create_range(i, j):
    if i <= 0 or i >= j:
        return []
    if i > 0 and j > i:
        return list(range(i, j))
    else:
        return []


def subset_sel_1(v, i):
    def new_subset(j):
        if type(v) != str:
            import pdb

            pdb.set_trace()
        if len(v) >= j and j > 0 and j >= i and i >= 0:
            return v[i:j]
        else:
            return ""

    return new_subset



def subset_sel(i, j):
    def new_subset(v):
        if i >= 0 and j > i and len(v) >= j:
            return v[i:j]
        else:
            return ""

    return new_subset


def neg_int(a):
    return -a


def add_f_2(a, func):
    return func(a)


def concat(x, y):
    return x + y


def regexToTuple(r1, r2):
    return RegexTuple(r1, r2)


def matches(v, rr):
    r = "(?<=" + rr[0].pattern + ")" + rr[1].pattern
    it = regex.finditer(r, v)
    outList = []
    for i in it:
        outList.append(i.start())
    return outList


def intToList(x):
    return [x]


def addInt(x, t):
    return x + t


def occurPosition(s1, s2):
    if s2 in s1:
        return s1.index(s2)
    else:
        return 0


def regTupList(r):
    return [r]


def chooseRegList_1(l, i):
    if i >= 0 and i < len(l):
        return l[i][1]
    else:
        return TypeRegex(r"")


def indexOf(c, cL):
    if c in cL:
        return cL.index(c)
    else:
        return -10


def toRegexTuple(r1, r2):
    return RegexTuple(r1, r2)


def matchesTrue(v, r):
    it = regex.search(r.reg, v)
    if it == None:
        return TypeRegex(r"")
    else:
        return r


def filter_reg(v, b, b2, listeI, functionI):
    for e, l in enumerate(listeI):
        try:
            if not functionI.f(v, l[int(b)]) and b2:
                del listeI[e]
        except:
            return
    return listeI
