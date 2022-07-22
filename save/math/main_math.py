import operator
#import math
import random
#import string

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

#import copy

import sys

sys.path.append("..")  # Adds higher directory to python modules path.

# from flashFill import createPset
# from regexFill import createPset
# from regexDsl import createPset
from mathDSL import createPset

# from regexFill_no_type import createPset
from evolutionaryWitnessFunctions.typeClasses import *
from dsl_math import *
#import spec
import spec_new as spec
#import regex

from evaluation import Signature, Evaluation, levenshtein

from export_function import *


def create_signature(parameter, condi_params, wf_out_type, out_type):
    """ """
    input_sign = {}

    for p in condi_params:
        input_sign[p] = spec.SPACE_DIC[p]
    input_sign["out"] = out_type

    # return Signature(input_sign, spec.SPACE_DIC[parameter], parameter)
    return Signature(input_sign, wf_out_type, parameter)


def function_learning(
    operator_dsl, parameter="k", condi_params=[], wf_output_type=IntList, out_type=None
):

    # signatureAbsPos = Signature({'x': str, 'k': int}, str, 'x')
    # signature = create_signature(parameter, condi_params, out_type)
    signature = create_signature(parameter, condi_params, wf_output_type, out_type)

    # KJjisignatureAbsPos = Signature({'x': str, 'out': int}, int, 'k')
    # signature = signatureAbsPos
    pset = createPset(signature)

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

    pop, log = algorithms.eaSimple(
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
        condi_params: list of strings that describe parameters that are given to the witness function as condition,
        out_type: type of output,
        wf_output_type: Output type of witness functions (usually a list),
        num_wfs: the number of witness functions we aim to learn for the given arguments,
    Return:
       - List of learned Witness Functions (deap objects)
       - Signature object (see evaluation.py)
    """

    # Create Training data (input-output examples)
    specTrainCond = spec.data_create(dsl_operator, OPERATOR_PARAMETER_DIC[dsl_operator])
    specTrain, specTrainCond = spec.create_conditions(
        specTrainCond, wf_parameter=parameter, condi_params=condi_params
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
        specTrainCond=specTrainCond,
        specTrain=specTrain,
        typ=wf_output_type,
        operator=dsl_operator,
        toolbox=toolbox,
    )

    toolbox.register("evaluate", evaluation.evalSpec, spec=specTrain)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=4)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate(
        "mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)
    )
    toolbox.decorate(
        "mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)
    )

    for i in range(0, num_wfs):
        funcLearned = training_single(toolbox)

        # Add Learned Witness function to Evluation
        # Enforces the new learned Witness function to be different from the previously learned WFs
        evaluation.addLearnedWF(funcLearned)

        # print('Leanred ', evaluation.learnedWFs[-1])
        # if 1 in evaluation.lossLearnedWFs().values():
        #    print('bei Abbruch: ', evaluation.lossLearnedWFs())
        #    break
    # print(evaluation.lossLearnedWFs())
    return evaluation.learnedWFs, signature


if __name__ == "__main__":

    # a = [[RelPos, 'r2', ['v', 'r1'], int, RegexList]]#$,
    a = [[addition, "b", ["a"], int, IntList]]  # $,

    out = ""
    for t in a:
        # learnedWFs, signature = train(subStr, parameter='start', condi_params=['x'], out_type=str)
        learnedWFs, signature = train(*t)

        tree = gp.PrimitiveTree(learnedWFs[-1])
        # functions = gp.compile(tree, pset)

        input_vars = signature.inpTypesWF.keys()

        out += function_to_str(tree, input_vars, name=t[0].__name__, parameter=t[1])

    print(out)
    # create_wf_file(out)
