import re

class solver:
    def __init__(self, expression, complement="\\"):
        expression = expression.replace(" ", "")
        
        temp = ""
        for i in range(len(expression)):
            if i != len(expression)-1 and expression[i] not in "+(" and expression[i+1] not in "+)":
                temp += f"{expression[i]} & "
            else: 
                temp += expression[i]
                
        expression = temp
        expression = expression.replace("+", " | ")
        print(expression)
        self._expr = expression
        
    
        
s = "A+B(C + AD)"

f = solver(s)
