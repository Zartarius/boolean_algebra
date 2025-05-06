complement = "\\"

class boolean_expression:
    global complement
        
    def __init__(self, expression, complement=complement):
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
        while inputs < (2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (inputs >> (len(self._params) - i - 1)) & 1
                truth_table += f" {bit} |"
                expression = expression.replace(self._params[i], str(bit))
            truth_table += f"  {int(eval(expression))}\n"
            inputs += 1
            
        print(truth_table)
        
s = "(A+B)\\"
f = boolean_expression(s)
f.truth_table()
