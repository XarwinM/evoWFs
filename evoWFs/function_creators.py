"""
Function-Creators that allow to create functions that
have a specific name. For instance, we can create several instances
of identity function (each distinguishable and with separate name)
"""


def ident_f(name):
    """
    Creator for identity function. Returns identity function
    with name name
    """

    def i_f(x_input):
        """Identity Function"""
        return x_input

    # Make new function identifiable under name
    i_f.__name__ = name

    return i_f


def compare_f(name):
    """
    Creator for function of the form (x -> (x->y)
    """

    def comp_1(input_a):
        def comp_2(input_b):
            return input_a == input_b

        comp_2.__name__ = name + "_2_" + str(input_a)
        return comp_2

    # Assign name to function
    comp_1.__name__ = name + "_1_"

    return comp_1


def function_comb(name):
    """
    Creator for function that applies a given function on a given element
    """

    def fc_comb(element, func):
        """Applies func on element"""
        return func(element)

    # Assign name to function
    fc_comb.__name__ = name
    return fc_comb


def map_f(name):
    """
    Creator for map function. Returns map function
    with name name
    """

    def m_f(liste, func):
        """Map Function"""
        return [func(l) for l in liste]

    # Assign name to map function
    m_f.__name__ = name

    return m_f


def filter_f(name):
    """
    Creator for filter function. Returns filter function
    with name name
    """

    def f_f(liste, func):
        out = []
        for element in liste:
            if func(element):
                out.append(element)

        return out

    # Assign name to filter function
    f_f.__name__ = name

    return f_f


def add_f(name):
    """
    Creator for function that returns another function.
    In total we perform the addition operation.
    x -> (y->x+y).
    """

    def a_f(summand_1):
        def a_t(summand_2):
            return summand_1 + summand_2

        return a_t

    # Assign name to function
    a_f.__name__ = name
    return a_f


def append_f(name):
    """
    Creator that creates append-function
    """

    def a_f(liste, element):
        """Appends element to liste"""
        out = liste.copy()
        out.append(element)
        return out

    # Assign name to function
    a_f.__name__ = name
    return a_f


def element_in(name):
    """
    Creator that creates function that checks whether
    element is in a list
    """

    def e_f(liste, element):
        """Checks whether element is in List. Return boolean value"""
        if element in liste:
            return True
        return False

    # Assign name to function
    e_f.__name__ = name
    return e_f


def len_f(name):
    """
    Creator that creates function that returns length of list
    """

    def l_f(x_list):
        """Return length of list"""
        return len(x_list)

    # Assign name to function
    l_f.__name__ = name
    return l_f


def index_f(name):
    """
    Creator that creates function that returns index of element in list
    """

    def indexOf(element, x_list):
        """
        Returns index of element in x_list if element is in x_list
        and -10 otherwise
        """
        if element in x_list:
            return x_list.index(element)
        # -10 represents the value when the element is not in list
        return -10

    # Assign name to function
    indexOf.__name__ = name
    return indexOf
