"""Operators of the text domain. For each of these operators we aim to learn a witness function"""

import regex

# from regex import *

def const_str(s):
    """Returns string as it is"""
    return s


def substring(v, start, end):
    """Returns a substring of input string v"""
    return v[start:end]


def concat(v, s):
    """Returns concatenation of two input strings"""
    return v + s


def abs_pos(v, k):
    """Implements AbsPos operator as described in thesis"""
    if k < 0:
        return len(v) + k + 1
    else:
        return k - 1

    """
    if type(k)==int:
        return k-1
    else:
        return k[0]-1
    """


def rel_pos(v, r1, r2):
    # left = rr[0].pattern
    # right = rr[1].pattern
    left = r1.pattern
    right = r2.pattern
    import re

    rightMatches = re.findall(right, v)
    leftMatches = re.findall(left, v)
    for lm in leftMatches:
        for rm in rightMatches:
            if v.index(rm) == v.index(lm) + len(lm):
                # return leftMatch.Index + leftMatch.Length;
                return v.index(lm) + len(lm)
    return -10


def RelPosA(v, rr, k=1):
    r = "(?<=" + rr[0].pattern + ")" + rr[1].pattern
    m = regex.finditer(r, v)
    count = sum(1 for _ in m)
    m = regex.finditer(r, v)
    i = 0
    if k > 0:
        i = k - 1
    else:
        i = k + count

    j = 0
    for a in m:
        if j == i:
            return a.start()
        j += 1
    if i < 0 or i >= count:
        return -10


def linesMap(func, Ls):
    new = []
    for x in Ls:
        new.append(func(x))
    return new


# OPERATOR_PARAMETER_DIC = {AbsPos: ['v', 'k'], Substring:['v', 'start', 'end'], RelPos:['v', 'rr']}
OPERATOR_PARAMETER_DIC = {
    abs_pos: ["v", "k"],
    substring: ["v", "start", "end"],
    rel_pos: ["v", "r1", "r2"],
    const_str: ["s"],
    concat: ["v", "s"],
}
