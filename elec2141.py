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
        
s = "A(B\\C\\ + (B+C)\\)\\"
f = boolean_expression(s)
print(f.evaluate("A=1, B=0, C=1"))
