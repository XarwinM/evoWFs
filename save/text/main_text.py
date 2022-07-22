import operator
import math
import random
import string

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

import copy

import sys
sys.path.append('..')

#from flashFill import createPset
#from regexFill import createPset
#from regexDsl import createPset
#from mathDSL import createPset
from textDSL import createPset
#from regexFill_no_type import createPset
from typeClasses import *
from dsl_text import *
import spec_new
import regex

from evaluation import Signature, Evaluation, levenshtein

from export_function import *

from main_math import create_signature 

def function_learning(operator_dsl,
        parameter='k',
        condi_params=[],
        wf_output_type=IntList,
        out_type=None):

    #signatureAbsPos = Signature({'x': str, 'k': int}, str, 'x')
    #signature = create_signature(parameter, condi_params, out_type)
    signature = create_signature(parameter, condi_params, wf_output_type, out_type)

    #KJjisignatureAbsPos = Signature({'x': str, 'out': int}, int, 'k')
    #signature = signatureAbsPos
    pset = createPset(signature)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    #toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=4)
    toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=12)
    #toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=8)
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

    pop, log = algorithms.eaSimple(pop, toolbox, 0.5, 0.2, 1000, stats=mstats,
                                   halloffame=hof, verbose=True)


    return(hof[0])


def train(dsl_operator, parameter='k', condi_params=[], out_type=None, wf_output_type=IntList):

    #specTrainCond = spec.data_create(dsl_operator, OPERATOR_PARAMETER_DIC[dsl_operator])
    specTrain, specTrainCond= spec_new.create_conditions(dsl_operator,wf_parameter=parameter, condi_params=condi_params, creator=creators_dic[dsl_operator])
    signature, pset, toolbox = function_learning(dsl_operator, parameter=parameter, condi_params=condi_params, wf_output_type=wf_output_type, out_type=out_type)

    evaluation = Evaluation([],  parameter=signature.parameter, specTrainCond=specTrainCond, specTrain=specTrain, typ=wf_output_type, operator=dsl_operator, toolbox=toolbox)

    toolbox.register("evaluate", evaluation.evalSpec, spec=specTrain)
    toolbox.register("select", tools.selTournament, tournsize=2)
    toolbox.register("mate", gp.cxOnePoint)
    toolbox.register("expr_mut", gp.genFull, min_=0, max_=4)
    toolbox.register("mutate", gp.mutUniform, expr=toolbox.expr_mut, pset=pset)

    toolbox.decorate("mate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))
    toolbox.decorate("mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17))


    for i in range(0,1):
        funcLearned = training_single(toolbox)
        evaluation.addLearnedWF(funcLearned)
        print('Leanred ', evaluation.learnedWFs[-1])
        if 1 in evaluation.lossLearnedWFs().values():
            print('bei Abbruch: ', evaluation.lossLearnedWFs())
            break
    print(evaluation.lossLearnedWFs())
    return evaluation.learnedWFs, signature

creators_dic = {Substring: 'condition_creator_substring', AbsPos:'condition_creator_abspos', Concat:'condition_creator_concat'}

if __name__ == "__main__":

    a =[[Substring, 'start', ['v'], str, IntList]]
    a.append(  [Substring, 'end', ['v', 'start'], str, IntList]) #works 
    a.append([Concat, 'v', [], str, ListString])
    a.append([Concat, 's', ['v'], str, ListString])
    a.append([AbsPos, 'k', ['v'], int, IntList])
    #a = [[RelPos, 'r2', ['v', 'r1'], int, RegexList]]#$,
    # Concat



    out = ""
    for t in a:
        learnedWFs, signature = train(*t)

        tree = gp.PrimitiveTree(learnedWFs[-1])

        input_vars = signature.inpTypesWF.keys()

        out += function_to_str(tree, input_vars, name=t[0].__name__, parameter=t[1])

    create_wf_file(out)

    print(out)
