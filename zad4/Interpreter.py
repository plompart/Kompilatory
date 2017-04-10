import AST
import SymbolTable
from Memory import *
from Exceptions import *
from visit import *
import sys

sys.setrecursionlimit(10000)

ops = {"+": (lambda x, y: x + y),
       "-": (lambda x, y: x - y),
       "*": (lambda x, y: x * y),
       "/": (lambda x, y: x / y),
       "%": (lambda x, y: x % y),
       "|": (lambda x, y: x | y),
       "&": (lambda x, y: x & y),
       "^": (lambda x, y: x ^ y),
       "==": (lambda x, y: x == y),
       "!=": (lambda x, y: x != y),
       ">": (lambda x, y: x > y),
       "<": (lambda x, y: x < y),
       "<=": (lambda x, y: x <= y),
       ">=": (lambda x, y: x >= y),
       "<<": (lambda x, y: x << y),
       ">>": (lambda x, y: x >> y)}


class Interpreter(object):
    def __init__(self):
        self.globalStack = MemoryStack()
        self.funcStack = FunctionStack()
        self.isFunction = False

    @on('node')
    def visit(self, node):
        pass

    @when(AST.BinExpr)
    def visit(self, node):
        r1 = node.left.accept(self)
        r2 = node.right.accept(self)
        return ops[node.op](r1, r2)

    @when(AST.Variable)
    def visit(self, node):
        if self.funcStack.get(node.name) is None:
            if len(self.funcStack.stack) != 0:
                funcName = self.funcStack.stack[-1].name
                return self.globalStack.get_global_value(funcName, node.name)
            else:
                return self.globalStack.get(node.name)
        else:
            return self.funcStack.get(node.name)

    @when(AST.Integer)
    def visit(self, node):
        return int(node.value)

    @when(AST.Float)
    def visit(self, node):
        return float(node.value)

    @when(AST.String)
    def visit(self, node):
        return node.value

    @when(AST.AnythingList)
    def visit(self, node):
        for anything in node.children:
            anything.accept(self)

    @when(AST.Declaration)
    def visit(self, node):
        node.inits.accept(self)

    @when(AST.InitsList)
    def visit(self, node):
        for init in node.children:
            init.accept(self)

    @when(AST.Init)
    def visit(self, node):
        expression = node.expression.accept(self)
        if self.funcStack.get_last_memory() is None:
            self.globalStack.insert(node.id, expression)
        else:
            self.funcStack.insert(node.id, expression)
        return expression

    @when(AST.PrintInstruction)
    def visit(self, node):
        print node.expressionList.accept(self)

    @when(AST.LabeledInstruction)
    def visit(self, node):
        node.instruction.accept(self)

    @when(AST.Assignment)
    def visit(self, node):
        instruction = node.instruction.accept(self)
        if self.funcStack.get(node.id) is None:
            if len(self.funcStack.stack) > 0:
                funcName = self.funcStack.stack[-1].name
                self.globalStack.set_global_value(funcName, node.id, instruction)
            else:
                self.globalStack.set(node.id, instruction)
        else:
            self.funcStack.set(node.id, instruction)
        return instruction

    @when(AST.ChoiceInstruction)
    def visit(self, node):
        if node.condition.accept(self):
            return node.instruction.accept(self)
        elif node.elseInstruction:
            return node.elseInstruction.accept(self)
        else:
            pass

    @when(AST.WhileInstruction)
    def visit(self, node):
        while node.condition.accept(self):
            try:
                node.instruction.accept(self)
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.RepeatInstruction)
    def visit(self, node):
        i = 0
        while True:
            try:
                node.anythingList.accept(self)
                if node.condition.accept(self):
                    break
            except BreakException:
                break
            except ContinueException:
                pass

    @when(AST.ReturnInstruction)
    def visit(self, node):
        value = node.expression.accept(self)
        raise ReturnValueException(value)

    @when(AST.BreakInstruction)
    def visit(self, node):
        raise BreakException()

    @when(AST.ContinueInstruction)
    def visit(self, node):
        raise ContinueException()

    @when(AST.CompoundInstruction)
    def visit(self, node):
        if self.isFunction is False:
            compoundMemory = Memory("compound")
            self.globalStack.push(compoundMemory)
            node.anythingList.accept(self)
            self.globalStack.pop()
        else:
            self.isFunction = False
            node.anythingList.accept(self)

    @when(AST.Condition)
    def visit(self, node):
        return node.expression.accept(self)

    @when(AST.FuncDeclarationsExpr)
    def visit(self, node):
        fun = self.globalStack.get(node.funcName)
        funMemory = Memory(node.funcName)
        for argExpr, actualArg in zip(node.arguments.children, fun.arguments.children):
            funMemory.put(actualArg.accept(self), argExpr.accept(self))
        self.funcStack.push(funMemory)
        try:
            self.isFunction = True
            fun.compoundInstruction.accept(self)
        except ReturnValueException as e:
            return e.value
        finally:
            self.funcStack.pop()

    @when(AST.ExpressionList)
    def visit(self, node):
        for expression in node.children:
            expression.accept(self)

    @when(AST.FuncDefinition)
    def visit(self, node):
        self.globalStack.insert(node.name, node)

    @when(AST.ArgumentsList)
    def visit(self, node):
        for argument in node.children:
            argument.accept(self)

    @when(AST.Argument)
    def visit(self, node):
        return node.id

    @when(AST.Program)
    def visit(self, node):
        node.anythingList.accept(self)

    @when(AST.Error)
    def visit(self, node):
        pass
