#!/usr/bin/python
import re

from scanner import Scanner
import AST


class Cparser(object):
    def __init__(self):
        self.scanner = Scanner()
        self.scanner.build()

    tokens = Scanner.tokens

    precedence = (
        ("nonassoc", 'IFX'),
        ("nonassoc", 'ELSE'),
        ("nonassoc", 'decl'),
        ("nonassoc", 'fd'),
        ("right", '='),
        ("left", 'OR'),
        ("left", 'AND'),
        ("left", '|'),
        ("left", '^'),
        ("left", '&'),
        ("nonassoc", '<', '>', 'EQ', 'NEQ', 'LE', 'GE'),
        ("left", 'SHL', 'SHR'),
        ("left", '+', '-'),
        ("left", '*', '/', '%'),
    )

    def p_error(self, p):
        if p:
            print("Syntax error at line {0}, column {1}: LexToken({2}, '{3}')".format(p.lineno,
                                                                                      self.scanner.find_tok_column(p),
                                                                                      p.type, p.value))
        else:
            print("Unexpected end of input")

    def p_program(self, p):
        """program : anything_list"""
        anythingList = p[1]
        #if anything_list is not None:
            #print AST.Program(anything_list)
        p[0] = AST.Program(anythingList)

    def p_anything_list(self, p):
        """anything_list : anything_list anything
                         | """
        if len(p) == 3:
            p[0] = AST.AnythingList() if p[1] is None else p[1]
            p[0].addAnything(p[2])
        else:
            p[0] = AST.AnythingList()

    def p_anything(self, p):
        """anything : declarations %prec decl
                    | fundef %prec fd
                    | instruction"""

        p[0] = p[1]

    def p_declarations(self, p):
        """declarations : declarations declaration
                        | declaration"""
        if len(p) == 3:
            p[0] = AST.DeclarationsList() if p[1] is None else p[1]
            p[0].addDeclaration(p[2])
        else:
            p[0] = AST.DeclarationsList()
            p[0].addDeclaration(p[1])

    def p_declaration(self, p):
        """declaration : TYPE inits ';'
                       | error ';' """
        if len(p) == 4:
            type = p[1]
            inits = p[2]
            p[0] = AST.Declaration(type, inits)

    def p_inits(self, p):
        """inits : inits ',' init
                 | init """
        if len(p) == 4:
            p[0] = AST.InitsList() if p[1] is None else p[1]
            p[0].addInit(p[3])
        else:
            p[0] = AST.InitsList()
            p[0].addInit(p[1])

    def p_init(self, p):
        """init : ID '=' expression """
        id = p[1]
        expression = p[3]
        p[0] = AST.Init(id, expression, p.lineno(1))

    #    def p_instructions_opt(self, p):
    #        """instructions_opt : instructions
    #                            | """
    #        p[0] = None if len(p) == 1 else p[1]

    #    def p_instructions(self, p):
    #        """instructions : instructions instruction
    #                        | instruction """
    #        if len(p) == 3:
    #            p[0] = AST.InstructionsList() if p[1] is None else p[1]
    #            p[0].addInstruction(p[2])
    #        else:
    #            p[0] = AST.InstructionsList()
    #            p[0].addInstruction(p[1])


    def p_instruction(self, p):
        """instruction : print_instr
                       | labeled_instr
                       | assignment
                       | choice_instr
                       | while_instr
                       | repeat_instr
                       | return_instr
                       | break_instr
                       | continue_instr
                       | compound_instr
                       | expression ';' """
        p[0] = p[1]

    def p_print_instr(self, p):
        """print_instr : PRINT expr_list ';'
                       | PRINT error ';' """
        expressionsList = p[2]
        p[0] = AST.PrintInstruction(expressionsList)

    def p_labeled_instr(self, p):
        """labeled_instr : ID ':' instruction """
        id = p[1]
        instruction = p[3]
        p[0] = AST.LabeledInstruction(id, instruction, p.lineno(1))

    def p_assignment(self, p):
        """assignment : ID '=' expression ';' """
        id = p[1]
        expression = p[3]
        p[0] = AST.Assignment(id, expression, p.lineno(1))

    def p_choice_instr(self, p):
        """choice_instr : IF '(' condition ')' instruction  %prec IFX
                        | IF '(' condition ')' instruction ELSE instruction
                        | IF '(' error ')' instruction  %prec IFX
                        | IF '(' error ')' instruction ELSE instruction """
        condition = p[3]
        instruction = p[5]
        elseInstruction = p[7] if len(p) == 8 else None
        p[0] = AST.ChoiceInstruction(condition, instruction, elseInstruction)

    def p_while_instr(self, p):
        """while_instr : WHILE '(' condition ')' instruction
                       | WHILE '(' error ')' instruction """
        condition = p[3]
        instruction = p[5]
        p[0] = AST.WhileInstruction(condition, instruction)

    def p_repeat_instr(self, p):
        """repeat_instr : REPEAT anything_list UNTIL condition ';' """
        instructionsList = p[2]
        condition = p[4]
        p[0] = AST.RepeatInstruction(instructionsList, condition)

    def p_return_instr(self, p):
        """return_instr : RETURN expression ';' """
        expression = p[2]
        p[0] = AST.ReturnInstruction(expression, p.lineno(1))

    def p_continue_instr(self, p):
        """continue_instr : CONTINUE ';' """
        p[0] = AST.ContinueInstruction(p.lineno(1))

    def p_break_instr(self, p):
        """break_instr : BREAK ';' """
        p[0] = AST.BreakInstruction(p.lineno(1))

    def p_compound_instr(self, p):
        """compound_instr : '{' anything_list '}' """
        anythingList = p[2]
        p[0] = AST.CompoundInstruction(anythingList)

    def p_condition(self, p):
        """condition : expression"""
        p[0] = p[1]

    def p_const(self, p):
        """const : INTEGER
                 | FLOAT
                 | STRING"""
        if re.match(r"\d+(\.\d*)|\.\d+", p[1]):
            p[0] = AST.Float(p[1], p.lineno(1))
        elif re.match(r"\d+", p[1]):
            p[0] = AST.Integer(p[1], p.lineno(1))
        else:
            p[0] = AST.String(p[1], p.lineno(1))

    def p_expressionId(self, p):
        """expression : ID"""
        p[0] = AST.Variable(p[1], p.lineno(1))

    def p_expression(self, p):
        """expression : const
                      | expression '+' expression
                      | expression '-' expression
                      | expression '*' expression
                      | expression '/' expression
                      | expression '%' expression
                      | expression '|' expression
                      | expression '&' expression
                      | expression '^' expression
                      | expression AND expression
                      | expression OR expression
                      | expression SHL expression
                      | expression SHR expression
                      | expression EQ expression
                      | expression NEQ expression
                      | expression '>' expression
                      | expression '<' expression
                      | expression LE expression
                      | expression GE expression
                      | '(' expression ')'
                      | '(' error ')'
                      | ID '(' expr_list_or_empty ')'
                      | ID '(' error ')' """
        if len(p) == 2:
            value = p[1]
            p[0] = AST.Const(value, p.lineno(1))
        elif p[1] == '(':
            expression = p[2]
            p[0] = AST.InBracesExpression(expression)
        elif p[2] == '(' and p[1] != "(":
            id = p[1]
            expression = p[3]
            p[0] = AST.FuncDeclarationsExpr(id, expression, p.lineno(1))
        else:
            expression1 = p[1]
            operator = p[2]
            expression2 = p[3]
            p[0] = AST.BinExpr(operator, expression1, expression2, p.lineno(1))

    def p_expr_list_or_empty(self, p):
        """expr_list_or_empty : expr_list
                              | """
        p[0] = None if len(p) == 1 else p[1]

    def p_expr_list(self, p):
        """expr_list : expr_list ',' expression
                     | expression """
        if len(p) == 4:
            p[0] = AST.ExpressionList() if p[1] is None else p[1]
            p[0].addExpression(p[3])
        else:
            p[0] = AST.ExpressionList()
            p[0].addExpression(p[1])

        #    def p_fundefs_opt(self, p):
        #        """fundefs_opt : fundefs
        #                       | """
        #        p[0] = None if len(p) == 1 else p[1]

        #    def p_fundefs(self, p):
        #        """fundefs : fundef"""
        #        if len(p) == 3:
        #            p[0] = AST.FuncDefinitionsList() if p[1] is None else p[1]
        #            p[0].addFuncDefinition(p[2])
        #        else:
        #            p[0] = AST.FuncDefinitionsList()
        #            p[0].addFuncDefinition(p[1])

    def p_fundef(self, p):
        """fundef : TYPE ID '(' args_list_or_empty ')' compound_instr """
        if len(p) == 7:
            type = p[1]
            id = p[2]
            argumentsList = p[4]
            compoundInstruction = p[6]
            p[0] = AST.FuncDefinition(type, id, argumentsList, compoundInstruction, p.lineno(1), p.lineno(6))
        else:
            p[0] = None

    def p_args_list_or_empty(self, p):
        """args_list_or_empty : args_list
                              | """
        p[0] = None if len(p) == 1 else p[1]

    def p_args_list(self, p):
        """args_list : args_list ',' arg
                     | arg """
        if len(p) == 4:
            p[0] = AST.ArgumentsList() if p[1] is None else p[1]
            p[0].addArgument(p[3])
        else:
            p[0] = AST.ArgumentsList()
            p[0].addArgument(p[1])

    def p_arg(self, p):
        """arg : TYPE ID """
        type = p[1]
        id = p[2]
        p[0] = AST.Argument(type, id, p.lineno(1))
