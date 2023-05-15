from Engine import Engine
from LogicalExpression import LogicalExpression

class DPLL(Engine):
    def __init__(self):
        super().__init__()

    def solve(self):
        exp = LogicalExpression("(a <=> (c => ~d)) & b & (b => a); c; ~f || g")
        exp = self.convert_to_cnf(exp)
        exp.print_info()

    def convert_to_cnf(self, expression):
        # print("Type of Expression:", type(expression))
        if expression.symbol is not None:
            return expression
        elif expression.connective == "<=>":
            new_expression = LogicalExpression()
            new_expression.connective = "&"
            child1 = LogicalExpression(expression.children[0].original_string)
            child2 = LogicalExpression(expression.children[1].original_string)

            new_expression.children = [child1, child2]
            print("Remove Bi-Implication: ")
            new_expression.print_info()
            return new_expression
        elif expression.connective == "=>":
            new_expression = LogicalExpression()
            new_expression.connective = "\\/"
            child1 = self.convert_to_cnf(expression.children[0])
            child2 = self.convert_to_cnf(expression.children[1])
            negate_child1 = LogicalExpression()
            negate_child1.connective = "~"
            negate_child1.children.append(child1)
            new_expression.children.append(negate_child1)
            new_expression.children.append(child2)
            print("Remove Implication: ")
            new_expression.print_info()
            return new_expression
        elif expression.connective == "~":
            if expression.children[0].symbol is not None:
                return expression
            else:
                if expression.children[0].connective == "\\/":
                    new_expression = LogicalExpression()
                    new_expression.connective = "&"
                    child1 = LogicalExpression()
                    child1.connective = "~"
                    child1.children.append(expression.children[0].children[0])
                    child2 = LogicalExpression()
                    child2.connective = "~"
                    child2.children.append(expression.children[0].children[1])
                    new_expression.children.append(child1)
                    new_expression.children.append(child2)
                    return new_expression

                elif expression.children[0].connective == "&":
                    new_expression = LogicalExpression()
                    new_expression.connective = "\\/"
                    child1 = LogicalExpression()
                    child1.connective = "~"
                    child1.children.append(expression.children[0].children[0])
                    child2 = LogicalExpression()
                    child2.connective = "~"
                    child2.children.append(expression.children[0].children[1])
                    new_expression.children.append(child1)
                    new_expression.children.append(child2)
                    return new_expression

        return expression
