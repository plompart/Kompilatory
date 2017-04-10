class Node(object):
    def __str__(self):
        print "jestem 3"
        return self.printTree()


class BinExpr(Node):
    def __init__(self, op, left, right):
        self.op = op
        self.left = left
        self.right = right


class Const(Node):
    def __init__(self, value):
        self.value = value


class Integer(Const):
    pass


class Float(Const):
    pass


class String(Const):
    pass


class Variable(Node):
    pass


class AnythingList(Node):
    def __init__(self):
        self.anythingList = []

    def addAnything(self, anything):
        self.anythingList.append(anything)


class DeclarationsList(Node):
    def __init__(self):
        self.declarationsList = []

    def addDeclaration(self, declaration):
        self.declarationsList.append(declaration)


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class InitsList(Node):
    def __init__(self):
        self.inits = []

    def addInit(self, init):
        self.inits.append(init)


class Init(Node):
    def __init__(self, id, expression):
        self.id = id
        self.expression = expression


class PrintInstruction(Node):
    def __init__(self, expressionList):
        self.expressionList = expressionList


class LabeledInstruction(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class Assignment(Node):
    def __init__(self, id, instruction):
        self.id = id
        self.instruction = instruction


class ChoiceInstruction(Node):
    def __init__(self, condition, instruction, elseInstruction):
        self.condition = condition
        self.instruction = instruction
        self.elseInstruction = elseInstruction


class WhileInstruction(Node):
    def __init__(self, condition, instruction):
        self.condition = condition
        self.instruction = instruction


class RepeatInstruction(Node):
    def __init__(self, anythingList, condition):
        self.anythingList = anythingList
        self.condition = condition


class ReturnInstruction(Node):
    def __init__(self, expression):
        self.expression = expression


class BreakInstruction(Node):
    pass


class ContinueInstruction(Node):
    pass


class CompoundInstruction(Node):
    def __init__(self, anythingList):
        self.anythingList = anythingList


class InBracesExpression(Node):
    def __init__(self, expression):
        self.expression = expression


class FuncDeclarationsExpr(Node):
    def __init__(self, funcName, arguments):
        self.funcName = funcName
        self.arguments = arguments


class ExpressionList(Node):
    def __init__(self):
        self.expressionList = []

    def addExpression(self, expression):
        self.expressionList.append(expression)


class FuncDefinition(Node):
    def __init__(self, type, id, arguments, compoundInstruction):
        self.type = type
        self.id = id
        self.arguments = arguments
        self.compoundInstruction = compoundInstruction


class ArgumentsList(Node):
    def __init__(self):
        self.argumentsList = []

    def addArgument(self, argument):
        self.argumentsList.append(argument)


class Argument(Node):
    def __init__(self, type, id):
        self.type = type
        self.id = id


class Program(Node):
    def __init__(self, anythingList):
        self.anythingList = anythingList
