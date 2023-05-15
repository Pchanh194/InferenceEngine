class LogicalExpression:
    def __init__(self, sentence=None):
        self._symbol = None
        self._connective = None
        self._children = []
        self._original = None

        if sentence is not None:
            self._original = sentence
            sentence = sentence.strip()
            if any(op in sentence for op in ["<=>", "=>", "&", "~", "\\/", "||"]):
                self.sentence_parser(sentence)
                print(f"New sentence: {sentence}")
            else:
                print(f"Symbol sentence: {sentence}")
                self._symbol = sentence

    @property
    def children(self):
        return self._children

    @children.setter
    def children(self, value):
        self._children = value

    def print_info(self):
        print(f"Original String: {self._original}")
        if self._symbol is None:
            if len(self._children) > 1:
                print(f"left: {self._children[0].original_string} Connective: {self._connective} right: {self._children[1].original_string}")
                for child in self._children:
                    child.print_info()
            elif len(self._children) == 1:
                self._children[0].print_info()
        else:
            print(f"Symbol: {self._symbol}")

    @property
    def connective(self):
        return self._connective

    @connective.setter
    def connective(self, value):
        self._connective = value

    @property
    def symbol(self):
        return self._symbol

    @property
    def original_string(self):
        return self._original

    def sentence_parser(self, sentence):
        bracket_counter = 0
        operator_index = -1
        trigger = True
        trigger2 = True
        sentence = sentence.strip()
        print(f"Initial Sentence: {sentence}")
        for i, c in enumerate(sentence):
            if c == '(':
                bracket_counter += 1
            elif c == ')':
                bracket_counter -= 1
            elif c == '<' and bracket_counter == 0:
                operator_index = i
                trigger = False
                trigger2 = False
            elif c == '=' and sentence[i + 1] == '>' and bracket_counter == 0 and trigger2:
                operator_index = i
                trigger = False
                trigger2 = False
            elif c == '&' and bracket_counter == 0 and trigger and trigger2:
                operator_index = i
                trigger = False
                trigger2 = False
            elif c == '||' and bracket_counter == 0 and trigger and trigger2: #check
                operator_index = i
                trigger = False
                trigger2 = False
            elif c == '\\' and bracket_counter == 0 and trigger and trigger2:
                operator_index = i
                trigger = False
                trigger2 = False
            elif c == '~' and bracket_counter == 0 and operator_index < 0 and trigger and trigger2:
                operator_index = i

        if operator_index < 0:
            sentence = sentence.strip()
            if sentence[0] == '(' and sentence[-1] == ')':
                self.sentence_parser(sentence[1:-1])
        else:
            if sentence[operator_index] == '<':
                print(f"sentence: {sentence}")
                first = sentence[:operator_index].strip()
                second = sentence[operator_index + 3:].strip()
                child1 = LogicalExpression(first)
                child2 = LogicalExpression(second)
                self._children.append(child1)
                self._children.append(child2)
                self._connective = "<=>"
            elif sentence[operator_index] == '=':
                first = sentence[:operator_index].strip()
                second = sentence[operator_index + 2:].strip()
                child1 = LogicalExpression(first)
                child2 = LogicalExpression(second)
                self._children.append(child1)
                self._children.append(child2)
                self._connective = "=>"
            elif sentence[operator_index] == '&':
                first = sentence[:operator_index].strip()
                second = sentence[operator_index + 1:].strip()
                child1 = LogicalExpression(first)
                child2 = LogicalExpression(second)
                self._children.append(child1)
                self._children.append(child2)
                self._connective = "&"
            elif sentence[operator_index:operator_index + 2] == '||':
                first = sentence[:operator_index].strip()
                second = sentence[operator_index + 2:].strip()
                child1 = LogicalExpression(first)
                child2 = LogicalExpression(second)
                self._children.append(child1)
                self._children.append(child2)
                self._connective = "||"
            elif sentence[operator_index] == '\\':
                first = sentence[:operator_index].strip()
                second = sentence[operator_index + 2:].strip()
                child1 = LogicalExpression(first)
                child2 = LogicalExpression(second)
                self._children.append(child1)
                self._children.append(child2)
                self._connective = "\\/"
            elif sentence[operator_index] == '~':
                first = sentence[operator_index + 1:].strip()
                child = LogicalExpression(first)
                self._children.append(child)
                self._connective = "~"
