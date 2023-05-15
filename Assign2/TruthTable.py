from Engine import Engine

class TruthTable(Engine):
    def __init__(self, kb, query):
        self._model_count = 0
        self._knowledge_base = kb
        self._query = query

    def create_symbol_list(self, kb, alpha):
        symbol_list = [alpha]
        for c in kb.clauses:
            if c.premise is not None:
                for s in c.premise:
                    if s not in symbol_list:
                        symbol_list.append(s)
            if c.conclusion is not None:  # check if conclusion is not None
                if isinstance(c.conclusion, list):  # check if conclusion is a list
                    for s in c.conclusion:  # iterate over symbols in the list
                        if s not in symbol_list:
                            symbol_list.append(s)
                elif c.conclusion not in symbol_list:
                    symbol_list.append(c.conclusion)
        return symbol_list


    def extend(self, key, value, model):
        new_model = model.copy()
        new_model[key] = value
        return new_model

    def solve(self):
        is_true = self.TT_entails(self._knowledge_base, self._query)
        print(f"Is True: {is_true} model count: {self._model_count}")

    def TT_entails(self, kb, alpha):
        symbols = self.create_symbol_list(kb, alpha)
        model = {}
        return self.TT_check_all(kb, alpha, symbols, model)

    def TT_check_all(self, kb, alpha, symbols, model):
        # print(';'.join(symbols))
        if len(symbols) == 0:
            # for key, value in model.items():
            #     print(f"{key}: {value}")
            
            # print(self.PL_true_from_kb(kb, model), self.PL_true(alpha, model))

            if self.PL_true_from_kb(kb, model): 
                if self.PL_true(alpha, model):
                    self._model_count += 1
                    print(self.PL_true_from_kb(kb, model), self.PL_true(alpha, model), "Count: ", self._model_count)
                    return True
                else:
                    return False
            else:
                return True
        else:
            # for key, value in model.items():
            #     print(f"{key}: {value}")
            P = symbols.pop(0)
            return self.TT_check_all(kb, alpha, symbols[:], self.extend(P, True, model)) and \
                   self.TT_check_all(kb, alpha, symbols[:], self.extend(P, False, model))

    def PL_true(self, query, model):
        if isinstance(query, list):
            return all(self.PL_true(q, model) for q in query)
        else:
            return model.get(query, False)

    def PL_true_from_kb(self, kb, model):
        final_result = True
        for c in kb.clauses:
            clause_result = True
            if c.premise is None:
                clause_result = self.PL_true(c.conclusion, model)
            else:
                premise_is_true = all(self.PL_true(symbol, model) for symbol in c.premise)
                conclusion = c.conclusion
                if isinstance(conclusion, list) and len(conclusion) == 1:
                    conclusion = conclusion[0]
                clause_result = not (premise_is_true and not self.PL_true(conclusion, model))
            final_result &= clause_result

        # print(f"model: {final_result}")
        return final_result


