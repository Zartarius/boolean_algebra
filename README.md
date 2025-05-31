# Boolean Algebra modules
Modules to help with problems relating to boolean algebra and digital circuit design (calculating Gate Input Cost, boolean simplification, printing truth tables, SOP/POS form, prime implicants etc). Many of the k-map solvers and boolean expression simplifiers online simplify expressions incorrectly, especially when it comes to problems with "don't care conditions", this module aims to solve that. 

Example usage is shown below, and also in `main.py`.
*Requires 0 external libraries or packages*. 


- `set_complement`: Takes in a string that will be used as the complement (logical NOT) symbol. Default complement is set to `'`.

**boolean_expression**
- `__init__`: Takes in a boolean equation in string form, where '+' is used for OR, placing literals/terms next to each other is used to AND them, and a character of the user's choice can be used to complement a literal or term (i.e. A+(BC)', where ' is used to complement). The equation can have an arbitrary number of variables. Function parameters must be a single alphabetical character, lowercase and uppercase are both fine. Using '0' or '1' will implicitly use them as their truth values (i.e. passing in "A+1" will always evaluate to true/1).
- `print_summary`: Prints the truth table, min and max terms, *simplified* Sum of Products (SOP) form, *simplified* Product of Sums (POS) form, prime implicants and Gate Input Cost (GIC) of the expression => does everything listed below (except evaluate), basically all you need. 
- `evaluate`: Evaluates the expression, inputs must be given in as a single string in the form `"A=1,B=0,C=1"`, *all* parameters need to be assigned a value.
- `truth_table`: Prints the truth table for the expression.
- `min_max_terms`: Returns the min and max terms of the function.
- `SOP_form`: Returns the *simplified* SOP form of the expression, as a string. 
- `POS_form`: Returns the *simplified* POS form of the expression, as a string.
- `prime_implicants`: Returns the prime implicants of the expression, as a string.
- `GIC`: Returns the GIC of the (original) expression.



**boolean_terms**
- `__init__`: Takes in a tuple of parameter names (type `str`) (i.e. ("A", "B", "C"). Additionally, *either* minterms or maxterms can be passed in as a tuple of type `int` (or both), default argument for both is an empty tuple => if only minterms are passed in, maxterms will be automatically deduced and vice versa. Also optionally takes in a tuple of don't care conditions, default is once again an empty tuple.
- `print_summary`: Prints the truth table, min and max terms, don't care conditions, *simplified* Sum of Products (SOP) form, *simplified* Product of Sums (POS) form and prime implicants => does everything listed below (except evaluate), basically all you need. 
- `evaluate`: Evaluates the expression, inputs must be given in as a single string in the form `"A=1,B=0,C=1"`, *all* parameters need to be assigned a value.
- `truth_table`: Prints the truth table.
- `min_max_terms`: Returns the min and max terms of the function, as well as the don't care conditions.
- `SOP_form`: Returns the *simplified* SOP form of the function, as a string. 
- `POS_form`: Returns the *simplified* POS form of the function, as a string.
- `prime_implicants`: Returns the prime implicants of the function, as a string.



**Additional notes**
- Functionality to accomodate for multi-character parameters will be added later.
- `SOP_form` and `POS_form` have significantly slower runtimes for equations with more than 9-10 different parameters, due to the exponential time complexity of the Quine McCluskey algorithmn.
- Whitespace will automatically be removed from all input strings.

# Example program

**Code**
```py
from elec2141 import *

set_complement("\\")
expression = "(AB)\\(B\\+C)+B(A\\C+AD\\)"
f = boolean_expression(expression)
f.print_summary()

print("---------------------------------------------")

minterms = (5,7,11,12,27,29)
dcs = (14,20,21,22,23)
params = ('A', 'B', 'C', 'D', 'E')
g = boolean_terms(params, minterms=minterms, dcs=dcs)
g.print_summary()
```

**Console output**
```
Summary

Truth table:
 A | B | C | D | OUT
----------------------
 0 | 0 | 0 | 0 |  1
 0 | 0 | 0 | 1 |  1
 0 | 0 | 1 | 0 |  1
 0 | 0 | 1 | 1 |  1
 0 | 1 | 0 | 0 |  0
 0 | 1 | 0 | 1 |  0
 0 | 1 | 1 | 0 |  1
 0 | 1 | 1 | 1 |  1
 1 | 0 | 0 | 0 |  1
 1 | 0 | 0 | 1 |  1
 1 | 0 | 1 | 0 |  1
 1 | 0 | 1 | 1 |  1
 1 | 1 | 0 | 0 |  1
 1 | 1 | 0 | 1 |  0
 1 | 1 | 1 | 0 |  1
 1 | 1 | 1 | 1 |  0

Minterms: 0, 1, 2, 3, 6, 7, 8, 9, 10, 11, 12, 14
Maxterms: 4, 5, 13, 15

Sum of Products form (SOP): B\+A\C+AD\
Products of Sums form (POS): (A+B\+C)(A\+B\+D\)
Prime implicants: B\, A\C, AD\, CD\
Gate Input Cost (GIC): 20
        
---------------------------------------------
Summary

Truth table:
 A | B | C | D | E | OUT
---------------------------
 0 | 0 | 0 | 0 | 0 |  0
 0 | 0 | 0 | 0 | 1 |  0
 0 | 0 | 0 | 1 | 0 |  0
 0 | 0 | 0 | 1 | 1 |  0
 0 | 0 | 1 | 0 | 0 |  0
 0 | 0 | 1 | 0 | 1 |  1
 0 | 0 | 1 | 1 | 0 |  0
 0 | 0 | 1 | 1 | 1 |  1
 0 | 1 | 0 | 0 | 0 |  0
 0 | 1 | 0 | 0 | 1 |  0
 0 | 1 | 0 | 1 | 0 |  0
 0 | 1 | 0 | 1 | 1 |  1
 0 | 1 | 1 | 0 | 0 |  1
 0 | 1 | 1 | 0 | 1 |  0
 0 | 1 | 1 | 1 | 0 |  -
 0 | 1 | 1 | 1 | 1 |  0
 1 | 0 | 0 | 0 | 0 |  0
 1 | 0 | 0 | 0 | 1 |  0
 1 | 0 | 0 | 1 | 0 |  0
 1 | 0 | 0 | 1 | 1 |  0
 1 | 0 | 1 | 0 | 0 |  -
 1 | 0 | 1 | 0 | 1 |  -
 1 | 0 | 1 | 1 | 0 |  -
 1 | 0 | 1 | 1 | 1 |  -
 1 | 1 | 0 | 0 | 0 |  0
 1 | 1 | 0 | 0 | 1 |  0
 1 | 1 | 0 | 1 | 0 |  0
 1 | 1 | 0 | 1 | 1 |  1
 1 | 1 | 1 | 0 | 0 |  0
 1 | 1 | 1 | 0 | 1 |  1
 1 | 1 | 1 | 1 | 0 |  0
 1 | 1 | 1 | 1 | 1 |  0

Minterms: 5, 7, 11, 12, 27, 29
Maxterms: 0, 1, 2, 3, 4, 6, 8, 9, 10, 13, 15, 16, 17, 18, 19, 24, 25, 26, 28, 30, 31
Don't cares: 14, 20, 21, 22, 23

Sum of Products form (SOP): B'CE+A'BCE'+ACD'E+BC'DE
Products of Sums form (POS): (B+C)(A'+E)(B+E)(C+D)(C+E)(B'+C'+D')(A+B'+C'+E')
Prime implicants: AB'C, B'CE, A'BCE', ACD'E, BC'DE

```

