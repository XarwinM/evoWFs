from wf_for_cs import *
from typeClasses import *

from dsl_text import *

import spec_new 

import re
import time

def wf_true_substring_start(v, out):
    ### Has to be corrected
    #return [v.index(out)]
    return [m.start() for m in re.finditer(re.escape(out), v)] 

def wf_true_substring_end(v, start, out):
    return [start+len(out)]

def wf_true_AbsPos_k(v, out):
    return [out+1, out-len(v)-1]

def wf_true_Concat_v(out):
    return [out[0:i] for i in range(1,len(out)) ]

def wf_true_Concat_s(v,out):
    return [out[len(v):]]


def measure_metric(operator, wf, specTrain, specTrainCond, parameter, metric='jaccard_index'): 
    n = 0
    metric_out = 0
    for k in specTrain.keys():

        w_out = wf(**specTrainCond[k])
        w_out_true = []
        w_out_true = witness_fct_dic[operator][parameter](**specTrainCond[k])
        metric_out += eval(metric)(w_out, w_out_true)
        n += 1 

    return metric_out / n

def measure_time(wf, specTrainCond, specTrain):
    elapsed_time = 0
    n=0
    for k in specTrain.keys():
        start = time.time()
        w_out = wf(**specTrainCond[k])
        end = time.time()
        elapsed_time += end-start
        n+=1

    return (elapsed_time/n)*1000


def measure_agnostic_recall(wf, specTrainCond, specTrain, param):
    corr = 0
    n=0
    for k in specTrain.keys():
        w_out = wf(**specTrainCond[k])
        if specTrain[k][param] in w_out:
            corr += 1
        n +=1

    return corr / n


def jaccard_index(A,B):
    return len(set(A).intersection(set(B))) / len(set(A).union(set(B)))

def precision(A,B):
    if len(set(A)) == 0:
        return 0
    return len(set(A).intersection(set(B))) / len(set(A))

def recall(A,B):
    if len(set(A)) == 0:
        return 0
    return len(set(A).intersection(set(B))) / len(set(B))


witness_fct_dic = {Substring: {'start':wf_true_substring_start, 'end':wf_true_substring_end}, Concat:{'v':wf_true_Concat_v, 's':wf_true_Concat_s}, AbsPos:{'k':wf_true_AbsPos_k} }

if __name__ == "__main__":

    a =[[Substring, 'start', ['v'], str, IntList, 'Substring_start']]
    a.append(  [Substring, 'end', ['v', 'start'], str, IntList, 'Substring_end']) #works 
    a.append([Concat, 'v', [], str, ListString, 'Concat_v'])
    a.append([Concat, 's', ['v'], str, ListString, 'Concat_s'])
    a.append([AbsPos, 'k', ['v'], int, IntList, 'AbsPos_k'])

    creators_dic = {Substring: 'condition_creator_substring', AbsPos:'condition_creator_abspos', Concat:'condition_creator_concat'}
    
    out_dic = {}

    metrics = ['jaccard_index', 'precision', 'recall']

    for t in a:
        specTrain, specTrainCond= spec_new.create_conditions(t[0],wf_parameter=t[1], condi_params=t[2], creator=creators_dic[t[0]], n_samples=500)

        out_dic[t[-1]] = {}
        for m in metrics:
            out_dic[t[-1]][m] = measure_metric(t[0], eval('wf_'+ t[-1]), specTrain, specTrainCond, t[1], metric=m)

        out_dic[t[-1]]['time'] = measure_time(eval('wf_'+t[-1]), specTrainCond, specTrain)

        out_dic[t[-1]]['agnostic_recall'] = measure_agnostic_recall(eval('wf_'+t[-1]), specTrainCond, specTrain, t[1])

    print(out_dic)

