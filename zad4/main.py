import sys
import ply.yacc as yacc
from Cparser import Cparser
from TypeChecker import TypeChecker
from Interpreter import Interpreter
from TreePrinter import TreePrinter


if __name__ == '__main__':

    try:
        filename = sys.argv[1] if len(sys.argv) > 1 else "example.txt"
        file = open(filename, "r")
    except IOError:
        print("Cannot open {0} file".format(filename))
        sys.exit(0)

    Cparser = Cparser()
    parser = yacc.yacc(module=Cparser)
    text = file.read()
    ast = parser.parse(text, lexer=Cparser.scanner)
    if ast.isValid:
        typeChecker = TypeChecker()
        typeChecker.visit(ast)
        if typeChecker.isValid:
            ast.accept(Interpreter())
        else:
            print "Type check failed!\n"
    else:
        print "Synthax check failed!\n"
