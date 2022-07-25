"""
Module that allows to sample input-output samples.
In this module we define a function (sample_space) that allows to
draw samples from a given type, e.g. drawing samples from strings or integers.

Using these samples, we can draw an arbitrary amount of input-output samples
for a given operator.
"""
import random
import string

# import evoWFs.dsl
# from evoWFs.dsl import *
# import evoWFs.flashFill
from evoWFs.type_classes import RegexTuple, TypeII


# Letters, Numbers and Regeluar Expression on which we operate
# We oversample the space ' '
LETTERS = string.ascii_letters + "0123456789" + " " + " " + " "
numbers = [e for e in range(10)] + [-e for e in range(1, 10)]
UsefulRegexes = [r"\w+", r"\d+", r"\s+", r".+", r"$"]

# SPACE_DIC = {'k':  int, 'v': str, 'start': int, 'end': int, 'rr':RegexTuple}

# Parameters have a fixed, assigned type.
# This correspondence is describe in the SPACE_DIC dictionary
SPACE_DIC = {
    "k": int,
    "v": str,
    "str_input": str,
    "str_input_1": str,
    "str_input_2": str,
    "start": int,
    "end": int,
    "r1": TypeII,
    "r2": TypeII,
    "a": int,
    "b": int,
    "summand_1": int,
    "summand_2": int,
}


# Can be deleted???
trainInput = {}
for i in range(0, 70):
    trainInput[i] = ""
    for j in random.sample(
        range(0, len(LETTERS) - 1), random.randint(1, len(LETTERS) - 1)
    ):
        trainInput[i] += LETTERS[j]


def sample_space(space):
    """This function describes how to sample from a given space/type, e.g. how to sample a string
    Argument:
        space: A type like str, int or RegexTuple
    Return:
        One drawn element
    """
    if space == str:
        str_random = ""
        for i in random.sample(
            range(0, len(LETTERS) - 1), random.randint(1, len(LETTERS) - 1)
        ):
            str_random += LETTERS[i]
        return str_random

    if space == int:
        numbers = [e for e in range(10)] + [-e for e in range(1, 10)]
        return random.sample(numbers, 1)[0]
    elif space == RegexTuple:
        regex_set = [TypeRegex(r) for r in UsefulRegexes]
        regex_1 = random.sample(regex_set, 1)[0]
        regex_2 = random.sample(regex_set, 1)[0]
        return RegexTuple(regex_1, regex_2)
    elif space == TypeII:
        regex_set = [TypeII(r) for r in UsefulRegexes]
        regex_1 = random.sample(regex_set, 1)[0]
        return regex_1


def data_create(operator, parameters, n_samples=25):
    """Creates a training set of n_samples input-output samples.
    Input-outputs are described via a dictionary. The key 'out' denotes the output.
    Inputs to the operator are described via parameters, e.g. 'k', 'x'.
    Arguments:
        operator: operator/function to create input-output samples,
        parameters:
        n_samples: Amount of input-output samples to create

    Return:
        spec_train_cond: A dictionary with keys 0,1,...,n_samples
            where each value describes a full set of input-output of the operator.
            Note that the input-output set is described via a dictionary
            where each parameter is key to a corresponding value
    """

    spec_train_cond = {}
    for i in range(n_samples):

        spec_train_cond[i] = {}
        for p in parameters:
            spec_train_cond[i][p] = sample_space(SPACE_DIC[p])

        spec_train_cond[i]["out"] = operator(**spec_train_cond[i])

    return spec_train_cond


def create_conditions(spec_train_cond, wf_parameter="k", condi_params=[]):
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
    """
    spec_train_param = {}
    for i in spec_train_cond.keys():
        spec_train_param[i] = {}
        spec_train_param[i][wf_parameter] = spec_train_cond[i][wf_parameter]
        del spec_train_cond[i][wf_parameter]
        ###Only keep conditions
        del_p = []
        for k in spec_train_cond[i].keys():
            if k not in condi_params and k != "out":
                del_p.append(k)
        for k in del_p:
            del spec_train_cond[i][k]

    return spec_train_param, spec_train_cond
