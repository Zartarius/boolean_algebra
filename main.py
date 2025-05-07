from elec2141 import boolean_expression, boolean_terms

function = "AB + (C+D)\\"
f = boolean_expression(function)
terms = f.min_max_terms()
print(terms)
f.truth_table()

minterms = (1,2,3,4,5,6,7)
dcs = (9, 10)
params = ('A', 'B', 'C', 'D')
g = boolean_terms(params, minterms=minterms, dcs=dcs)
g.truth_table()
