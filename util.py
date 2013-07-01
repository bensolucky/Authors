import pandas as pd

# Checks if 2 authors share a affiliation word
def check_affs(list1, list2):
    for item in list1:
	if item in list2:
	    return 1
    return 0

# Checks if 2 authors share a common co-conf
def check_conf(list1, list2):
    for item in list1:
	if item in list2:
	    return 1
    return 0

# Checks if 2 authors share a common co-author
def check_coauth(list1, list2, this1, this2):
    for item in list1:
	if item in list2:
	    if item != this1 and item != this2:
	        return 1
    return 0

# This is my reader for "tab seperated files". There is probably a better way
# to print and then read list-values from pandas dataframes.
def read_tsv_of_lists(tsv_file, col_name):
    tsv = pd.read_csv(tsv_file, index_col=0, sep="\t")
    tsv[col_name] = tsv[col_name].str.replace("[", "")
    tsv[col_name] = tsv[col_name].str.replace("]", "")
    tsv[col_name] = tsv[col_name].str.replace(",", "")
    tsv[col_name] = tsv[col_name].str.split()
    return tsv

# string levenshtein distances, from an online cookbook
# Returns a value for "string similarities", lower is more similar
def leven(seq1, seq2):
    oneago = None
    thisrow = range(1, len(seq2) + 1) + [0]
    for x in xrange(len(seq1)):
        twoago, oneago, thisrow = oneago, thisrow, [0] * len(seq2) + [x + 1]
        for y in xrange(len(seq2)):
            delcost = oneago[y] + 1
            addcost = thisrow[y - 1] + 1
            subcost = oneago[y - 1] + (seq1[x] != seq2[y])
            thisrow[y] = min(delcost, addcost, subcost)
    return thisrow[len(seq2) - 1]

# Lucas wrote this function to help replace pandas values more efficiently
def dict_len(dict_var, key):
    return len(dict_var[key]) if key in dict_var else 0

# Lucas wrote this function to help replace pandas values more efficiently
def dict_move(dict_var, from_key, to_key, idx=None):
    if idx is None:
        idx = dict_var.pop(from_key)
        dict_var[to_key] = dict_var[to_key] + [idx]
    else:
        auth_idx = dict_var[from_key]
        auth_idx.remove(idx)
        if len(auth_idx) == 0:
            dict_var.pop(from_key)
        else:
            dict_var[from_key] = auth_idx
        dict_var[to_key] = dict_var[to_key] + [idx]

