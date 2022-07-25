"""
This module allows to learn a witness function for a given function.
As a Domain Specific Language (DSL) for the evoltionary algorithm
we employ a DSL that operates on the text domain (see evoWFs/text_operators/pset_text.py)
"""
import operator
import random

import numpy

from deap import algorithms
from deap import base
from deap import creator
from deap import tools
from deap import gp

from evoWFs.text_operators.pset_text import create_pset

from evoWFs.type_classes import IntList, ListString
from evoWFs.text_operators.dsl_text import (  # pylint: disable=unused-import
    substring,
    const_str,
    concat,
    abs_pos,
)
import evoWFs.spec_new as spec_new

from evoWFs.evaluation import Evaluation

from evoWFs.export_function import create_wf_file, function_to_str

from evoWFs.math_operators.main_math import create_signature


def function_learning(
    operator_dsl, parameter="k", condi_params=[], wf_output_type=IntList, out_type=None
):
    """ """

    # Create Signature of learning problem
    signature = create_signature(parameter, condi_params, wf_output_type, out_type)

    pset = create_pset(signature)

    creator.create("FitnessMin", base.Fitness, weights=(-1.0,))
    creator.create("Individual", gp.PrimitiveTree, fitness=creator.FitnessMin)

    toolbox = base.Toolbox()
    toolbox.register("expr", gp.genGrow, pset=pset, min_=1, max_=12)
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
        pop, toolbox, 0.5, 0.2, 1000, stats=mstats, halloffame=hof, verbose=True
    )

    return hof[0]


def train(
    dsl_operator, parameter="k", condi_params=[], out_type=None, wf_output_type=IntList
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

    # spec_train_cond = spec.data_create(dsl_operator, OPERATOR_PARAMETER_DIC[dsl_operator])
    spec_train, spec_train_cond = spec_new.create_conditions(
        dsl_operator,
        wf_parameter=parameter,
        condi_params=condi_params,
        creator=creators_dic[dsl_operator],
    )
    signature, pset, toolbox = function_learning(
        dsl_operator,
        parameter=parameter,
        condi_params=condi_params,
        wf_output_type=wf_output_type,
        out_type=out_type,
    )

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
        "mutate", gp.staticLimit(key=operator.attrgetter("height"), max_value=17)
    )

    for _ in range(0, 1):
        func_learned = training_single(toolbox)
        evaluation.add_learned_wf(func_learned)
        print("Leanred ", evaluation.learned_wfs[-1])
        if 1 in evaluation.loss_learned_wfs().values():
            print("bei Abbruch: ", evaluation.loss_learned_wfs())
            break
    # print(evaluation.lossLearnedWFs())
    return evaluation.learned_wfs, signature


creators_dic = {
    substring: "condition_creator_substring",
    abs_pos: "condition_creator_abspos",
    concat: "condition_creator_concat",
}

if __name__ == "__main__":

    operator_candidates = [[substring, "start", ["str_input"], str, IntList]]
    operator_candidates.append([substring, "end", ["str_input", "start"], str, IntList])
    operator_candidates.append([concat, "str_input_1", [], str, ListString])
    operator_candidates.append([concat, "str_input_2", ["str_input_1"], str, ListString])
    operator_candidates.append([abs_pos, "k", ["str_input"], int, IntList])

    OUT = ""
    for operator_candidate in operator_candidates:
        learnedWFs, signature = train(*operator_candidate)

        tree = gp.PrimitiveTree(learnedWFs[-1])

        input_vars = signature.input_types_wf.keys()

        OUT += function_to_str(
            tree,
            input_vars,
            name=operator_candidate[0].__name__,
            parameter=operator_candidate[1],
        )

    create_wf_file(OUT)

    print(OUT)
