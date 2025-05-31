from boolmods import *

set_complement("\\") # Optional, default complement is set to '
f = boolean_expression("(AB)\\(B\\+C)+B(A\\C+AD\\)")
f.print_summary()

minterms = (5,7,11,12,27,29)
dcs = (14,20,21,22,23)
params = ('A', 'B', 'C', 'D', 'E')
g = boolean_terms(params, minterms=minterms, dcs=dcs)
g.print_summary()
