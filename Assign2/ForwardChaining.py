from collections import deque

class ForwardChaining:
    def __init__(self, kb, query):
        self._knowledge_base = kb
        self._query = query
        self._inferred = {}

    def solve(self):
        is_true = self.PL_FC_Entails()
        path = ""
        yes_or_no = "Yes" if is_true else "No"
        if is_true:
            for key, value in self._inferred.items():
                if value:
                    path += key + ","
        print(f"{yes_or_no}: {path}")

    def init_agenda(self):
        agenda = deque()
        # print("Clauses: ", self._knowledge_base.clauses)
        for c in self._knowledge_base.clauses:
            # print(f"Premise: {c.premise}, Conclusion: {c.conclusion}")
            if c.conclusion is None:
                agenda.append(c.premise)
        # print(len(agenda))
        return agenda

    def init_count(self):
        count = {}
        for c in self._knowledge_base.clauses:
            if c.conclusion is not None:
                count[c] = len(c.conclusion)
        return count

    def init_inferred(self):
        inferred = {}
        symbols = self._knowledge_base.get_symbols()
        for symbol in symbols:
            inferred[symbol] = False
        return inferred

    def PL_FC_Entails(self):
        count = self.init_count()
        self._inferred = self.init_inferred()
        agenda = self.init_agenda()
        while agenda:
            symbol = agenda.popleft()
            if symbol == self._query:
                self._inferred[symbol] = True
                return True

            if not self._inferred[symbol]:
                self._inferred[symbol] = True
                for c in self._knowledge_base.clauses:
                    if c.conclusion is not None and symbol in c.conclusion:
                        count[c] -= 1
                        if count[c] == 0:
                            agenda.append(c.premise)
        return False
