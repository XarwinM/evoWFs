from only_dsls import *

def wf_Substring_start(v, out):
	return app_i([], index_sl(out, v))

def wf_Substring_end(v, start, out):
	return map_i(app_i([], start), add_i(len_s(out)))

def wf_Concat_v(out):
	return map_s_i(create_range(1, len_s(out)), subset_sel_1(out, 0))

def wf_Concat_s(v, out):
	return map_s(app_s([], out), subset_sel(len_s(v), len_s(out)))

def wf_AbsPos_k(v, out):
	return app_i(app_i([], add_f_2(add_f_2(neg_int(len_s(v)), add_i(-1)), add_i(out))), add_f_2(1, add_i(out)))

