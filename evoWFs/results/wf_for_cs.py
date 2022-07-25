"""
Learned Witness Functions with our approach
"""
from evoWFs.results.functions_from_pset_dsl import (
    app_i,
    index_sl,
    map_i,
    add_i,
    map_s_i,
    len_s,
    map_s,
    app_s,
)

from evoWFs.text_operators.pset_text import create_range, subset_sel, subset_sel_1, neg_int, add_f_2

def wf_substring_start(str_input, out):
    """Learned Witness Function"""
    return app_i([], index_sl(out, str_input))


def wf_substring_end(str_input, start, out): # pylint: disable=unused-argument
    """Learned Witness Function"""
    return map_i(app_i([], start), add_i(len_s(out)))


def wf_concat_first(out):
    """Learned Witness Function"""
    return map_s_i(create_range(1, len_s(out)), subset_sel_1(out, 0))


def wf_concat_second(str_input_1, out):
    """Learned Witness Function"""
    return map_s(app_s([], out), subset_sel(len_s(str_input_1), len_s(out)))


def wf_abs_pos_k(str_input, out):
    """Learned Witness Function"""
    return app_i(
        app_i([], add_f_2(add_f_2(neg_int(len_s(str_input)), add_i(-1)), add_i(out))),
        add_f_2(1, add_i(out)),
    )
