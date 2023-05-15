class KnowledgeBase:
    def __init__(self, clauses):
        self._clauses = clauses

    @property
    def clauses(self):
        return self._clauses

    def get_symbols(self):
        symbol_list = []
        for c in self._clauses:
            # if there is a premise in clause
            # print(f"KnowledgeBase: \n Premise: {c.premise}, Conclusion: {c.conclusion}")
            if c.conclusion is not None:
                for s in c.conclusion:
                    # checks if symbol list already has the symbol
                    if s not in symbol_list:
                        symbol_list.append(s)
            # checks if symbol list already contains the conclusion
            if isinstance(c.premise, list):
                for s in c.premise:
                    if s not in symbol_list:
                        symbol_list.append(s)
            elif c.premise not in symbol_list:
                symbol_list.append(c.premise)
        return symbol_list

    def get_facts(self):
        symbol_list = []
        for c in self._clauses:
            if c.conclusion is None:
                if isinstance(c.premise, list):
                    for s in c.premise:
                        symbol_list.append(s)
                else:
                    symbol_list.append(c.premise)
        return symbol_list
