# from evoWFs.only_dsls import *
from evoWFs.only_dsls import (
    app_i,
    index_sl,
    map_i,
    add_i,
    map_s_i,
    create_range,
    len_s,
    subset_sel_1,
    map_s,
    app_s,
    subset_sel,
    add_f_2,
    neg_int,
)


def wf_substring_start(str_input, out):
    return app_i([], index_sl(out, str_input))


def wf_substring_end(str_input, start, out):
    return map_i(app_i([], start), add_i(len_s(out)))


def wf_concat_v(out):
    return map_s_i(create_range(1, len_s(out)), subset_sel_1(out, 0))


def wf_concat_s(str_input_1, out):
    return map_s(app_s([], out), subset_sel(len_s(str_input_1), len_s(out)))


def wf_abs_pos_k(str_input, out):
    return app_i(
        app_i([], add_f_2(add_f_2(neg_int(len_s(str_input)), add_i(-1)), add_i(out))),
        add_f_2(1, add_i(out)),
    )
