# ToyPL-compiler (2024 ver.)
This is a compiler for ToyPL programming language written in Python using the Ply library (https://www.dabeaz.com/ply/).

## Introduction of ToyPL
The ToyPL language is a simple, imperative-style educational programming language. It is small and lacks many of the useful features that practical programming languages usually have, but it is good for learning how to construct a compiler.

### Grammar
The following is the grammar of ToyPL, written in BNF form, with the following criteria:
1) Words with uppercase characters are variables (non-terminals).
2) Words with lowercase characters inside quotation marks are terminals.
3) "E" represents epsilon.

```
PROGRAM -> NAMESPACE_DECS CONST_DECS VAR_DECS FUNC_DECS

NAMESPACE_DECS -> E | NAMESPACE_DEC NAMESPACE_DECS
NAMESPACE_DEC -> "namespace" NIDENT NAMESPACE_DECS CONST_DECS VAR_DECS FUNC_DECS "end"

CONST_DECS -> E | "const" CONSTS
CONSTS -> LIDENT ":=" NUMBER | LIDENT ":=" NUMBER "," CONSTS

VAR_DECS -> E | "var" VARS
VARS -> LIDENT | LIDENT "," VARS

FUNC_DECS -> E | FUNC_DEC FUNC_DECS
FUNC_DEC -> "func" LIDENT "(" PARAMS ")" CONST_DECS VAR_DECS "begin" STMTS "end"
PARAMS -> E | LIDENT PARAMS_TAIL
PARAMS_TAIL -> E | "," LIDENT PARAMS_TAIL

STMT -> "skip"
      | IDENT "<-" "read"
      | "print" "(" EXPR ")"
      | IDENT "<-" EXPR
      | IDENT "<-" "call" IDENT "(" ARGS ")"
      | "if" BEXPR "then" STMT "else" STMT
      | "while" BEXPR "do" STMT
      | "return" EXPR
      | "{" STMTS "}"

STMTS -> STMT | STMT ";" | STMT ";" STMTS
ARGS -> E | EXPR ARGS_TAIL
ARGS_TAIL -> E | "," EXPR ARGS

CMP_OP -> "==" | "/=" | "<" | "<=" | ">" | ">="

BEXPR -> BTERM | BEXPR "||" BTERM
BTERM -> BFACTOR | BTERM "&&" BFACTOR
BFACTOR -> EXPR CMP_OP EXPR | "(" BEXPR ")"

EXPR -> TERM | EXPR "+" TERM | EXPR "-" TERM
TERM -> FACTOR | TERM "*" FACTOR | TERM "/" FACTOR | TERM "%" FACTOR
FACTOR -> IDENT | NUMBER | "(" EXPR ")"

IDENT -> ABS_PATH LIDENT | REL_PATH LIDENT
ABS_PATH -> ":" REL_PATH
REL_PATH -> E | NIDENT "." REL_PATH

# The following three are defined with regular expressions.
NIDENT := [A-Z][a-zA-Z_0-9]*   # namespace identifier
LIDENT := [a-z_][a-zA-Z_0-9]*  # local identifier
NUMBER := [0-9]+
```

Writing comments in the ToyPL program is also available, and ToyPL only uses a single line style comment starts with #.

> e.g., ```# This is a comment```

Also, three characters (tab - '\t', whitespace - ' ', and newline - '\n') will be ignored while tokenizing the input programs. However, you have to increase a line number when you read a newline character.

## Usage
Recommend to use Python 3.11~

To run built-in testing for the lexer, type the following command:
- python lexer_test.py

To run your lexer with your own files, type the following command:
- python lexer.py [path-to-your-file]

To run built-in testing for the parser, type the following command:
- python parser_test.py

To run your parser with your own files, type the following command:
- python parser.py [path-to-your-file]

To run built-in testing for the identifier resolver, type the following command:
- python resolver_test.py

To run your identifier resolver with your own files, type the following command:
- python resolver.py [path-to-your-file]

To run built-in testing for the code generator, type the following command:
- python codegen_test.py

To run your code generator with your own files, type the following command:
- python codegen.py [path-to-your-file]

## History
Version 3.0 (2024-11.02)

## Credits
Jieung Kim (jieungkim@yonsei.ac.kr), SoonwWon Moon, and Jay Hwan Lee

## License
The MIT License (MIT)

Copyright (c) 2024 Jieung Kim et al. (One hidden contributor)

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
