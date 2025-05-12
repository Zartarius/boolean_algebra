import boolmods

expression = "AB + (C+D)\\"
f = boolmods.boolean_expression(expression)
min_max_terms = f.min_max_terms()
print(f"Minterms: {min_max_terms["minterms"]}\nMaxterms: {min_max_terms["maxterms"]}")
f.truth_table()
SOP, POS = f.SOP_form(), f.POS_form()
print(f"Sum of Products form: {SOP}\nProduct of Sums form: {POS}")

minterms = (1,2,3,4,5,6,7)
dcs = (9, 10)
params = ('A', 'B', 'C', 'D')
g = boolean_terms(params, minterms=minterms, dcs=dcs)
g.truth_table()
