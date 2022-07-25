"""
This module offers different functions that draw samples
for input values of different operators. Here we consider
only operators of the Substring DSL (see thesis)
"""

import random

from evoWFs.spec import LETTERS



def create_random_int_substr(x_str, cond=[]):
    """
    Creates a random integer value which serves as
    starting/ending position (depending on cond)
    for the substring-operator and input x_str
    """
    if cond == []:
        return random.randint(0, len(x_str)-1)
    return random.randint(cond[0]+1, len(x_str))


def condition_creator_substring():
    """
    Creates random inputs for substrings
    """
    str_random = create_random_str()
    start = create_random_int_substr(str_random, cond=[])
    end = create_random_int_substr(str_random, cond=[start])
    return {'v':str_random, 'start':start,'end': end}

def condition_creator_substring_2():
    """
    Creates random inputs for substrings
    Each string contains at most 15 chars
    """
    str_random = create_random_str()[:5]
    str_random = str_random+str_random +str_random
    start = create_random_int_substr(str_random, cond=[])
    end = create_random_int_substr(str_random, cond=[start])
    return {'v':str_random, 'start':start,'end': end}

def create_random_str(min_length=2):
    """
    Creates random string of length min_length
    """

    chars = LETTERS
    int2char = dict(enumerate(chars))
    str_random = ""
    while len(str_random) <= min_length:
        for k in random.sample(range(0,len(LETTERS)-1),random.randint(1,20)):
            str_random += LETTERS[k]
        if len(str_random) > 20:
            str_random = str_random[:random.randint(10, 20)]

    return str_random

def condition_creator_abspos():
    """
    Creates random inputs for abs_pos operator
    """
    str_random = create_random_str()
    k = create_random_int_substr(str_random, cond=[])
    k *= (2*random.randint(0,1)-1)

    return {'v':str_random,'k':k}

def condition_creator_concat():
    """
    Creates random inputs for concat operator
    """
    str_random_1 = create_random_str(min_length=1)
    str_random_1 = str_random_1[:random.randint(1,len(str_random_1))][:10]

    str_random_2 = create_random_str(min_length=1)
    str_random_2 = str_random_2[:random.randint(1,len(str_random_2))][:10]
    return {'v' : str_random_1,'s' : str_random_2}

def create_conditions(operator,
        wf_parameter='k',
        condi_params=[],
        creator='condition_creator_substring',
        n_samples=50):
    """
    Arguments:
        spec_train_cond: Training set to learn Witness Function,
        wf_parameter: parameter (described as string) for which we aim
        to learn the Witness Function,
        condi_params: list of parameters (described as strings) on which
            we condition the Witness Function
    Return:
        spec_train_param: Dictionary of training instances, where each training instance
            consists of a single key-value dictionary with
            'key' wf_parameter and as 'value' its corresponding value.
        spec_train_cond: Input Training set with certain information removed;
            Data about wf_parameter and condi_params has been deleted
    ToDo: This function bears some similarities to the function create_conditions
    in spec.py. Both implement the same functionalities and have to be merged at some point
    """

    spec_train_param ={}
    spec_train_cond={}
    for i in range(n_samples):
        spec_train_cond[i] = eval(creator)()
        spec_train_cond[i]['out'] = operator(**spec_train_cond[i]  )
    for i in spec_train_cond.keys():
        spec_train_param[i] = {}
        spec_train_param[i][wf_parameter] = spec_train_cond[i][wf_parameter]
        del spec_train_cond[i][wf_parameter]
        ###Only keep conditions
        del_p = []
        for k in spec_train_cond[i].keys():
            if k not in condi_params and k != 'out':
                del_p.append(k)
        for k in del_p:
            del spec_train_cond[i][k]

    return spec_train_param, spec_train_cond
