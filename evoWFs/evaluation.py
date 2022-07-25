"""
Module contains evaluation function necessary for optimization
algorithm in deap.
With the evaluation we assign a loss-value to a function.
The deap-framework aims to find a function with minimal loss
employing evolutionary algorithms.
"""


class Signature:
    """A class that describes the 'signature' of a witness function,
    i.e. the input type, the output type and the parameters.
    Arguments:
        input_types_dic: A dictionary with parameters as keys and corresponding types as values,
        parameter: String that describes parameters of function,
        wf_out_type: Type of Witness Function output
    """

    def __init__(self, input_types_dic, wf_out_type, parameter):

        self.parameter = parameter

        self.out_type_wf = wf_out_type

        # Dictionary that describes the types of all inputs
        input_types_wf = input_types_dic.copy()
        self.input_types_wf = input_types_wf

    def get_wf_input(self):
        """
        Returns a list of types. The types describe the input-types to the Witness Function
        """
        wf_input = []
        for input_type in self.input_types_wf.values():
            wf_input.append(input_type)
        return wf_input

    def get_wf_output(self):
        """
        Return type of Witness Function Output
        """
        return self.out_type_wf

    def arg_set(self):
        """
        Returns a dictionary with keys 'Arg{i}' and values parameters
        The dictionary describes the types of the inputs to the witness function
        """
        arg_set = {}
        for i, j in enumerate(self.input_types_wf.keys()):
            arg_set["ARG{}".format(i)] = j
        return arg_set


class Evaluation:
    """Class to evaluate a candidate program
    Arguments:
        learned_wfs: A list of learned Witness Functions for a given operator.
            Usually the list is empty in the beginning.
        parameter: Parameter of learned witness function (given an output and conditions,
            we aim to find possible inputs for this parameter)
        spec_train_cond: Input-Output examples for the witness function,
        spec_train: all training data, i.e. all inputs to operator and its outputs,
        operator: Function/Operator for which we learn Witness Function
        length_weight: Weight of how strongly a lengthy function is punished
        length_output_weight: Witness Functions return a set.
            This factor punishes large output sets of the witness function
        toolbox: see deap
    """

    def __init__(
        self,
        learned_wfs,
        parameter=None,
        spec_train_cond=None,
        spec_train=None,
        operator=None,
        toolbox=None,
        length_weight=0.2,
        length_output_weight=0.05,
    ):
        self.learned_wfs = learned_wfs

        # Parameter for which we learn the witness function, i.e.
        # The parameter we aim to predict with the witness function
        self.parameter = parameter

        # operator for which we learn the witness function
        self.operator = operator

        self.spec_train = spec_train
        self.spec_train_cond = spec_train_cond

        # Weight of how strongly a lengthy function is punished
        self.length_weight = length_weight

        # Witness Functions return a set
        # This factor punishes large sets
        self.length_output_weight = length_output_weight

        # Toolbox to compile functions (see deap package)
        self.toolbox = toolbox

    def loss(self, witness_function):
        """
        Computes loss of witness_function on trainings data
        """

        loss_value = 0

        for instance_key in self.spec_train.keys():

            witness_out = witness_function(**self.spec_train_cond[instance_key])
            oracle = self.spec_train[instance_key][self.parameter]

            # Compute loss for training instance with key a
            loss_value += int(oracle not in witness_out)

            # Add weighted number of outputs to loss_value
            loss_value += len(witness_out) * self.length_output_weight

        return loss_value

    def eval_spec(self, individual, spec):
        """
        Compute total loss (inclusive Occam's razor) on all training data
        """
        witness_function = self.toolbox.compile(expr=individual)

        # If current witness function matches a previously learned one
        # Matching is measured whether both witness functions comply on the test set
        # If both functions matches we induce a high loss in order to encourage
        # the algorithm to learn a new witness function
        if self.wf_compare(witness_function, spec):
            return (100,)

        # If witness_function is different than previously learned ones

        # Loss of witness_function on trainings set
        loss = self.loss(witness_function)

        # Add complexity of function to loss
        # This gives an inductive bias similar to Occam's razor
        loss += len(individual) * self.length_weight

        return (loss,)

    def add_learned_wf(self, witness_function):
        """Collect newly learned witness function to previously learned ones"""
        self.learned_wfs.append(witness_function)

    def wf_compare(self, witness_function, spec):
        """
        Check whether the new function (witness_function) is the same
        as a witness function learned before. Sameness is measured whether
        both functions lead to the same result on the training set
        """

        for learned_wf in self.learned_wfs:
            index_wf_current = 0  # Index
            index_wf_old = 0
            for _, i in enumerate(spec.keys()):
                index_wf_current += 1
                witness_arg = {}
                witness_arg = self.spec_train_cond[i].copy()
                old_wf = self.toolbox.compile(expr=learned_wf)
                if witness_function(**witness_arg) == old_wf(**witness_arg):
                    index_wf_old += 1
            if index_wf_current == index_wf_old:
                return True
        return False

    def loss_learned_wfs(self):
        """Compute Loss for Learned Witness Functions"""
        loss = {}

        for learned_wf in self.learned_wfs:

            witness_function = self.toolbox.compile(expr=learned_wf)
            loss[str(learned_wf)] = self.loss(
                witness_function,
            )
        return loss
