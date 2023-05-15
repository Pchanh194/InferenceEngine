from Engine import Engine

class BackwardChaining(Engine):
    def __init__(self, kb, query):
        self._knowledge_base = kb
        self._query = query
        self._facts = kb.get_facts()
        self._checked = []

    def init_agenda(self, query):
        agenda = []
        agenda.append(query)
        return agenda

    def solve(self):
        # facts = "; ".join(self._facts)
        # print("Query: " + self._query)
        # print("Facts: " + facts)
        result = self.PL_BC_Entails(self._query)
        self._checked.reverse()
        entailed = ",".join(self._checked)
        yes_or_no = "Yes" if result else "No"
        print(f"{yes_or_no}: {entailed}")

    def PL_BC_Entails(self, query):
        agenda = self.init_agenda(query)

        while len(agenda) != 0:
            searching = agenda.pop()
            searching = searching.strip()
            self._checked.append(searching)

            # print(searching)

            if searching not in self._facts:
                contains_query = []
                for c in self._knowledge_base.clauses:
                    # print(f"Premise: {c.premise}, Conclusion: {c.conclusion}")
                    if c.premise is not None and searching in c.premise:
                        contains_query.append(c)
                if len(contains_query) == 0:
                    return False
                else:
                    for c in contains_query:
                        # print(c.conclusion)
                        if c.conclusion is None:
                            continue
                        for s in c.conclusion:
                            if s not in self._checked:
                                agenda.append(s)
        return True
