import random
import regex

import dsl
from dsl import *
import flashFill
from typeClasses import *

import string


trainInput = {}

range_int = [i for i in range(100)] + [-i for i in range(100)]
import string
letters = string.ascii_letters + '0123456789' + ' '+ ' ' + ' ' + ' '  + ' ' + ' ' + ' ' + '-' + ')(' + '.'
UsefulRegexes = [r'\w+', r"\d+", r"\s+", r".+", r"$"]


def create_random_int_substr(x, cond=[]):
    if cond == []:
        return random.randint(0, len(x)-1)
    if len(cond) > 0:
        return random.randint(cond[0]+1, len(x))


def condition_creator_substring():
    x = create_random_str()
    a = create_random_int_substr(x, cond=[])
    b = create_random_int_substr(x, cond=[a])
    return {'v':x, 'start':a,'end': b}

def condition_creator_substring_2():
    x = create_random_str()[:5]
    x = x+x +x
    a = create_random_int_substr(x, cond=[])
    b = create_random_int_substr(x, cond=[a])
    return {'v':x, 'start':a,'end': b}

def create_random_str(min_length=2):

    chars = letters
    int2char = dict(enumerate(chars))
    char2int = {ch: ii for ii, ch in int2char.items()}
    x = ""
    while len(x) <= min_length:
        for k in random.sample(range(0,len(letters)-1),random.randint(1,20)):
            x += letters[k]
        if len(x) > 20:
            x = x[:random.randint(10, 20)]

    return x
def condition_creator_abspos():
    x = create_random_str()
    k = create_random_int_substr(x, cond=[])
    k *= (2*random.randint(0,1)-1)

    return {'v':x,'k':k}

def condition_creator_concat():
    x_1 = create_random_str(min_length=1)
    x_1 = x_1[:random.randint(1,len(x_1))][:10]

    x_2 = create_random_str(min_length=1)
    x_2 = x_2[:random.randint(1,len(x_2))][:10]
    return {'v' : x_1,'s' : x_2}




#SPACE_DIC = {'k':  int, 'v': str, 'start': int, 'end': int, 'rr':RegexTuple}
SPACE_DIC = {'k':  int, 'v': str, 'start': int, 'end': int, 'r1':t2, 'r2':t2, 'a':int, 'b':int}

def sample_space(space):
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
    specTrain= {}
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

def create_conditions(operator, 
        wf_parameter='k',
        condi_params=[],
        creator='condition_creator_substring',
        n_samples=50):
        #n_samples=150):

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


