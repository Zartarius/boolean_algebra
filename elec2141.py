complement = "\\"

class boolean_expression:
    global complement
        
    def __init__(self, expression=None, minterms=None, maxterms=None, dcs=None, params=None, complement=complement):
        self._m = None
        self._M = None
        
        if expression == None:
            self._expr = None
            if minterms != None:
                self._m = minterms
            else:
                self._M = maxterms
            self._params = params
            return
        
        expression = expression.replace(" ", "")
        temp = ""
        for i in range(len(expression)):
            if i != len(expression) - 1 and expression[i] not in "+(" and expression[i + 1] not in f"+){complement}":
                temp += f"{expression[i]} and "
            else: 
                temp += expression[i]
                
        expression = temp.replace("+", " or ")

        while complement in expression:
            i = len(expression) - expression[::-1].find(complement) - 2

            temp = list(expression)
            temp.pop(i + 1)
            expression = "".join(str(char) for char in temp)
            bracket_count = int(expression[i] == ")")
            
            j = i - 1
            while bracket_count > 0:
                if expression[j] == ")":
                    bracket_count += 1
                elif expression[j] == "(":
                    bracket_count -= 1
                j -= 1
                
            expression = f"{expression[:j+1]}(not {expression[j+1:i+1]}){expression[i+1:]}"
            
        self._expr = expression
        
        temp = expression.replace("and", "").replace("or", "").replace("not", "")
        params = []
        for char in temp:
            if char not in " ()&|~10" and char not in params:
                params.append(char)
        self._params = tuple(sorted(params))
        
    def evaluate(self, inputs):
        inputs = inputs.replace(" ", "")
        inputs = inputs.split(",")
        
        if self.expr == None:
            decimal = 0
            for bit in inputs:
                decimal = (decimal << 1) | int(bit[1])
            return 1 if decimal in self._m else 0

        expression = self._expr
        for param in inputs:
            expression = expression.replace(param[0], param[2])
            
        return int(eval(expression))
        
    def truth_table(self):
        truth_table = ""
        for param in self._params:
            truth_table += f" {param} |"
        truth_table += " OUT\n"
        truth_table += ("-" * (len(self._params) * 5 + 2)) + "\n"
        
        inputs = 0
        if self._expr == None:
            while inputs < (2 ** len(self._params)):
                for i in range(len(self._params)):
                    bit = (inputs >> (len(self._params) - i - 1)) & 1
                    truth_table += f" {bit} |"
                truth_table += f"  {1 if inputs in self._m else 0}\n"
                inputs += 1
            print(truth_table)
            return
            
        while inputs < (2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (inputs >> (len(self._params) - i - 1)) & 1
                truth_table += f" {bit} |"
                expression = expression.replace(self._params[i], str(bit))
            truth_table += f"  {int(eval(expression))}\n"
            inputs += 1
            
        print(truth_table)
    
    def min_max_terms(self):
        minterms = []
        maxterms = []
        
        if self._expr == None:
            for i in range(2 ** len(self._params)):
                if self._m != None and i not in self._m:
                    maxterms.append(i)
                elif self._M != None and i not in self._M:
                    minterms.append(i)
                    
            return {"minterms": self._m if self._m != None else tuple(minterms), 
                    "maxterms": self._M if self._M != None else tuple(maxterms)}
        
        inputs = 0
        while inputs < (2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (inputs >> (len(self._params) - i - 1)) & 1
                expression = expression.replace(self._params[i], str(bit))
                
            if int(eval(expression)) == 0:
                maxterms.append(inputs)
            else:
                minterms.append(inputs)
            inputs += 1
            
        return {"minterms": tuple(minterms), "maxterms": tuple(maxterms)}
        
    def SOP_form(self):
        minterms = self.min_max_terms()["minterms"]
        
        
        
s = "AB + (C+D)\\"
m = (1,2,3,4,5,6,7)
p = ('A', 'B', 'C', 'D')
f = boolean_expression(minterms=m, params=p)
terms = f.min_max_terms()
print(terms)
f.truth_table()
