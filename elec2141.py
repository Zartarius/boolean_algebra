complement = "\\"

def _my_bin(x, num_bits=4):
    bits = [(x >> i) & 1 for i in range(num_bits-1, -1, -1)]
    return "".join(str(bit) for bit in bits)

def _gen_prime_implicants(groups):
    base_case = True
    new_groups = {i: [] for i in range(max(groups.keys())+1)}
    checked = set()

    for group in range(max(groups.keys())):
        for b1 in groups[group]:
            for b2 in groups[group+1]:
                if sum(1 if x != y else 0 for x, y in zip(b1[-1], b2[-1])) != 1:
                    continue
                base_case = False
                new_bits = ["-" if x != y else x for x, y in zip(b1[-1], b2[-1])]
                new_bits = "".join(bit for bit in new_bits)
                new_group = tuple(sorted(b1[:-1] + b2[:-1]) + [new_bits])

                checked.add(tuple(sorted(b1[:-1])))
                checked.add(tuple(sorted(b2[:-1])))
                
                if new_group not in new_groups[new_bits.count("1")]:
                    new_groups[new_bits.count("1")].append(new_group)

    if base_case is True:
        return sum(groups.values(), start=[])
    
    p_implicants = []
    for group in groups.values():
        for minterms in group:
            if tuple(sorted(minterms[:-1])) not in checked:
                p_implicants.append(minterms)

    return p_implicants + _gen_prime_implicants(new_groups)


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
        groups = {i: [] for i in range(len(self._params)+1)}

        for m in minterms:
            bin_str = _my_bin(m, num_bits=len(self._params))
            groups[bin_str.count("1")].append((m, bin_str))
        
        print(f"\nResult: {_gen_prime_implicants(groups)}")
        
        
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

s = "ABC+ABC\\"
f = boolean_expression(s)
f.SOP_form()














'''
def _quine_mccluskey(m, dcs):
    groups = {}
    for term in m:
        num_1_bits = _my_bin(term).count("1")
        if num_1_bits not in groups.keys(): groups[num_1_bits] = [term]
        else: groups[num_1_bits].append(term)

    paired_groups = {}
    group_num = 0
    for num_1_bits in sorted(groups.keys()):
        if (num_1_bits + 1) not in groups.keys():
            continue
        for m1 in groups[num_1_bits]:
            for m2 in groups[num_1_bits + 1]:
                if _my_bin(m1 ^ m2).count("1") != 1:
                    continue
                bits = ["-" if x != y else str(x) for x, y in zip(_my_bin(m1), _my_bin(m2))]
                bits = "".join(char for char in bits)

                if group_num in paired_groups.keys(): paired_groups[group_num].append((m1, m2, bits))
                else: paired_groups[group_num] = [(m1, m2, bits)]
        group_num += 1

    p_implicants = []
    for group_num in range(len(paired_groups.keys())-1):
        for m11, m12, bits1 in paired_groups[group_num]:
            for m21, m22, bits2 in paired_groups[group_num + 1]:
                if bits1.find("-") != bits2.find("-"):
                    continue
                new_bits = ["-" if x != y else x for x, y in zip(bits1, bits2)]
                new_bits = "".join(char for char in new_bits)
                if new_bits.find("-") != 2:
                    continue

                new_p_implicant = (m11, m12, m21, m22, new_bits)
                if _unique_tuple(new_p_implicant, p_implicants):
                    p_implicants.append(new_p_implicant)
                
    print(p_implicants)
    
    groups = {}
    for term in (m + dcs):
        num_1_bits = _my_bin(term).count("1")
        if num_1_bits in groups.keys(): groups[num_1_bits].append(term)
        else: groups[num_1_bits] = [term]

    p_implicants = []
    paired_groups = {}
    group_num = 0
    for num_1_bits in sorted(groups.keys()):
        print(groups[num_1_bits])
        if (num_1_bits + 1) not in groups.keys():
            continue
        for minterm1 in groups[num_1_bits]:
            for minterm2 in groups[num_1_bits + 1]:
                if _my_bin(minterm1 ^ minterm2).count("1") != 1:
                    continue
                bits = ["_" if x != y else str(x) for x, y in zip(_my_bin(minterm1), _my_bin(minterm2))]
                bits = "".join(char for char in bits)

                if group_num in paired_groups.keys(): paired_groups[group_num].append((minterm1, minterm2, bits))
                else: paired_groups[group_num] = [(minterm1, minterm2, bits)]
        group_num += 1

    for group_num in range(len(paired_groups.keys())-1):
        for m11, m12, bits1 in paired_groups[group_num]:
            for m21, m22, bits2 in paired_groups[group_num + 1]:
                if bits1.find("_") != bits2.find("_"):
                    continue
                new_bits = ["_" if x != y else x for x, y in zip(bits1, bits2)]
                new_bits = "".join(char for char in new_bits)
                p_implicants.append((m11, m12, m21, m22, new_bits))

    print(p_implicants)
    '''
