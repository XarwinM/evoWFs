"""
Module provides some functions used in the DSL in
evoWFs/text_operators/pset_text.py
"""
from evoWFs.function_creators import (
    append_f,
    len_f,
    index_f,
    add_f,
    map_f,
    ident_f,
)


app_i = append_f("app_i")
index_il = index_f("index_il")
index_sl = index_f("index_sl")
map_i = map_f("map_i")
map_s = map_f("map_s")
map_s_i = map_f("map_s_i")


len_il = len_f("len_il")
len_s = len_f("len_s")
len_sl = len_f("len_sl")

id_s = ident_f("id_s")
id_sl = ident_f("id_sl")
id_rt = ident_f("id_rt")
id_r = ident_f("id_r")
id_i = ident_f("id_i")

add_i = add_f("add_i")

app_r = append_f("app_r")
app_rt = append_f("app_rt")
app_s = append_f("app_s")
