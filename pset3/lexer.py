"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
import string

# This file implements a lexer for ToyPL, which is described in our README file.
import ply.lex as lex
import sys

# Reserved keywords and token definitions. You should not touch them.
reserved = {
    "namespace": "NAMESPACE",
    "const": "CONST",
    "var": "VAR",
    "func": "FUNC",
    "begin": "BEGIN",
    "end": "END",
    "skip": "SKIP",
    "read": "READ",
    "print": "PRINT",
    "call": "CALL",
    "if": "IF",
    "then": "THEN",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "return": "RETURN"
}

tokens = [
    # separators
    "COMMA",  # ,
    "COLON",  # :
    "SEMICOLON",  # ;
    "PERIOD",  # .
    "LPAR",  # (
    "RPAR",  # )
    "LBRC",  # {
    "RBRC",  # }
    # arithmetic operators
    "PLUS",  # +
    "MINUS",  # -
    "MUL",  # *
    "DIV",  # /
    "MOD",  # %
    # comparison operators
    "EQ",  # ==
    "NE",  # /=
    "LT",  # <
    "LE",  # <=
    "GT",  # >
    "GE",  # >=
    # boolean operators
    "OR",  # ||
    "AND",  # &&
    # assignments
    "DEFINE",  # :=
    "ASSIGN",  # <-
    # tokens that has to be defined with action functions
    "NIDENT",
    "LIDENT",
    "NUMBER",
] + list(reserved.values())

################################################################
# HW1 part start
# MODIFY THE FOLLOWING PARTS AND FILL OUT WITH YOUR OWN DEFINITIONS
################################################################
t_COMMA = r","
t_COLON = r":"
t_SEMICOLON = r";"
t_PERIOD = r"\."
t_LPAR = r"\("
t_RPAR = r"\)"
t_LBRC = r"{"
t_RBRC = r"}"
t_PLUS = r"\+"
t_MINUS = r"\-"
t_MUL = r"\*"
t_DIV = r"/"
t_MOD = r"%"
t_EQ = r"=="
t_NE = r"/="
t_LT = r"<"
t_LE = r"<="
t_GT = r">"
t_GE = r">="
t_OR = r"\|\|"
t_AND = r"&&"
t_DEFINE = r":="
t_ASSIGN = r"<-"
t_NIDENT = r"[A-Z][a-zA-Z_0-9]*"
t_ignore = " \t"

error_message = ""

def errorHandlerMsg(t, newT, message):
    t.value = newT
    t.type = reserved.get(newT)
    return t

def errorHandler(t, errorType):
    break_innerLoop = False
    global error_message 

    if (errorType == "transpose"):
        for i in range(len(t.value) - 1):  # Check for transpose
            swapped = t.value[:i] + t.value[i + 1] + t.value[i] + t.value[i + 2:]  # swap all adjacent letters
            if swapped in reserved:
                new_error_message = "Char transpose: {0} -> {1}".format(t.value, swapped)
                error_message = error_message + "\n" + new_error_message
                errorHandlerMsg(t, swapped, new_error_message)
                # errorHandlerMsg(t, swapped, "Char transpose: {0} -> {1}".format(t.value, swapped))
                break
    elif (errorType == "replace"):
        for i in range(len(t.value)):  # Check for char replacement
            for j in string.ascii_lowercase:  # iterate through all lowercase letters
                swapped = t.value[:i] + j + t.value[i + 1:]  # swap individual characters
                if swapped in reserved:
                    new_error_message = "Char replace: {0} -> {1}".format(t.value, swapped)
                    error_message = error_message + "\n" + new_error_message                
                    errorHandlerMsg(t, swapped, new_error_message)
                    break_innerLoop = True  # avoid repeat error messages
                    break
            if break_innerLoop: break
    elif (errorType == "missing"):
        for i in range(len(t.value) + 1): # Check for missing char, ignore 2-char keywords
            for j in string.ascii_lowercase:  # iterate through all lowercase letters
                swapped = t.value[:i] + j + t.value[i:]  # add individual characters
                if swapped in reserved:
                    new_error_message = "Char insert: {0} -> {1}".format(t.value, swapped)
                    error_message = error_message + "\n" + new_error_message
                    errorHandlerMsg(t, swapped, new_error_message)
                    break_innerLoop = True
                    break
            if break_innerLoop: break
    elif (errorType == "extra"):
        for i in range(len(t.value)): # check for extra char
            swapped = t.value[:i] + t.value[i + 1:]
            if swapped in reserved:
                new_error_message = "Char remove: {0} -> {1}".format(t.value, swapped)
                error_message = error_message + "\n" + new_error_message
                errorHandlerMsg(t, swapped, error_message)
                break
    return t

def t_RESERVED(t):
    r"[a-z_][a-zA-Z_0-9]*"
    global error_message 
    t.type = reserved.get(t.value, "LIDENT")  # Check for reserved words
    if (t.type == "LIDENT"): # Was not found in RESERVED
        for keyword in reserved:
            if (len(t.value) == len(keyword)):  # Same length
                errorHandler(t, "transpose")  # transpose
                if (t.type == "LIDENT"): errorHandler(t, "replace")  # replace
            elif ((len(t.value) == len(keyword) - 1) and (len(keyword) > 2)):
                errorHandler(t, "missing")  # missing char
            elif (len(t.value) == len(keyword) + 1):
                errorHandler(t, "extra")  # extra char

    if (t.type == "LIDENT"): # Still not found in RESERVED
        if (len(t.value) > 79): # Way too long identifier
            new_error_message = "Long identifier '%s'" % t.value
            error_message = error_message + "\n" + new_error_message
            t.value = t.value[:79] # Take only the first 79 chars
    return t


def t_NUMBER(t):
    r"\d+"
    global error_message 
    t.value = int(t.value)
    if (((t.value.bit_length() + 7) // 8) > 4 ):
        new_error_message = "Large number size '%i'" % t.value
        error_message = error_message + "\n" + new_error_message
        t.value = 0
    return t


def t_newline(t):
    r"\n+"
    t.lexer.lineno += len(t.value)


def t_error(t):
    global error_message 
    new_error_message = "Illegal character '%s'" % t.value[0]
    error_message = error_message + "\n" + new_error_message
    t.lexer.skip(1)

def t_comment(t):
    r"\#[^\n]*"
    pass


################################################################
# HW1 part end"
################################################################

# Do not touch after this line
# Create a lexer
lexer = lex.lex()

def initialize_error_message():
    global error_message
    error_message = "ERRORS:\n"

def lex_str(s):
    lexer.input(s)
    lexer.lineno = 1
    ts = []
    while True:
        t = lexer.token()
        if t:
            ts.append(t)
        else:
            lexer.lineno = 1
            return ts

def main(filename):
    initialize_error_message()
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    tok_list = lex_str(inputs)
    print(error_message)
    print(tok_list)


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
