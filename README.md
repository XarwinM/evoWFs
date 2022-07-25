# Finding Witness Functions with Genetic Programming 

The goal of this repository is to learn the inverse of a given operator using genetic programming. This inverse is also often called witness function in program synthesis literature.

For the genetic learning approach we rely heavily on the deap framework (see https://deap.readthedocs.io/en/master/) 

# Setup

To install the required packages execute

``python setup.py install``

``pip install -r requirements``


# Quick Start 

With 
``python evoWFs/metrics.py``
we can evaluate learned witness functions and compare them to known witness functions. The learned witness functions are from the text domain and include operators like `Substring`. Previously learned functions in this framework can be found in `evoWFs/results/wf_for_cs.py` and evaluated with ``python evoWFs/metrics.py``.

With 

``python evoWFs/math_operators/main_math.py``

or

``python evoWFs/text_operators/main_text.py``

we can learn witness functions for operators defined and characterized in `evoWFs/text_operators/dsl_text.py` or `evoWFs/math_operators/dsl_math.py`.

# Usage

In order to learn a witness function for a new operator, we have to follow four steps. These steps are very roughly outlined below.
* Define the operator and characterize its parameters as in `evoWFs/math/dsl_math.py`
* Define a way to sample from the parameters of the operator, e.g. one small modification to the `sample_space` function in `evoWFs/spec.py`
* Define a DSL on which the evolutionary algorithm operates as e.g. in `evoWFs/math_operators/pset_math.py` 
* Combine all three parts similar to `evoWFs/math_operators/main_math.py` `evoWFs/text_operators/main_text.py` and start the learning procedure

# Evaluation and Data

The data for the training and evaluation is defined in `evoWFs/spec_new.py`. For each operator we define a `condition_creator`, e.g. `condition_creator_substring` for the `substring` operator. These are basically the generators for the training data and in many scenarios for the test data (which are of course different than the training data, but are drawn due to the same process).


# Statistics 

With 
``pygount --format=summary  evoWFs`` 
I have counted the LOC of this repository and obtained 880 LOC and

With 
``python -m pylint evoWFs --disable=E1101``
I get a score of 8.93

In total I've executed 4 tests, with 27 LOC and get a coverage of 35\% (found out by we executing `coverage report -m`).
