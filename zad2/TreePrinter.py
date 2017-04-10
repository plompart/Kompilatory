
import AST

INDENT_TOKEN = "| "


def addToClass(cls):

    def decorator(func):
        setattr(cls, func.__name__, func)
        return func
    return decorator


class TreePrinter:

    @addToClass(AST.Node)
    def printTree(self):
        raise Exception("printTree not defined in class " + self.__class__.__name__)

    @addToClass(AST.BinExpr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + self.op + "\n" + self.left.printTree(indent + 1) + self.right.printTree(indent + 1)

    @addToClass(AST.Const)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + str(self.value) + "\n"

    @addToClass(AST.AnythingList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.anythingList))

    @addToClass(AST.DeclarationsList)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "DECL\n" + "".join(map(lambda x: x.printTree(indent + 1), self.declarationsList))

    @addToClass(AST.Declaration)
    def printTree(self, indent=0):
        return self.inits.printTree(indent)

    @addToClass(AST.InitsList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.inits))

    @addToClass(AST.Init)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "=\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
               self.expression.printTree(indent + 1)

    @addToClass(AST.PrintInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "PRINT\n" + self.expressionList.printTree(indent)

    @addToClass(AST.LabeledInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "LABEL\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
               self.instruction.printTree(indent + 1)

    @addToClass(AST.Assignment)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "=\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
               self.instruction.printTree(indent + 1)

    @addToClass(AST.ChoiceInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "IF\n" + self.condition.printTree(indent + 1) + self.instruction.printTree(
            indent + 1) + \
               ("" if self.elseInstruction is None else INDENT_TOKEN * indent + "ELSE\n" +
                                                        self.elseInstruction.printTree(indent + 1))

    @addToClass(AST.WhileInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "WHILE\n" + self.condition.printTree(indent + 1) + self.instruction.printTree(
            indent + 1)

    @addToClass(AST.RepeatInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "REPEAT\n" + self.anythingList.printTree(indent + 1) + INDENT_TOKEN * indent + \
               "UNTIL\n" + self.condition.printTree(indent + 1)

    @addToClass(AST.ReturnInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "RETURN\n" + self.expression.printTree(indent + 1)

    @addToClass(AST.CompoundInstruction)
    def printTree(self, indent=0):
        return "" if self.anythingList is None else self.anythingList.printTree(indent)

    @addToClass(AST.InBracesExpression)
    def printTree(self, indent=0):
        return self.expression.printTree(indent)

    @addToClass(AST.FuncDeclarationsExpr)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FUNCALL\n" + INDENT_TOKEN * (indent + 1) + str(self.funcName) + "\n" + \
               self.arguments.printTree(indent)

    @addToClass(AST.ExpressionList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent + 1), self.expressionList))

    @addToClass(AST.FuncDefinition)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "FUNDEF\n" + INDENT_TOKEN * (indent + 1) + str(self.id) + "\n" + \
               INDENT_TOKEN * (indent + 1) + "RET " + str(self.type) + "\n" + self.arguments.printTree(indent + 1) + \
               self.compoundInstruction.printTree(indent + 1)

    @addToClass(AST.ArgumentsList)
    def printTree(self, indent=0):
        return "".join(map(lambda x: x.printTree(indent), self.argumentsList))

    @addToClass(AST.Argument)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "ARG " + self.id + "\n"

    @addToClass(AST.BreakInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "BREAK\n"

    @addToClass(AST.ContinueInstruction)
    def printTree(self, indent=0):
        return INDENT_TOKEN * indent + "CONTINUE\n"

    @addToClass(AST.Program)
    def printTree(self, indent=0):
        print "jestem 2"
        return "" if self.anythingList is None else self.anythingList.printTree(indent)
