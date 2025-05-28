# Boolean Algebra modules (Work in progress)
Modules to help with problems relating to boolean algebra and digital circuit design (calculating Gate Input Cost, boolean simplification, printing truth tables, SOP/POS form, prime implicants etc). 

Example usage is shown in `main.py`.
Requires 0 external libraries or packages. 


- `set_complement`: Takes in a string that will be used as the complement (logical NOT) symbol. Default complement is set to `'`.

**boolean_expression**
- `__init__`: Takes in a boolean equation in string form, where '+' is used for OR, placing literals/terms next to each other is used to AND them, and a character of the user's choice can be used to complement a literal or term (i.e. A+(BC)', where ' is used to complement). The equation can have an arbitrary number of variables. Function parameters must be a single alphabetical character, lowercase and uppercase are both fine. Using '0' or '1' will implicitly use them as their truth values (i.e. passing in "A+1" will always evaluate to true/1).
- `print_summary`: Prints the truth table, min and max terms, *simplified* Sum of Products (SOP) form, *simplified* Product of Sums (POS) form and Gate Input Cost (GIC) of the expression => does everything listed below (except evaluate), basically all you need. 
- `evaluate`: Evaluates the expression, inputs must be given in as a single string in the form `"A=1,B=0,C=1"`, *all* parameters need to be assigned a value.
- `truth_table`: Prints the truth table for the expression.
- `min_max_terms`: Returns the min and max terms of the function.
- `SOP_form`: Returns the *simplified* SOP form of the expression, as a string. 
- `POS_form`: Returns the *simplified* POS form of the expression, as a string.
- `GIC`: Returns the GIC of the (original) expression.



**boolean_terms**
(To be added later)



**Additional notes**
- Functionality to accomodate for multi-character parameters will be added later.
- `SOP_form` and `POS_form` have significantly slower runtimes for equations with more than 9-10 different parameters, due to the exponential time complexity of the Quine McCluskey algorithmn.
- Whitespace will automatically be removed from all input strings.
