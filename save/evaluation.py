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

from flashFill import createPset
from typeClasses import *
from dsl import *
import spec
import regex

class Signature:
    """ A class that describes the 'signature' of a function, i.e. the input type, the output type and the parameters.
    Arguments:
        inpTypesDic: A dictionary with parameters as keys and corresponding types as values 
        parameter: String that describes parameter
        wf_out_type: Type of Witness Function output
    Example:
    """

    def __init__(self, inpTypesDic, wf_out_type,  parameter):
        self.parameter = parameter
        self.inpTypesOperator = inpTypesDic #dictinary with input-types and its belonging parameters
        #self.outTypeOperator = outTypeOperator
        #### Needs to be corrected
        print("Wf out type", wf_out_type)
        self.outTypeWF =wf_out_type#RegexList#IntList #inpTypesDic[parameter] 

        inpTypesWF = inpTypesDic.copy()
        ####del inpTypesWF[parameter]
        #####inpTypesWF['out'] = self.outTypeOperator
        self.inpTypesWF = inpTypesWF 

    def getWFInput(self):
        """
            Returns a list of types. The types describe the input-types to the Witness Function
        """
        wFInput = []#self.inpTypes.copy() 
        for a in self.inpTypesWF.values():
            wFInput.append(a)
        return wFInput

    def getWFOutput(self):
        """
            Return type of Witness Function Output
        """
        return self.outTypeWF

    def argSet(self):
        """
            Returns a dictionary with keys 'Arg{i}' and values parameters 
        """
        argSet = {}
        for i, a in enumerate(self.inpTypesWF.keys()):
            argSet["ARG{}".format(i)] = a 
        return argSet


def levenshtein(s1, s2):
    if len(s1) < len(s2):
        return levenshtein(s2, s1)

    if len(s2) == 0:
        return len(s1)

    previous_row = range(len(s2) + 1)
    for i, c1 in enumerate(s1):
        current_row = [i + 1]
        for j, c2 in enumerate(s2):
            insertions = previous_row[j + 1] + 1 # j+1 instead of j since previous_row and current_row are one character longer
            deletions = current_row[j] + 1       # than s2
            substitutions = previous_row[j] + (c1 != c2)
            current_row.append(min(insertions, deletions, substitutions))
        previous_row = current_row

    return previous_row[-1]

class Evaluation:
    """Class to evaluate a candidate program
    Arguments:
        learnedWFs: A list of learned Witness Functions in 'deap'. Usually the list is empty in the beginning.
        parameter: Parameter of learned witness function (given an output and conditions, we aim to find possibile inputs for this parameter)
        specTrainCond: Input-Output examples for th conditions
        specTrain: Input-Output examples ???
        typ: Output type of learned function, i.e. output type of witness function
        operator: Function/Operator for which we learn Witness Function
        toolbox: see deap
    """

    def __init__(self, learnedWFs, parameter=None, specTrainCond=None, specTrain=None, typ=None, operator=None, toolbox=None, conditions={}, pset=None, specTrainFull=None): 
        if specTrainFull ==None:
            self.specTrainFull = specTrainCond
        else:
            self.specTrainFull = specTrainFull
        self.learnedWFs = learnedWFs
        self.parameter = parameter
        self.conditions = conditions
        self.type = typ
        self.specTrainCond = specTrainCond
        self.specTrain = specTrain
        self.lengthWeight = 0.2
        self.lengthOutputWeight=0.05
        #self.lengthWeight = 0.25
        #self.lengthWeight = 0.1
        self.operator = operator
        self.toolbox = toolbox

        self.pset = pset

    def addLearnedWF(self, WF):
        self.learnedWFs.append(WF)


    #Check whether the new function (witnessF) is the same as a function learned before
    def wFCompare(self, witnessF, spec):
        for learnedWF in self.learnedWFs:
            index1 = 0
            index2 = 0
            for i, a in enumerate(spec.keys()):
                index1 += 1
                witnessArg = {}
                witnessArg = self.specTrainCond[a].copy()
                ###witnessArg['out'] = self.specTrain[a]
                ###del witnessArg[self.parameter]
                oldWF = self.toolbox.compile(expr=learnedWF)
                if witnessF(**witnessArg) == oldWF(**witnessArg):
                    index2 +=1
            if index1 == index2:
                return True 
        return False

    def distanceVar(self, witness_out, condi, oracle ):
        summe = 0
        cond  =condi.copy()
        cond[self.parameter] = witness_out
        out = cond['out']
        del  cond['out']
        '''
        if self.type == 'int':
            summe += abs(self.operator(**cond)- oracle)
        elif self.type == 'str':
            summe += levenshtein(self.operator(**cond), oracle)
        elif self.type == 'RegexTuple':
            if self.operator(**cond) != oracle:
                summe += 1
        '''
        if self.type == IntList:
            ###unsure:
            ##if oracle not in self.operator(**cond) :
            if oracle not in witness_out:
                summe += 1
            if False:
                for w_out in witness_out:
                    cond[self.parameter] = w_out
                    if out != self.operator(**cond):
                        summe+=1.1 
        elif self.type == RegexList:
            ###unsure:
            if oracle not in witness_out:
                summe+=1
            #a = True
            #for w_out in witness_out:
            #    if oracle == w_out:
            #        a== False
            #if a:
            #    summe += 1
            #if oracle not in witness_out:
            #    summe += 1
            #import pdb
            #pdb.set_trace()
            
            '''
            for w_out in witness_out:
                cond[self.parameter] = w_out
                if out != self.operator(**cond):
                    summe+=4.2 
            '''
        elif self.type == ListString:
            if oracle not in witness_out:
                summe+=1
        else:
            print("Error: Type not defined and is necessary for evaluation")
        del cond
        return summe 

    def loss(self, witnessF, spec):
        distance=0
        for i, a in enumerate(spec.keys()):
            """
            witnessArg = {}
            witnessArg = self.specTrain[a].copy()
            witnessArg.update(self.conditions)
            """

            #witnessArg = self.specTrainCond[a].copy()
            ###witnessArg['out'] = self.specTrain[a]
            ###del witnessArg[self.parameter]
            #distance += self.distanceVar(witnessF(**witnessArg), self.specTrainCond[a], self.specTrain[a])
            distance += self.distanceVar(witnessF(**self.specTrainCond[a]), self.specTrainCond[a], self.specTrain[a][self.parameter])
            distance +=  len(witnessF(**self.specTrainCond[a]))*self.lengthOutputWeight #*0.01
        return distance 


    def evalSpec(self, individual, spec):
        global initial 
        witnessF = self.toolbox.compile(expr=individual)
        #print(individual)

        if self.wFCompare(witnessF, spec):
            return 100,
        else:
            distance = self.loss(witnessF, spec)
            distance += len(individual) * self.lengthWeight 
            return distance, 

    def lossLearnedWFs(self):
        loss ={} 
        for learnedWF in self.learnedWFs:
            a =1
#            loss[str(learnedWF)] =  self.loss(learnedWF, self.specTrain)[0] - self.lengthWeight * len(learnedWF) 
            witnessF = self.toolbox.compile(expr=learnedWF)
            loss[str(learnedWF)] =  self.loss(witnessF, self.specTrain) #- self.lengthWeight * len(learnedWF) 
        return loss 

