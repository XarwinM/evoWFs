"""
This module provides functions to compare learned witness functions to
known/ground truth witness functions. Furthermore, it provides functions 
to analyze the learned witness functions, e.g. measure execution time.
"""
import re
import time
from prettytable import PrettyTable

from evoWFs.results.wf_for_cs import (  # pylint: disable=unused-import
    wf_substring_start,
    wf_substring_end,
    wf_concat_v,
    wf_concat_s,
    wf_abs_pos_k,
)
from evoWFs.type_classes import IntList, ListString
import evoWFs.spec_new as spec_new
from evoWFs.text_operators.dsl_text import substring, abs_pos, concat


def wf_true_substring_start(str_input, out):
    """
    Expert witness function for substring operator
    and 'start' parameter
    """
    return [m.start() for m in re.finditer(re.escape(out), str_input)]


def wf_true_substring_end(str_input, start, out):  # pylint: disable=unused-argument
    """
    Expert witness function for substring operator
    and 'end' parameter
    """
    return [start + len(out)]


def wf_true_abs_pos_k(str_input, out):
    """
    Expert witness function for AbsPos operator
    and 'end' parameter
    """
    return [out + 1, out - len(str_input) - 1]


def wf_true_concat_v(out):
    """
    Expert witness function for concat operator
    and 'first' parameter
    """
    return [out[0:i] for i in range(1, len(out))]


def wf_true_concat_s(str_input_1, out):
    """
    Expert witness function for concat operator
    and 'second' parameter
    """
    return [out[len(str_input_1) :]]


def measure_metric(
    operator,
    witness_function,
    spec_train,
    spec_train_cond,
    parameter,
    metric="jaccard_index",
):
    """
    Computes the given metric for the learned witness function.
    Arguments:
        operator: Operator for which witness function has been learned,
        witness_function: Learned witness function,
        spec_train: Training specification,
        spec_train_cond: Training data for witness function, i.e. input-outputs to wf,
        parameter: Parameter for which witness function has been learned,
        metric: Metric on how we evaluate the witness function
    Return:
        metric_out: Measured metric on spec_train and spec_train_cond of witness function
    """
    i = 0
    metric_out = 0
    for j in spec_train.keys():

        w_out = witness_function(**spec_train_cond[j])
        w_out_true = []
        w_out_true = witness_fct_dic[operator][parameter](**spec_train_cond[j])
        metric_out += eval(metric)(w_out, w_out_true)
        i += 1

    return metric_out / i


def measure_time(witness_function, spec_train_cond, spec_train):
    """Measure average execution time for Witness Function wf"""
    elapsed_time = 0
    i = 0
    for j in spec_train.keys():
        start = time.time()
        witness_function(**spec_train_cond[j])
        end = time.time()
        elapsed_time += end - start
        i += 1

    return (elapsed_time / i) * 1000


def measure_agnostic_recall(witness_function, spec_train_cond, spec_train, param):
    """Measure agnostic recall as defined in thesis on spec_train_cond and spec_train"""
    corr = 0
    i = 0
    for j in spec_train.keys():
        w_out = witness_function(**spec_train_cond[j])
        if spec_train[j][param] in w_out:
            corr += 1
        i += 1

    return corr / i


def jaccard_index(retrieved, relevant):
    """Computes the Jaccard-Index/Jaccard-Similarity between two sets"""
    return len(set(retrieved).intersection(set(relevant))) / len(
        set(retrieved).union(set(relevant))
    )


def precision(retrieved, relevant):
    """Computes the Precision between two sets."""
    if len(set(retrieved)) == 0:
        return 0
    return len(set(retrieved).intersection(set(relevant))) / len(set(retrieved))


def recall(retrieved, relevant):
    """Computes the Recall between two sets"""
    if len(set(retrieved)) == 0:
        return 0
    return len(set(retrieved).intersection(set(relevant))) / len(set(relevant))


witness_fct_dic = {
    substring: {"start": wf_true_substring_start, "end": wf_true_substring_end},
    concat: {"str_input_1": wf_true_concat_v, "str_input_2": wf_true_concat_s},
    abs_pos: {"k": wf_true_abs_pos_k},
}

if __name__ == "__main__":

    a = [[substring, "start", ["str_input"], str, IntList, "substring_start"]]
    a.append([substring, "end", ["str_input", "start"], str, IntList, "substring_end"])
    a.append([concat, "str_input_1", [], str, ListString, "concat_v"])
    a.append([concat, "str_input_2", ["str_input_1"], str, ListString, "concat_s"])
    a.append([abs_pos, "k", ["str_input_1"], int, IntList, "abs_pos_k"])

    creators_dic = {
        substring: "condition_creator_substring",
        abs_pos: "condition_creator_abspos",
        concat: "condition_creator_concat",
    }

    out_dic = {}

    metrics = ["jaccard_index", "precision", "recall"]

    for t in a:
        spec_train, spec_train_cond = spec_new.create_conditions(
            t[0],
            wf_parameter=t[1],
            condi_params=t[2],
            creator=creators_dic[t[0]],
            n_samples=500,
        )

        out_dic[t[-1]] = {}
        for m in metrics:
            out_dic[t[-1]][m] = measure_metric(
                t[0], eval("wf_" + t[-1]), spec_train, spec_train_cond, t[1], metric=m
            )

        out_dic[t[-1]]["time"] = measure_time(
            eval("wf_" + t[-1]), spec_train_cond, spec_train
        )

        out_dic[t[-1]]["agnostic_recall"] = measure_agnostic_recall(
            eval("wf_" + t[-1]), spec_train_cond, spec_train, t[1]
        )

    # print(out_dic)
    TABLE = PrettyTable()
    TABLE.field_names = ["Operator and Parameter"] + list(out_dic[t[-1]].keys())

    for k in out_dic:
        TABLE.add_rows([[k] + list(out_dic[k].values())])

    print(TABLE)
