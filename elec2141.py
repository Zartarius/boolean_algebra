complement = "\\"

def _my_bin(x, num_bits=8):
    bits = [(x >> i) & 1 for i in range(num_bits-1, -1, -1)]
    return "".join(str(bit) for bit in bits)

def _quine_mccluskey(m):
    groups = {}
    for minterm in m:
        num_1_bits = _my_bin(minterm).count("1")
        if num_1_bits in groups.keys(): groups[num_1_bits].append(minterm)
        else: groups[num_1_bits] = [minterm]
    
    pairs = []
    for num_1_bits in groups.keys():
        if (num_1_bits + 1) not in groups.keys():
            continue
        for minterm1 in groups[num_1_bits]:
            for minterm2 in groups[num_1_bits + 1]:
                if _my_bin(minterm1 ^ minterm2).count("1") != 1:
                    continue
                bits = ["_" if x != y else str(x) for x, y in zip(_my_bin(minterm1), _my_bin(minterm2))]
                bits = "".join(char for char in bits)
                pairs.append((minterm1, minterm2, bits))

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
                if expression[j] == ")": bracket_count += 1
                elif expression[j] == "(": bracket_count -= 1
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
        truth_table += " OUT\n" + ("-" * (len(self._params) * 5 + 2)) + "\n"
        
        for bits in range(2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (bits >> (len(self._params) - i - 1)) & 1
                truth_table += f" {bit} |"
                expression = expression.replace(self._params[i], str(bit))
            truth_table += f"  {int(eval(expression))}\n"
            
        print(truth_table)
    
    def min_max_terms(self):
        minterms = []
        maxterms = []
        
        for bits in range(2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (bits >> (len(self._params) - i - 1)) & 1
                expression = expression.replace(self._params[i], str(bit))
                
            if int(eval(expression)) == 0: maxterms.append(bits)
            else: minterms.append(bits)
            
        return {"minterms": tuple(minterms), "maxterms": tuple(maxterms)}
        
    def SOP_form(self):
        minterms = self.min_max_terms()["minterms"]
        
        
class boolean_terms:
    global complement
    
    def __init__(self, params, minterms=(), maxterms=(), dcs=(), complement=complement):
        self._params = params
        self._dcs = dcs
        self._cmpl = complement
        
        m = []
        M = []
        for i in range(2 ** len(params)):
            if i in dcs: continue
            elif len(minterms) > 0 and i in minterms: m.append(i)
            elif len(minterms) > 0 and i not in minterms: M.append(i)
            elif len(maxterms) > 0 and i in maxterms: M.append(i)
            elif len(maxterms) > 0 and i not in maxterms: m.append(i)
        
        self._m = tuple(m)
        self._M = tuple(M)
        
    def evaluate(self, inputs):
        inputs = inputs.replace(" ", "")
        inputs = inputs.split(",")
        
        decimal = 0
        for bit in inputs:
            decimal = (decimal << 1) | int(bit[1])
            
        if decimal in self._m: return 1
        elif decimal in self._M: return 0
        else: return None
        
    def min_max_terms(self):
        return {"minterms": self._m, "maxterms": self._M, "don't cares": self._dcs}
        
    def truth_table(self):
        truth_table = ""
        for param in self._params:
            truth_table += f" {param} |"
        truth_table += " OUT\n" + ("-" * (len(self._params) * 5 + 2)) + "\n"
        
        for bits in range(2 ** len(self._params)):
            for i in range(len(self._params)):
                bit = (bits >> (len(self._params) - i - 1)) & 1
                truth_table += f" {bit} |"
            if bits in self._m: truth_table += "  1\n"
            elif bits in self._M: truth_table += "  0\n"
            else: truth_table += "  x\n"
        print(truth_table)

_quine_mccluskey((1,2,3))
