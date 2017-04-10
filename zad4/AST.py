class Node(object):
    def __str__(self):
        return self.printTree()

    def accept(self, visitor):
        return visitor.visit(self)


class BinExpr(Node):
    def __init__(self, op, left, right, line):
        self.op = op
        self.left = left
        self.right = right
        self.line = line


class Const(Node):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Variable(Node):
    def __init__(self, name, line):
        self.name = name
        self.line = line


class Integer(Const):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class Float(Const):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class String(Const):
    def __init__(self, value, line):
        self.value = value
        self.line = line


class AnythingList(Node):
    def __init__(self):
        self.children = []

    def addAnything(self, anything):
        self.children.append(anything)


class Declaration(Node):
    def __init__(self, type, inits):
        self.type = type
        self.inits = inits


class InitsList(Node):
    def __init__(self):
        self.children = []

    def addInit(self, init):
        self.children.append(init)


class Init(Node):
    def __init__(self, id, expression, line):
        self.id = id
        self.expression = expression
        self.line = line


class PrintInstruction(Node):
    def __init__(self, expressionList):
        self.expressionList = expressionList


class LabeledInstruction(Node):
    def __init__(self, id, instruction, line):
        self.id = id
        self.instruction = instruction
        self.line = line


class Assignment(Node):
    def __init__(self, id, instruction, line):
        self.id = id
        self.instruction = instruction
        self.line = line


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
    def __init__(self, expression, line):
        self.expression = expression
        self.line = line


class BreakInstruction(Node):
    def __init__(self, line):
        self.line = line


class ContinueInstruction(Node):
    def __init__(self, line):
        self.line = line


class CompoundInstruction(Node):
    def __init__(self, anythingList):
        self.anythingList = anythingList


class Condition(Node):
    def __init__(self, expression):
        self.expression = expression


class FuncDeclarationsExpr(Node):
    def __init__(self, funcName, arguments, line):
        self.funcName = funcName
        self.arguments = arguments
        self.line = line


class ExpressionList(Node):
    def __init__(self):
        self.children = []

    def addExpression(self, expression):
        self.children.append(expression)


class FuncDefinition(Node):
    def __init__(self, type, name, arguments, compoundInstruction, line, lastLine):
        self.type = type
        self.name = name
        self.arguments = arguments
        self.compoundInstruction = compoundInstruction
        self.line = line
        self.lastLine = lastLine


class ArgumentsList(Node):
    def __init__(self):
        self.children = []

    def addArgument(self, argument):
        self.children.append(argument)


class Argument(Node):
    def __init__(self, type, id, line):
        self.type = type
        self.id = id
        self.line = line


class Program(Node):
    def __init__(self, anythingList,isValid):
        self.anythingList = anythingList
        self.isValid = isValid


class Error(Node):
    def __init__(self):
        pass
