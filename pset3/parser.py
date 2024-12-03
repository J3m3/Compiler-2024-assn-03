"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file implements a parser for ToyPL, which is described in our README file.
import ply.yacc as yacc
import ply.lex as lex
from lexer import *
import sys


###############################################################
# Program
###############################################################
def p_program(p):
    """
    program : namespace_decs const_decs var_decs func_decs
    """
    p[0] = ("program", p[1], p[2], p[3], p[4])


###############################################################
# Namespace
###############################################################
def p_namespace_decs(p):
    """
    namespace_decs : empty
                   | namespace_dec namespace_decs
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]


def p_namespace_dec(p):
    """
    namespace_dec : NAMESPACE NIDENT namespace_decs const_decs var_decs func_decs END
    """
    # p[1] = namespace declaration
    # p[2] = namespace name
    # p[3] = namespace declarations
    # p[4] = declared constants
    # p[5] = declared variables
    # p[6] = function declarations
    # p[7] = END keyword
    p[0] = ("namespace", p[2], p[3], p[4], p[5], p[6])


###############################################################
# Constants
###############################################################
def p_const_decs(p):
    """
    const_decs : empty
               | CONST consts
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]


def p_consts(p):
    """
    consts : LIDENT DEFINE NUMBER
           | LIDENT DEFINE NUMBER COMMA consts
    """
    if len(p) == 4:
        p[0] = [(p[1], p[3])]
    else:
        p[0] = [(p[1], p[3]), *p[5]]


###############################################################
# Variables
###############################################################
def p_var_decs(p):
    """
    var_decs : empty
             | VAR vars
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = p[2]


def p_vars(p):
    """
    vars : LIDENT
         | LIDENT COMMA vars
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], *p[3]]


###############################################################
# Functions
###############################################################
def p_func_decs(p):
    """
    func_decs : empty
              | func_dec func_decs
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]


def p_func_dec(p):
    """
    func_dec : FUNC LIDENT LPAR params RPAR const_decs var_decs BEGIN stmts END
    """
    # p[1] = func declaration
    # p[2] = func name
    # p[3] = left parenthesis token
    # p[4] = func parameters
    # p[5] = right parenthesis token
    # p[6] = declared constants: ('name', val)
    # p[7] = declared variables
    # p[8] = BEGIN keyword
    # p[9] = func statements
    # p[10] = END keyword
    p[0] = ("func", p[2], p[4], p[6], p[7], p[9])


def p_params(p):
    """
    params : empty
           | LIDENT params_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]


def p_params_tail(p):
    """
    params_tail : empty
                | COMMA LIDENT params_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[2], *p[3]]


###############################################################
# Statement definitions
###############################################################
def p_stmt_skip(p):
    """
    stmt : SKIP
    """
    p[0] = ("skip", )


def p_stmt_read(p):
    """
    stmt : ident ASSIGN READ
    """
    p[0] = ("read", p[1])


def p_stmt_print(p):
    """
    stmt : PRINT LPAR expr RPAR
    """
    p[0] = ("print", p[3])


def p_stmt_assign(p):
    """
    stmt : ident ASSIGN expr
    """
    # Check for scope
    inScope = False
    isConst = False

    for prevToken in reversed(parser.symstack):
        if prevToken.type == "var_decs": # Check for declared variables
            for prevVar in prevToken.value:
                if prevVar == p[1][2]:
                    inScope = True
        elif prevToken.type == "params": # Also check in function parameters
            for prevVar in prevToken.value:
                if prevVar == p[1][2]:
                    inScope = True
        elif prevToken.type == "const_decs": # Check for declared constants
            for prevVar in prevToken.value:
                if prevVar[0] == p[1][2]:
                    isConst = True

    if isConst:
        error_reporter("Error: {0} cannot become a l-value since it is a const variable".format(p[1][2]))
    elif not inScope:
        error_reporter("Error: {0} is not declared in this scope".format(p[1][2]))
    else:
        p[0] = ("assign", p[1], p[3])


def p_stmt_call(p):
    """
    stmt : ident ASSIGN CALL ident LPAR args RPAR
    """
    p[0] = ("call", p[1], p[4], p[6])


def p_stmt_if(p):
    """
    stmt : IF bexpr THEN stmt ELSE stmt
    """
    p[0] = ("if", p[2], p[4], p[6])


def p_stmt_while(p):
    """
    stmt : WHILE bexpr DO stmt
    """
    p[0] = ("while", p[2], p[4])


def p_stmt_return(p):
    """
    stmt : RETURN expr
    """
    p[0] = ("return", p[2])


def p_stmt_stmts(p):
    """
    stmt : LBRC stmts RBRC
    """
    p[0] = ("stmts", p[2])


def p_stmts(p):
    """
    stmts : stmt
          | stmt SEMICOLON
          | stmt SEMICOLON stmts
    """
    if len(p) == 2 or len(p) == 3:
        p[0] = [p[1]]
    else:
        p[0] = [p[1], *p[3]]


def p_args(p):
    """
    args : empty
         | expr args_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[2]]


def p_args_tail(p):
    """
    args_tail : empty
              | COMMA expr args_tail
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[2], *p[3]]


###############################################################
# Boolean expressions
###############################################################
def p_cmp_op(p):
    """
    cmp_op : EQ
           | NE
           | LT
           | LE
           | GT
           | GE
    """
    p[0] = p[1]


def p_bexpr(p):
    """
    bexpr : bterm
          | bexpr OR bterm
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("or", p[1], p[3])


def p_bterm(p):
    """
    bterm : bfactor
          | bterm AND bfactor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = ("and", p[1], p[3])


def p_bfactor_cmp(p):
    """
    bfactor : expr cmp_op expr
    """
    p[0] = (p[2], p[1], p[3])


def p_bfactor_bexpr(p):
    """
    bfactor : LPAR bexpr RPAR
    """
    p[0] = p[2]


###############################################################
# Arithmetic expressions
###############################################################
def p_expr(p):
    # EXPR ::= EXPR "+" TERM | EXPR "-" TERM | TERM
    """
    expr : term
         | expr PLUS term
         | expr MINUS term
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_term(p):
    """
    term : factor
         | term MUL factor
         | term DIV factor
         | term MOD factor
    """
    if len(p) == 2:
        p[0] = p[1]
    else:
        p[0] = (p[2], p[1], p[3])


def p_factor_ident(p):
    """
    factor : ident
    """
    p[0] = ("var", p[1])


def p_factor_number(p):
    """
    factor : NUMBER
    """
    p[0] = ("number", p[1])


def p_factor_expr(p):
    """
    factor : LPAR expr RPAR
    """
    p[0] = p[2]


###############################################################
# Identifiers
###############################################################
def p_ident_abs(p):
    """
    ident : abs_path LIDENT
    """
    p[0] = ("abs", p[1], p[2])


def p_ident_rel(p):
    """
    ident : rel_path LIDENT
    """
    p[0] = ("rel", p[1], p[2])


def p_abs_path(p):
    """
    abs_path : COLON rel_path
    """
    p[0] = p[2]


def p_rel_path(p):
    """
    rel_path : empty
             | NIDENT PERIOD rel_path
    """
    if len(p) == 2:
        p[0] = []
    else:
        p[0] = [p[1], *p[3]]


###############################################################
# Error Reporter and Handler (Panic Mode Recovery)
###############################################################
# Global variable for storing error messages.
error_message = ""

def error_reporter(message):
    global error_message
    new_error_message = message
    error_message = error_message + "\n" + new_error_message


# Synchronization tokens for our panic mode recovery are as followS:
# ",", ":", ";", ".", "(", ")", "{", "}" 
def p_error(p):
    global error_message
    # Tokens for synchronization:
    syncTokens = ["COMMA", "COLON", "SEMICOLON", "PERIOD", "LPAR", "RPAR", "LBRC", "RBRC"]

    new_error_message = ("Error in line '%s'" % p)
    error_message = error_message + "\n" + new_error_message

    while True:
        token = parser.token() # Get the next token

        if not token: # Parser throws None if the end of the code is reached
            new_error_message = "Reached end of input during recovery."
            error_message = error_message + "\n" + new_error_message
            break

        if (token.type in syncTokens): # Find the next synchronization point
            new_error_message = "Recovered to next {0} at Line {1}.".format(token.type, token.lineno)
            error_message = error_message + "\n" + new_error_message
            parser.errorok = True # Required to signal to parser that the error is resolved
            break


###############################################################
# NOTE: do not touch the remaining parts of this file.
###############################################################
###############################################################
# Empty rule
###############################################################
def p_empty(p):
    """
    empty :
    """

###############################################################
# Generate the parser and test it
###############################################################
parser = yacc.yacc()

def initialize_error_message():
    global error_message
    error_message = "ERRORS:\n"

def main(filename):
    initialize_error_message()
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    ast = parser.parse(inputs)
    print(error_message)
    print(ast)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
