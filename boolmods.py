complement = "\\"

def _my_bin(x: int, num_bits: int) -> str:
    """
    Decimal to binary converter
    x - decimal to convert
    num_bits - number of bits to include, starting from LSB
    Returns the binary conversion in the form of a string
    """
    bits = [(x >> i) & 1 for i in range(num_bits-1, -1, -1)]
    return "".join(str(bit) for bit in bits)

def _flatten_matrix(matrix: list[list]) -> list:
    """
    Given a 2D matrix, returns it with all the rows concatenated into
    a list
    matrix - A list of lists
    Returns a list
    """
    return [x for row in matrix for x in row]

def _gen_prime_implicants(groups: dict[int, list], max_bits: int) -> list[tuple]:
    """
    Recursive Quine McCluskey algorithmn to find prime implicants. 
    groups - a dictionary of lists (of tuples), with keys in range 0 to max_bits+1
    max_bits - the maximum number of bits needed to represent the largest possible
    minterm, it will be equal to the number of different parameters in the boolean function
    Returns a list of tuples, where the last element of each tuple is a binary string 
    representation of the prime implicant, and the remaining elements are the minterms that
    the prime implicant is composed of
    """
    new_groups = {group_num: [] for group_num in range(max_bits+1)}
    checked = set()

    for group in range(max_bits):
        for implicants1 in groups[group]:
            for implicants2 in groups[group+1]:
                if sum(1 if x != y else 0 for x, y in zip(implicants1[-1], implicants2[-1])) != 1:
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
        max_bits = len(self._params)
        groups = {i: [] for i in range(max_bits+1)}

        for m in minterms:
            bin_str = _my_bin(m, num_bits=len(self._params))
            groups[bin_str.count("1")].append((m, bin_str))
        
        p_implicants = _gen_prime_implicants(groups, max_bits)
        print(p_implicants)
        
        
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
