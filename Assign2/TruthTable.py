from LogicalExpression import LogicalExpression

class TruthTable:
    def __init__(self, kb, query):
        self._kb = kb
        self._query = query
        self._model_count = 0

    def solve(self):
        symbols = self.create_symbol_list(self._kb.expressions, self._query)
        result = self.TT_ENTAILS(self._kb, self._query)
        print("\nYes," if result == True else "No","Model count: ", self._model_count)

    def create_symbol_list(self, kb, query):
        symbol_list = []
        running_list = []
        if query:
            symbol_list.append(query)
        for exp in kb:
            if exp.symbol is not None:
                if exp.symbol not in symbol_list:
                    symbol_list.append(exp.symbol)
            else:
                running_list = self.create_symbol_list(exp.children, None)
                for s in running_list:
                    if s not in symbol_list:
                        symbol_list.append(s)
        # print("Symbol list: ", ' '.join(symbol_list))
        return symbol_list

    def extend(self, key, val, model):
        new_model = dict(model)
        if key is not None:
            new_model[key] = val
        return new_model

    def TT_ENTAILS(self, kb, query):
        symbols = self.create_symbol_list(kb.expressions, query)
        model = {}
        return self.TT_CHECK_ALL(kb, query, symbols, model)

    def TT_CHECK_ALL(self, kb, query, symbols, model):
        if len(symbols) == 0:
            if self.IS_TRUE(kb.expressions, model):
                if self.IS_TRUE(query, model):
                    self._model_count += 1
                    return True
                else:
                    return False
            else:
                return True
        else:
            P = symbols[0]
            symbols = symbols[1:]
            return (self.TT_CHECK_ALL(kb, query, list(symbols), self.extend(P, True, model)) 
                    and self.TT_CHECK_ALL(kb, query, list(symbols), self.extend(P, False, model)))

    def IS_TRUE(self, query, model):
        if isinstance(query, str):
            return model.get(query, False)
        elif isinstance(query, LogicalExpression):
            result = True
            if query.symbol is not None:
                result = self.IS_TRUE(query.symbol, model)
            else:
                if query.connective == "&":
                    for child in query.children:
                        result = result and self.IS_TRUE(child, model)
                if query.connective == "\\/":
                    result = False
                    for child in query.children:
                        result = result or self.IS_TRUE(child, model)
                if query.connective == "=>":
                    result = not self.IS_TRUE(query.children[0], model) or self.IS_TRUE(query.children[1], model)
                if query.connective == "<=>":
                    result = self.IS_TRUE(query.children[0], model) == self.IS_TRUE(query.children[1], model)
                if query.connective == "~":
                    return not self.IS_TRUE(query.children[0], model)
                if query.connective == "||":
                    result = False
                    for child in query.children:
                        result = result or self.IS_TRUE(child, model)

            return result
        elif isinstance(query, list):  # It is a knowledge base
            final_result = True
            for exp in query:
                final_result = final_result and self.IS_TRUE(exp, model)
            return final_result
