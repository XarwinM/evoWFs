
def ident_f(name):

    def i_f(v):
        return v

    i_f.__name__ = name

    return i_f

def compare_f(name):

    def comp_1(a):

        def comp_2(b):
            #if a == b:
            #    return True
            #else:
            #    return False
            return True
        comp_2.__name__ = name +'_2_' + str(a) 
        return comp_2
    comp_1.__name__ = name +'_1_'

    return comp_1

def function_comb(name):
    def fc_comb(a, func):
        return func(a) 
    fc_comb.__name__ = name
    return fc_comb

def negate(name):
    def neg(a):
        return not a
    neg.__name__ = name
    return neg

def map_f(name):

    def m_f(liste, func):
        return [func(l) for l in liste]
    m_f.__name__ = name

    return m_f

def filter_f(name):

    def f_f(liste, func):
        out = []
        #pdb.set_trace()
        #for l in liste:
        #    if func.f(l):
        #        out.append(l)

        return out
    f_f.__name__ = name
    return f_f

def add_f(name):

    def a_f(a):
        def a_t(b):
            return a+b
        return a_t

    a_f.__name__ = name
    return a_f

def append_f(name):
    def a_f(liste, a):
        out = liste.copy()
        out.append(a)
        return out 
    a_f.__name__=name
    return a_f

def element_in(name):

    def e_f(liste,a):
        if a in liste:
            return True
        else:
            return False

    e_f.__name__ = name
    return e_f

def len_f(name):
    def l_f(a):
        return len(a)
    l_f.__name__ = name
    return l_f

def index_f(name):
    def indexOf(c, cL):
        if c in cL:
            return cL.index(c)
        else:
            return -10
    indexOf.__name__ = name
    return indexOf




