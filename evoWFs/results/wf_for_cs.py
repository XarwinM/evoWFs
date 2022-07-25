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


def wf_substring_start(v, out):
    return app_i([], index_sl(out, v))


def wf_substring_end(v, start, out):
    return map_i(app_i([], start), add_i(len_s(out)))


def wf_concat_v(out):
    return map_s_i(create_range(1, len_s(out)), subset_sel_1(out, 0))


def wf_concat_s(v, out):
    return map_s(app_s([], out), subset_sel(len_s(v), len_s(out)))


def wf_abs_pos_k(v, out):
    return app_i(
        app_i([], add_f_2(add_f_2(neg_int(len_s(v)), add_i(-1)), add_i(out))),
        add_f_2(1, add_i(out)),
    )
