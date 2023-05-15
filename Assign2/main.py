import sys
from LogicalExpression import LogicalExpression
from AdvancedKnowledgeBase import AdvancedKnowledgeBase
from KnowledgeBase import KnowledgeBase
from Clause import Clause
from TruthTable import TruthTable
from BackwardChaining import BackwardChaining
from ForwardChaining import ForwardChaining
from ExtendedTruthTable import ExtendedTruthTable
from DPLL import DPLL

_kb = None
_akb = None
_query = None
_engine = None

def main():
    global _kb, _akb, _query, _engine

    args = sys.argv[1:]

    if read_problem(args[1], args[0]):
        # Determines which algorithm to use for solving problem
        if args[0] == "TT":
            _engine = TruthTable(_kb, _query)
        elif args[0] == "BC":
            _engine = BackwardChaining(_kb, _query)
        elif args[0] == "FC":
            _engine = ForwardChaining(_kb, _query)
        elif args[0] == "GTT":
            _engine = ExtendedTruthTable(_akb, _query)
        elif args[0] == "DPLL":
            _engine = DPLL()
        else:
            raise ValueError("No Valid Inference Method Given")

    # Runs the selected engine.
    if _engine is None:
        print("_engine is None")
    else:
        _engine.solve()  # Runs the selected engine.

def read_problem(filename, solver):
    global _kb, _akb, _query

    text = []

    # tries to read problem file, if it can't returns false
    try:
        with open(filename, 'r') as reader:
            for _ in range(4):
                text.append(reader.readline().strip())
    except:
        print("Error: Could not read file")
        return False

    knowledge = text[1].split(';')
    knowledge = knowledge[:-1]
    clauses = []

    # If basic checking method
    if solver != "GTT" and solver != "DPLL":
        for s in knowledge:
            if "=>" in s:
                premise_symbols = []
                index = s.index("=>")
                premise = s[:index]
                conclusion = s[index + 2:].strip()
                split_premise = [premise] if "&" not in premise else premise.split('&')

                for symbol in split_premise:
                    trim = symbol.strip()
                    premise_symbols.append(trim)

                clauses.append(Clause(premise_symbols, conclusion))
            else:
                conclusion = s.strip()
                clauses.append(Clause(None, conclusion))

        _query = text[3]
        _kb = KnowledgeBase(clauses)
        return True
    # if solving method more advanced clauses
    else:
        kb = []
        for s in knowledge:
            exp = LogicalExpression(s)
            kb.append(exp)

        _akb = AdvancedKnowledgeBase(kb)
        _query = text[3]
        return True

if __name__ == "__main__":
    main()
