# Finding Witness Functions with Genetic Programming 

The goal of this repository is to learn the inverse of a given operator.
This inverse is also often called witness function in program synthesis literature.
We consider inverse function that are also conditioned on values. 

# Setup

To install the required packages execute

``python setup.py install``

# Quick Start 

With 
``python evoWFs/metrics.py``
we can evaluate learned witness functions and compare them to known witness functions. The learned witness functions are from the text domain and include operators like `Substring`

With 

``python evoWFs/math_operators/main_math.py``

or

``python evoWFs/text_operators/main_text.py``

we can learn witness functions for operators defined and characterized in `evoWFs/text_operators/dsl_text.py` or `evoWFs/math_operators/dsl_math.py`.
The learned witness functions are saved to the python file ... (make them with arguments)

# Usage

In order to learn a witness function for a new operator, we have to follow three steps:
* Define the operator and characterize its parameters as in `evoWFs/math/dsl_math.py`
* Define a way to sample from the parameters of the operator, e.g. one small modification to the `sample_space` function in `evoWFs/spec.py`
* Define a DSL on which the evolutionary algorithm operates as e.g. in `evoWFs/math_operators/pset_math.py` 

# References and Statistics 
