#!/usr/bin/python


class Symbol():
    pass

class LabeledSymbol(Symbol):
    def __init__(self, name):
        self.name = name

class VariableSymbol(Symbol):
    def __init__(self, name, type):
        self.name = name
        self.type = type


class FunctionSymbol(Symbol):
    def __init__(self, name, type, table):
        self.name = name
        self.type = type
        self.arguments = []
        self.table = table

    #def extractParams(self):
    #    self.arguments = [x.type for x in self.table.entries.values()]


class SymbolTable(object):
    def __init__(self, parent, name): # parent scope and symbol table name
        self.parent = parent
        self.name = name
        self.entries = {}

    def put(self, name, symbol): # put variable symbol or fundef under <name> entry
        self.entries[name] = symbol

    def get(self, name): # get variable symbol or fundef from <name> entry
        try:
            ret = self.entries[name]
            return ret
        except:
            return None

    def getParentScope(self):
        return self.parent

    def pushScope(self, name):
        pass

    def popScope(self):
        pass

    def getGlobal(self, name):
        if self.get(name) is None:
            if self.parent is not None:
                return self.parent.getGlobal(name)
            else:
                return None
        else:
            return self.get(name)