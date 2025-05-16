COMPLEMENT = "'"

def set_complement(complement):
    global COMPLEMENT
    COMPLEMENT = complement

def _my_bin(x, num_bits):
    bits = [(x >> i) & 1 for i in range(num_bits-1, -1, -1)]
    return "".join(str(bit) for bit in bits)

def _flatten_matrix(matrix):
    return [x for row in matrix for x in row]

def _gen_prime_implicants(groups, max_bits):
    new_groups = {group_num: [] for group_num in range(max_bits+1)}
    checked = set()

    for group in range(max_bits):
        for implicants1 in groups[group]:
            for implicants2 in groups[group+1]:
                if [(x, y) for x, y in zip(implicants1[-1], implicants2[-1]) if x != y] != [("0", "1")]: 
                    continue
                new_bits = ["-" if x != y else x for x, y in zip(implicants1[-1], implicants2[-1])]
                new_bits = "".join(bit for bit in new_bits)
                new_group = tuple(sorted(implicants1[:-1] + implicants2[:-1]) + [new_bits])

                checked.add(tuple(sorted(implicants1[:-1])))
                checked.add(tuple(sorted(implicants2[:-1])))
                
                group_num = new_bits.count("1")
                if new_group not in new_groups[group_num]:
                    new_groups[group_num].append(new_group)

    if not checked:
        return _flatten_matrix(groups.values())
    
    prime_implicants = []
    for implicants in _flatten_matrix(groups.values()):
        if tuple(sorted(implicants[:-1])) not in checked:
            prime_implicants.append(implicants)

    return prime_implicants + _gen_prime_implicants(new_groups, max_bits)


def _gen_ess_implicants(implicant_chart):
    if all(len(row) == 0 for row in implicant_chart.values()):
        return []

    ess_implicants = []
    for minterm in tuple(implicant_chart.keys()):
        if minterm in implicant_chart.keys() and len(implicant_chart[minterm]) == 1:
            ess_implicant = implicant_chart[minterm][0]
            ess_implicants.append(ess_implicant[-1])
            for covered_minterm in ess_implicant[:-1]:
                implicant_chart.pop(covered_minterm, None)
    
    rem_minterms = tuple(implicant_chart.keys())
    for i in range(len(rem_minterms)):
        if rem_minterms[i] not in implicant_chart.keys():
            continue
        row1 = implicant_chart[rem_minterms[i]]
        for j in range(i+1, len(rem_minterms)):
            if rem_minterms[j] not in implicant_chart.keys():
                continue
            row2 = implicant_chart[rem_minterms[j]]
            if set(row1) >= set(row2):
                implicant_chart.pop(rem_minterms[i])
            elif set(row2) >= set(row1):
                implicant_chart.pop(rem_minterms[j])

    colwise_implicant_chart = {prime_implicant: [] for prime_implicant in _flatten_matrix(implicant_chart.values())}
    for minterm, prime_implicants in implicant_chart.items():
        for prime_implicant in prime_implicants:
            colwise_implicant_chart[prime_implicant].append(minterm)

    rem_implicants = tuple(colwise_implicant_chart.keys())
    for i in range(len(rem_implicants)):
        col1 = colwise_implicant_chart[rem_implicants[i]]
        for j in range(i+1, len(rem_implicants)):
            col2 = colwise_implicant_chart[rem_implicants[j]]
            if set(col1) >= set(col2):
                for minterm, prime_implicants in implicant_chart.items():
                    if rem_implicants[j] in prime_implicants:
                        implicant_chart[minterm].remove(rem_implicants[j])
            elif set(col2) >= set(col1):
                for minterm, prime_implicants in implicant_chart.items():
                    if rem_implicants[i] in prime_implicants:
                        implicant_chart[minterm].remove(rem_implicants[i])
               
    return ess_implicants  + _gen_ess_implicants(implicant_chart)


class boolean_expression:     
    def __init__(self, expression, complement=None):
        global COMPLEMENT
        if complement is None:
            complement = COMPLEMENT
        self._cmpl = complement

        self._m = None
        self._M = None
        self._p_impl = None

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
            # temp.pop(i + 1)
            expression = "".join(str(char) for char in temp)
            bracket_count = int(expression[i] == ")")
            
            j = i - 1
            while bracket_count > 0:
                if expression[j] == ")": bracket_count += 1
                elif expression[j] == "(": bracket_count -= 1
                j -= 1
                
            expression = f"{expression[:j+1]}(not {expression[j+1:i+1]}){expression[i+2:]}"
            
        self._expr = expression

        temp = expression.replace("and", "").replace("or", "").replace("not", "")
        params = set([char for char in temp if char not in " ()10"])
        self._params = tuple(sorted(list(params)))
        
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
        if self._m is not None and self._M is not None:
            return {"minterms": self._m, "maxterms": self._M}
        
        minterms = []
        maxterms = []
        
        for bits in range(2 ** len(self._params)):
            expression = self._expr
            for i in range(len(self._params)):
                bit = (bits >> (len(self._params) - i - 1)) & 1
                expression = expression.replace(self._params[i], str(bit))
                
            if int(eval(expression)) == 0: maxterms.append(bits)
            else: minterms.append(bits)

        self._m = tuple(minterms)
        self._M = tuple(maxterms)
        return {"minterms": self._m, "maxterms": self._M}
    
    def prime_implicants(self):
        if self._p_impl is None:
            minterms = self.min_max_terms()["minterms"]
            max_bits = len(self._params)
            groups = {group_num: [] for group_num in range(max_bits+1)}

            for minterm in minterms:
                bin_str = _my_bin(minterm, num_bits=max_bits)
                groups[bin_str.count("1")].append((minterm, bin_str))
            self._p_impl = _gen_prime_implicants(groups, max_bits)

        p_implicants = [p_implicant[-1] for p_implicant in self._p_impl]
        p_implicants = [
            "".join(
                param if bit == "1" else param + self._cmpl
                for bit, param in zip(p_implicant, self._params) if bit != "-"
            )
            for p_implicant in p_implicants
        ]
        sorting_key = lambda term: sum(ord(char) for char in term if char is not self._cmpl)
        p_implicants = sorted(p_implicants, key=sorting_key)

        return ", ".join(p_implicant for p_implicant in p_implicants)

    def SOP_form(self):
        minterms = self.min_max_terms()["minterms"]
        max_bits = len(self._params)
        groups = {group_num: [] for group_num in range(max_bits+1)}

        for minterm in minterms:
            bin_str = _my_bin(minterm, num_bits=max_bits)
            groups[bin_str.count("1")].append((minterm, bin_str))
        
        p_implicants = _gen_prime_implicants(groups, max_bits)
        if self._p_impl is None:
            self._p_impl = p_implicants

        implicant_chart = {minterm: [] for minterm in minterms}

        for p_implicant in p_implicants:
            for minterm in p_implicant[:-1]:
                implicant_chart[minterm].append(p_implicant) 

        ess_implicants = _gen_ess_implicants(implicant_chart)

        if len(ess_implicants) == 0:
            return "0"
        elif "1" not in ess_implicants[0] and "0" not in ess_implicants[0]:
            return "1"
        
        simplified_SOP = [
            "".join(
                param if bit == "1" else param + self._cmpl
                for bit, param in zip(ess_implicant, self._params) if bit != "-"
            )
            for ess_implicant in ess_implicants
        ]
        sorting_key = lambda term: sum(ord(char) for char in term if char is not self._cmpl)
        simplified_SOP = sorted(simplified_SOP, key=sorting_key)
        return "+".join(term for term in simplified_SOP)
        
    def POS_form(self):
        maxterms = self.min_max_terms()["maxterms"]
        max_bits = len(self._params)
        groups = {group_num: [] for group_num in range(max_bits+1)}

        for maxterm in maxterms:
            bin_str = _my_bin(maxterm, num_bits=max_bits)
            groups[bin_str.count("1")].append((maxterm, bin_str))
        
        p_implicants = _gen_prime_implicants(groups, max_bits)

        implicant_chart = {maxterm: [] for maxterm in maxterms}

        for p_implicant in p_implicants:
            for maxterm in p_implicant[:-1]:
                implicant_chart[maxterm].append(p_implicant) 

        ess_implicants = _gen_ess_implicants(implicant_chart)

        if len(ess_implicants) == 0:
            return "1"
        elif "1" not in ess_implicants[0] and "0" not in ess_implicants[0]:
            return "0"
        
        simplified_POS = [
            f"({"+".join(
                param if bit == "0" else param + self._cmpl
                for bit, param in zip(ess_implicant, self._params) if bit != "-"
            )})"
            for ess_implicant in ess_implicants
        ]
        sorting_key = lambda term: sum(ord(char) for char in term if char not in f"()+{self._cmpl}")
        simplified_POS = sorted(simplified_POS, key=sorting_key)
        return "".join(term for term in simplified_POS)
    
    def GIC(self):
        literals = sum(1 for char in self._expr if char in self._params or char in "01")

        unique_complements = set()
        expression = self._expr
        while "not" in expression:
            for i in range(len(expression)-3):
                if expression[i+1:i+4] == "not":
                    j = i 
                    bracket_count = 1
                    while bracket_count > 0:
                        j += 1
                        if expression[j] == ")": bracket_count -= 1
                        elif expression[j] == "(": bracket_count += 1
                    unique_complements.add(expression[i:j+1])
                    expression = (expression[:i+1] + expression[i+4:])
        unique_complements = len(unique_complements)

        terms = 0

        return literals + unique_complements + terms
                


class boolean_terms:
    global COMPLEMENT
    
    def __init__(self, params, minterms=(), maxterms=(), dcs=(), complement=COMPLEMENT):
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
            else: truth_table += "  -\n"
        print(truth_table)
