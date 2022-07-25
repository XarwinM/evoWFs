"""
This module allows to learn a witness function for a given function.
As a DSL for the evolutionary algorithm we employ a DSL that is specialized in the numerical domain
(see evoWFs/math_operators/pset_math.py)
"""


import operator

# import math
import random

# import string

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

# import copy

# import sys
# sys.path.append("..")  # Adds higher directory to python modules path.

# from flashFill import createPset
# from regexFill import createPset
# from regexDsl import createPset
from evoWFs.math_operators.pset_math import create_pset

# from regexFill_no_type import createPset
from evoWFs.type_classes import IntList
from evoWFs.math_operators.dsl_math import addition, OPERATOR_PARAMETER_DIC
import evoWFs.spec as spec

# import evoWFs.spec_new as spec
# import regex

from evoWFs.evaluation import Signature, Evaluation  # levenshtein

from evoWFs.export_function import function_to_str, create_wf_file


def create_signature(parameter, condi_params, wf_out_type, out_type):
    """
    Creates Signature for a given Witness Function setting, i.e.
    for given condition parameters, the output type of the witness function
    and the output type of the operator.
    """
    input_sign = {}

    for i in condi_params:
        input_sign[i] = spec.SPACE_DIC[i]
    input_sign["out"] = out_type

    # return Signature(input_sign, spec.SPACE_DIC[parameter], parameter)
    return Signature(input_sign, wf_out_type, parameter)


def function_learning(
    operator_dsl,
    parameter="k",
    condi_params=[],
    wf_output_type=IntList,
    out_type=None,
):

    # Create signature of learning problem
    signature = create_signature(parameter, condi_params, wf_output_type, out_type)

    pset = create_pset(signature)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    # toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=4)
    toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=8)
    toolbox.register("individual", tools.initIterate, creator.Individual, toolbox.expr)
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)
    toolbox.register("compile", gp.compile, pset=pset)
    return signature, pset, toolbox


def training_single(toolbox):
    random.seed(318)

    pop = toolbox.population(n=1000)
    hof = tools.HallOfFame(5)

    stats_fit = tools.Statistics(lambda ind: ind.fitness.values)
    stats_size = tools.Statistics(len)
    mstats = tools.MultiStatistics(fitness=stats_fit, size=stats_size)
    mstats.register("avg", numpy.mean)
    mstats.register("std", numpy.std)
    mstats.register("min", numpy.min)
    mstats.register("max", numpy.max)

    pop, _ = algorithms.eaSimple(
        pop, toolbox, 0.5, 0.2, 200, stats=mstats, halloffame=hof, verbose=True
    )

    return hof[0]


def train(
    dsl_operator,
    parameter="k",
    condi_params=[],
    out_type=None,
    wf_output_type=IntList,
    num_wfs=1,
):
    """
    Evolutionary Optimization for witness function for a certain parameter and a given operator

    Argument:
        dsl_operator: function of operator,
        parameter: string that describes parameter for which we learn witness function,
        condi_params: list of strings that describe parameters
            that are given to the witness function as condition,
        out_type: type of output,
        wf_output_type: Output type of witness functions (usually a list),
        num_wfs: the number of witness functions we aim to learn for the given arguments,
    Return:
       - List of learned Witness Functions (deap objects)
       - Signature object (see evaluation.py)
    """

    # Create Training data (input-output examples)
    spec_train_cond = spec.data_create(
        dsl_operator, OPERATOR_PARAMETER_DIC[dsl_operator]
    )
    spec_train, spec_train_cond = spec.create_conditions(
        spec_train_cond, wf_parameter=parameter, condi_params=condi_params
    )
    signature, pset, toolbox = function_learning(
        dsl_operator,
        parameter=parameter,
        condi_params=condi_params,
        wf_output_type=wf_output_type,
        out_type=out_type,
    )

    # Define Evaluation (determines losses for given programs and training data)
    evaluation = Evaluation(
        [],
        parameter=signature.parameter,
        spec_train_cond=spec_train_cond,
        spec_train=spec_train,
        operator=dsl_operator,
        toolbox=toolbox,
    )

    toolbox.register("evaluate", evaluation.eval_spec, spec=spec_train)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=4)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate(
        "mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)
    )
    toolbox.decorate(
        "mutate",
        gp.staticLimit(key=operator.attrgetter("height"), max_value=17),
    )

    for _ in range(0, num_wfs):
        func_learned = training_single(toolbox)

        # Add Learned Witness function to Evluation
        # Enforces the new learned Witness function to be different from the previously learned WFs
        evaluation.add_learned_wf(func_learned)

        # print('Leanred ', evaluation.learnedWFs[-1])
        # if 1 in evaluation.lossLearnedWFs().values():
        #    print('bei Abbruch: ', evaluation.lossLearnedWFs())
        #    break
    # print(evaluation.lossLearnedWFs())
    return evaluation.learned_wfs, signature


if __name__ == "__main__":

    #a = [[addition, "b", ["a"], int, IntList]]
    a = [[addition, "summand_2", ["summand_1"], int, IntList]]

    learned_wfs_str = ""
    for t in a:
        # learnedWFs, signature = train(subStr, parameter='start', condi_params=['x'], out_type=str)
        learnedWFs, signature = train(*t)

        tree = gp.PrimitiveTree(learnedWFs[-1])
        # functions = gp.compile(tree, pset)

        input_vars = signature.input_types_wf.keys()

        learned_wfs_str += function_to_str(
            tree, input_vars, name=t[0].__name__, parameter=t[1]
        )

    print(learned_wfs_str)
    # create_wf_file(out)
