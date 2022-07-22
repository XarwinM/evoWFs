import random
import regex

import dsl
from dsl import *
import flashFill
from typeClasses import *

import string

# Letters, Numbers and Regeluar Expression on which we operate
# We oversample the space ' ' 
letters = string.ascii_letters + '0123456789' + ' '+ ' ' + ' '
numbers = [ e for e in range(10)] + [-e for e in range(1,10)]
UsefulRegexes = [r'\w+', r"\d+", r"\s+", r".+", r"$"]

#SPACE_DIC = {'k':  int, 'v': str, 'start': int, 'end': int, 'rr':RegexTuple}

# Parameters have a fixed, assigned type. This correspondence is describe in the SPACE_DIC dictionary
SPACE_DIC = {'k':  int, 'v': str, 'start': int, 'end': int, 'r1':t2, 'r2':t2, 'a':int, 'b':int}


#Can be deleted???
trainInput = {}
for i in range(0,70):
    trainInput[i] = ""
    for k in random.sample(range(0,len(letters)-1),random.randint(1,len(letters)-1)):
        trainInput[i] += letters[k]

def sample_space(space):
    """This function describes how to sample from a given space/type, e.g. how to sample a string
    Argument:
        space: A type like str, int or RegexTuple
    Return:
        One drawn element
    """
    if space == str:
        x = ""
        for k in random.sample(range(0,len(letters)-1),random.randint(1,len(letters)-1)):
            x += letters[k]
        return x

    if space == int:
        numbers = [ e for e in range(10)] + [-e for e in range(1,10)]
        return random.sample(numbers,1)[0]
    elif space == RegexTuple:
        #regex_set = [RegexTuple(TypeRegex(r'\+s'), TypeRegex(r'\w+')) ,RegexTuple(TypeRegex(r''), TypeRegex(r'\w+')),
        #    RegexTuple(TypeRegex(r''), TypeRegex(r'\s+')), RegexTuple(TypeRegex(r'\w+'), TypeRegex(r''))]
        #regex_set = [  RegexTuple(TypeRegex(r''), TypeRegex(r'\w+'))]#, RegexTuple(TypeRegex(r''), TypeRegex(r''))]
        #return random.sample(regex_set,1)[0]
        regex_set = [ TypeRegex(r) for r in UsefulRegexes]#[TypeRegex(r'\w+'), TypeRegex(r'') ,TypeRegex(r'\s+'), TypeRegex(r'\d+') ,TypeRegex(r'^')]
        r1 = random.sample(regex_set,1)[0]
        r2 = random.sample(regex_set,1)[0]
        return RegexTuple(r1,r2)
    elif space == t2:
        regex_set = [ t2(r) for r in UsefulRegexes]#[TypeRegex(r'\w+'), TypeRegex(r'') ,TypeRegex(r'\s+'), TypeRegex(r'\d+') ,TypeRegex(r'^')]
        r1 = random.sample(regex_set,1)[0]
        return r1

#def data_create(operator, inputs, condtions, n_samples=50):
def data_create(operator, parameters, n_samples=25):
    """ Creates a training set of n_samples input-output samples. Input-outputs are described via a dictionary. The key 'out' denotes the output. Inputs to the operator are described via parameters, e.g. 'k', 'x'.
    Arguments:
        operator: operator/function to create input-output samples,
        parameters:
        n_samples: Amount of input-output samples to create

    Return:
        specTrainCond: A dictionary with keys 0,1,...,n_samples where each value describes a full set of input-output of the operator. Note that the input-output set is described via a dictionary where each parameter is key to a corresponding value
    """
    #specTrain= {}
    specTrainCond = {}
    for i in range(n_samples):
        # Add random process
        #specTrainCond[i] = { 'x': sample_space(space_dic[ , 'k':  }
        #'''
        specTrainCond[i] =  {}
        for p in parameters:
            specTrainCond[i][p] = sample_space(SPACE_DIC[p])
        #if specTrainCond[i][

        specTrainCond[i]['out'] = operator(**specTrainCond[i]  )
        #'''
        '''
        For Regex operators???
        a =True
        while a: 
            specTrainCond[i] =  {}
            for p in parameters:
                specTrainCond[i][p] = sample_space(SPACE_DIC[p])

            specTrainCond[i]['out'] = operator(**specTrainCond[i]  )
            if specTrainCond[i]['out'] != - 10:
                a =False
        '''
        #specTrainAbsPos[i] = dsl.absPos(**specTrainAbsPosCond[i]  ) 
    return specTrainCond 

def create_conditions(spec_train_cond, 
        wf_parameter='k', 
        condi_params=[]):
    """ 
    Arguments:
        spec_train_cond: Training set to learn Witness Function, 
        wf_parameter: parameter (described as string) for which we aim to learn the Witness Function,
        condi_params: list of parameters (described as strings) on which we condition the Witness Function 
    Return:
        spec_train_param: Dictionary of training instances, where each training instance consists of a single key-value dictionary with 'key' wf_parameter and as 'value' its corresponding value. 
        spec_train_cond: Input Training set with certain information removed; Data about wf_parameter and condi_params has been deleted 
    """
    spec_train_param ={}
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


