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
            stack = []
            if expression[i] == ")":
                stack.append(expression[i])
            
            j = i - 1
            while len(stack) > 0:
                if expression[j] == ")":
                    stack.append(expression[j])
                elif expression[j] == "(":
                    stack.pop()
                j -= 1
            expression = f"{expression[:j]} (not {expression[j+1:i+1]}){expression[i+2:]}"
            
        self._expr = expression
        
        params = []
        for char in expression:
            if char not in " ()&|~10" and char not in params:
                params.append(char)
        self._params = tuple(params)
        
    def evaluate(self, inputs):
        inputs = inputs.replace(" ", "")
        inputs = inputs.split(",")

        expression = self._expr
        print(expression)
        for param in inputs:
            expression = expression.replace(param[0], param[2])
        return int(eval(expression))
        
s = "A(BC\\ + (B+C)\\)\\"
f = boolean_expression(s)
print(f.evaluate("A=1, B=0, C=1"))


    
