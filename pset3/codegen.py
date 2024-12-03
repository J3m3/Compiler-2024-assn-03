"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""

# This file is used to generate intermediate code for
# our ToyPL.It is divided into two parts: `CodeGenFunc`
# and `CodeGen`. While you are not required to maintain
# this structure, you must ensure that all test cases
# pass without modifying the top-level interface of
# this file.

# Our design includes two classes:
# 1. `CodeGenFunc`: This class creates intermediate code
#     for each function. The intermediate code for each
#     function is similar to our original ToyPL syntax,
#     but with the following main differences:
#     1) Using "jump" and "label" instead of while loops.
#     2) Using "absolute" paths instead of relative
#        paths within namespaces.
# 2. Iteratively apply `CodeGenFunc` to each function
#    in the file and print the generated result as a
#    string format.
#
# Here are a few examples of function-wise intermediate
# codes, which are the results of the generation in
# `example01`. Note that the intermediate code differs
# somewhat from the TAC (Three-Address Code) format in
# our lecture notes. The format used here simplifies
# the problem compared to the TAC format from our
# lecture notes.

# Input (next_prime function defined in Util namespace)
'''
namespace Util
  ...
  func next_prime(n)
  var p
  begin
    p <- 0;
    while (p == 0) do {
      n <- n + 1;
      p <- call is_prime(n);
    };
    return n
  end
end
'''
# Desired output
'''
func :Util.next_prime(n) {
	t0 <- 0
	p <- t0
L0:
	t1 <- 0
	t2 <- p == t1
	branch t2 L1 L2
L1:
	t3 <- 1
	t4 <- n + t3
	n <- t4
	p <- call :Util.is_prime(n)
	jump L0
L2:
	return n
}
'''

# Input (main function)
'''
func main()
var r, x, _
begin
  _ <- call Godel.init_put();
  x <- 1;
  print(Godel.code);
  _ <- call Godel.init_get();
  x <- 1
end
'''
# Desired output
'''
func :main() {
	_ <- call :Godel.init_put()
	t0 <- 1
	x <- t0
	print :Godel.code
	_ <- call :Godel.init_get()
	t1 <- 1
	x <- t1
}
'''

################################################################
# HW3 part start
# IMPLEMENT THE FOLLOWING CLASSES
# To see how results are generated, refer to the test oracles in 
# the [assessment] directory.
################################################################
class CodeGenFunc:

    def __init__(self, constants, function_ast):
        self.code = []
        self.codegen_stmts(function_ast)

    def codegen_stmts(self, ast):
        pass

# As discussed, `CodeGen` is designed to iteratively
# apply the previously defined `CodeGenFunc` to each
# function in the program.
#
# Please note that you do not need to strictly follow
# this class structure if you can implement the code
# generation using a different approach, as long as you
# maintain the top-level interface and correctly pass
# all test cases. However, adhering to this interface
# might be easier than defining all parts from scratch.
class CodeGen:

    def __init__(self, gvars, funcs):
        self.gvars = gvars
        self.codes = {}
        for (f, (parameters, constants, _, ast)) in funcs.items():
            code_gen_func = CodeGenFunc(constants, ast)
            self.codes[f] = (parameters, code_gen_func.code)

    def pretty_printer(self):
        pass        

################################################################
# HW3 part end
# NOTE: do not touch the remaining parts of this file.
###############################################################
# Below is the code to run the `CodeGen`.
# Your implementation should work properly with the following interface.
import ply.lex as lex
import ply.yacc as yacc
import lexer
import parser
import resolver
import sys

def main(filename):
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    lexer.lexer.lineno = 1
    ast = parser.parser.parse(inputs)
    r = resolver.Resolver(ast)
    cg = CodeGen(r.gvars, r.funcs)
    print(cg.pretty_printer())

if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
