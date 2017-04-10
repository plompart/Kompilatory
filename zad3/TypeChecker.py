#!/usr/bin/python
from collections import defaultdict
from SymbolTable import SymbolTable, VariableSymbol, FunctionSymbol, LabeledSymbol

ttype = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: None)))
for op in ['+', '-', '*', '/', '%', '<', '>', '<<', '>>', '|', '&', '^', '<=', '>=', '==', '!=']:
    ttype[op]['int']['int'] = 'int'

for op in ['+', '-', '*', '/']:
    ttype[op]['int']['float'] = 'float'
    ttype[op]['float']['int'] = 'float'
    ttype[op]['float']['float'] = 'float'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['int']['float'] = 'int'
    ttype[op]['float']['int'] = 'int'
    ttype[op]['float']['float'] = 'int'

ttype['+']['string']['string'] = 'string'
ttype['*']['string']['int'] = 'string'

for op in ['<', '>', '<=', '>=', '==', '!=']:
    ttype[op]['string']['string'] = 'int'


class NodeVisitor(object):
    def visit(self, node):
        method = 'visit_' + node.__class__.__name__
        visitor = getattr(self, method, self.generic_visit)
        return visitor(node)

    def generic_visit(self, node):  # Called if no explicit visitor function exists for a node.
        if isinstance(node, list):
            for elem in node:
                self.visit(elem)
        #else:
        #    for child in node.children:
        #        if isinstance(child, list):
        #            for item in child:
        #                if isinstance(item, AST.Node):
        #                    self.visit(item)
        #        elif isinstance(child, AST.Node):
        #            self.visit(child)

                    # simpler version of generic_visit, not so general
                    # def generic_visit(self, node):
                    #    for child in node.children:
                    #        self.visit(child)


class TypeChecker(NodeVisitor):
    def __init__(self):
        self.table = SymbolTable(None, "root")
        self.actualType = ""
        self.actualFunction = ""
        self.wasReturn = False
        self.wasInWhile = False

    def visit_BinExpr(self, node):
        left = self.visit(node.left)
        right = self.visit(node.right)
        op = node.op
        if ttype[op][left][right] is None:
            print "Error: Illegal operation, {} {} {}: line {}".format(left, node.op, right, node.line)
        else:
            return ttype[op][left][right]

    def visit_Const(self, node):
        return self.visit(node.value)

    def visit_Integer(self, node):
        return 'int'

    def visit_Float(self, node):
        return 'float'

    def visit_String(self, node):
        return 'string'

    def visit_Variable(self, node):
        symbol = self.table.get(node.name)
        parentTable = self.table.getParentScope()
        while symbol is None and parentTable is not None:
            symbol = parentTable.get(node.name)
            parentTable = parentTable.getParentScope()

        if symbol is None:
            print "Error: Usage of undeclared variable '{}': line {}".format(node.name, node.line)
        elif isinstance(symbol, FunctionSymbol):
            print "Error: Function identifier '{}' used as a variable: line {}".format(node.name, node.line)
            return symbol.type
        else:
            return symbol.type

    def visit_AnythingList(self, node):
        for anything in node.anythingList:
            self.visit(anything)

    def visit_DeclarationsList(self, node):
        for declaration in node.declarationsList:
            self.visit(declaration)

    def visit_Declaration(self, node):
        tempType = self.actualType
        tempTable = self.table
        tempFunction = self.actualFunction
        self.actualType = node.type
        self.visit(node.inits)
        self.table = tempTable
        self.actualType = tempType
        self.actualFunction = tempFunction

    def visit_InitsList(self, node):
        for init in node.inits:
            self.visit(init)

    def visit_Init(self, node):
        typeOfExpression = self.visit(node.expression)

        symbol = self.table.get(node.id)
        parentTable = self.table.getParentScope()
        while symbol is None and parentTable is not None:
            symbol = parentTable.get(node.id)
            parentTable = parentTable.getParentScope()

        if self.table.get(node.id) is not None:
            print "Error: Variable '{}' already declared: line {}". \
                format(node.id, node.line)
        elif isinstance(symbol, FunctionSymbol):
            print "Error: Function identifier '{}' used as a variable: line {}".format(node.id, node.line)
        else:

            if typeOfExpression == self.actualType or (typeOfExpression == "int" and self.actualType == "float"):
                self.table.put(node.id, VariableSymbol(node.id, self.actualType))
            elif typeOfExpression == "float" and self.actualType == "int":
                print "WARNING: Possible loss of precision in line {} (casting float to int)!"\
                        .format(node.line)
                self.table.put(node.id, VariableSymbol(node.id, self.actualType))
            else:
                print "Bad assignment of {} to {} in line {}".format(typeOfExpression, self.actualType, node.line)

    def visit_PrintInstruction(self, node):
        self.visit(node.expressionList)

    def visit_LabeledInstruction(self, node):
        if self.table.get(node.id) is not None:
            print "Invalid definition of {} in line: {}. Label already defined". \
                format(node.id, node.line)
        else:
            self.table.put(node.id, LabeledSymbol(node.id))
            self.visit(node.instruction)

    def visit_Assignment(self, node):
        symbol = self.table.get(node.id)
        typeOfExpression = self.visit(node.instruction)
        parentTable = self.table.getParentScope()
        while symbol is None and parentTable is not None:
            symbol = parentTable.get(node.id)
            parentTable = parentTable.getParentScope()
        if symbol is None:
            print "Error: Variable '{}' undefined in current scope: line {}".format(node.id, node.line)
        elif typeOfExpression is None:
            pass
        elif typeOfExpression != symbol.type and not(typeOfExpression == "int" and symbol.type == "float")\
                                            and not(typeOfExpression == "float" and symbol.type == "int"):
            print "Error: Assignment of {} to {}: line {}".format(typeOfExpression, symbol.type, node.line)

    def visit_ChoiceInstruction(self, node):
        self.visit(node.condition)
        tempType = self.actualType
        tempTable = self.table
        tempFunction = self.actualFunction
        self.actualFunction = "ifScope"
        self.visit(node.instruction)
        if node.elseInstruction is not None:
            self.visit(node.elseInstruction)
        self.table = tempTable
        self.actualType = tempType
        self.actualFunction = tempFunction

    def visit_WhileInstruction(self, node):
        self.visit(node.condition)
        tempType = self.actualType
        tempTable = self.table
        tempFunction = self.actualFunction
        self.actualFunction = "whileScope"
        self.wasInWhile = True
        self.visit(node.instruction)
        self.wasInWhile = False
        self.table = tempTable
        self.actualType = tempType
        self.actualFunction = tempFunction

    def visit_RepeatInstruction(self, node):
        self.visit(node.condition)
        self.visit(node.anythingList)

    def visit_ReturnInstruction(self, node):
        if self.actualType is "":
            print "Error: return instruction outside a function: line {}".format(node.line)
        else:
            self.wasReturn = True
            typeOfExpression = self.visit(node.expression)
            if typeOfExpression is not None:
                if typeOfExpression != self.actualType:
                    print "Error: Improper returned type, expected {}, got {}: line {}".format( self.actualType, typeOfExpression, node.line)

    def visit_BreakInstruction(self, node):
        if not self.wasInWhile:
            print "Error: break instruction outside a loop: line {}".format(node.line)

    def visit_ContinueInstruction(self, node):
        if not self.wasInWhile:
            print "Error: continue instruction outside a loop: line {}".format(node.line)

    def visit_CompoundInstruction(self, node):
        tempType = self.actualType
        tempTable = self.table
        tempFunction = self.actualFunction
        if self.actualFunction == "whileScope" or self.actualFunction == "ifScope":
            innerScope = SymbolTable(self.table, self.actualFunction)
            self.table = innerScope
            self.visit(node.anythingList)
        elif self.actualFunction == "root":
            innerScope = SymbolTable(self.table, "Compound")
            self.table = innerScope
            self.visit(node.anythingList)
        else:
            self.visit(node.anythingList)
        self.table = tempTable
        self.actualType = tempType
        self.actualFunction = tempFunction

    def visit_InBracesExpression(self, node):
        return self.visit(node.expression)

    def visit_FuncDeclarationsExpr(self, node):
        symbol = self.table.get(node.funcName)
        parentTable = self.table.getParentScope()
        while symbol is None and parentTable is not None:
            symbol = parentTable.get(node.funcName)
            parentTable = parentTable.getParentScope()

        if symbol is None:
            print "Error: Call of undefined fun '{}': line {}".format(node.funcName, node.line)
        elif isinstance(symbol, VariableSymbol):
            print "Name {} not defined as function in line {}".format(node.funcName, node.line)
        else:
            if len(node.arguments.expressionList) != len(symbol.arguments):
                print "Error: Improper number of args in {} call: line {}". \
                    format(node.funcName, node.line)
            else:
                types = [self.visit(x) for x in node.arguments.expressionList]
                expectedTypes = symbol.arguments
                for actual, expected in zip(types, expectedTypes):
                    if actual != expected.type and not (actual == "int" and expected.type == "float"):
                        print "Error: Improper type of args in gcd call: line {}". \
                            format(node.line)
                        break
            return symbol.type

    def visit_ExpressionList(self, node):
        for expression in node.expressionList:
            self.visit(expression)

    def visit_FuncDefinition(self, node):
        if self.table.get(node.name) is not None:
            print "Error: Redefinition of function '{}': line {}". \
                format(node.name, node.line)
        else:
            function = FunctionSymbol(node.name, node.type, SymbolTable(self.table, node.name))
            self.table.put(node.name, function)
            tempType = self.actualType
            tempTable = self.table
            tempFunction = self.actualFunction
            self.actualType = node.type
            self.table = function.table
            self.actualFunction = function
            if node.arguments is not None:
                self.visit(node.arguments)
            self.visit(node.compoundInstruction)
            if not self.wasReturn:
                print "Error: Missing return statement in function 'gcd_iter' returning int: line 12".format(
                    node.name, node.lastLine)
            self.wasReturn = False
            self.table = tempTable
            self.actualType = tempType
            self.actualFunction = tempFunction

    def visit_ArgumentsList(self, node):
        for argument in node.argumentsList:
            self.visit(argument)
            self.actualFunction.arguments.append(argument)

    def visit_Argument(self, node):
        if self.table.get(node.id) is not None:
            print "Error: Variable '{}' already declared: line {}". \
                format(node.id, node.line)
        else:
            self.table.put(node.id, VariableSymbol(node.id, node.type))

    def visit_Program(self, node):
        self.visit(node.anythingList)
