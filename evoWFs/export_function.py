def export_signature(signature):

    ## Signature Creation
    signature.getWFInput()[0].__name__
    signature_out = []
    for s in signature.getWFInput():
        signature_out.append(s)

    signature_out.append(signature.getWFOutput())
    return signature_out

def function_to_str(function, input_vars, name='', parameter=''):

    arguments = ""
    for k in input_vars:
        arguments += k + ", "
    arguments = arguments[:-2]

    out = "def wf_{2}_{3}({0}):\n\treturn {1}\n\n".format(arguments, function.__str__(), name, parameter)
    return out


def create_wf_file(wf_function, file_name='wf_for_cs.py'):

    preamble = "from only_dsls import *\n\n" 

    out =preamble+ wf_function


    with open(file_name, 'w') as file:
        file.write(out)
