"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file defines test cases for our ToyPL parser.
import ply.lex as lex
import ply.yacc as yacc
import lexer
import parser
import resolver
import codegen
import unittest
import sys

cases = [
    ("assessment/test01.toypl", "assessment/test01.ir")  # 5 pts
    ,
    ("assessment/test02.toypl", "assessment/test02.ir")  # 5 pts
    ,
    ("assessment/test03.toypl", "assessment/test03.ir")  # 10 pts
    ,
    ("assessment/test04.toypl", "assessment/test04.ir")  # 10 pts
    ,
    ("assessment/test05.toypl", "assessment/test05.ir")  # 10 pts
    ,
    ("assessment/test06.toypl", "assessment/test06.ir")  # 10 pts
    ,
    ("assessment/test07.toypl", "assessment/test07.ir")  # 15 pts
    ,
    ("assessment/test08.toypl", "assessment/test08.ir")  # 15 pts
    ,
    ("assessment/test09.toypl", "assessment/test09.ir")  # 20 pts
]

def eval_golden(i):
    lexer.lexer.lineno = 1
    ast = parser.parser.parse(i)
    r = resolver.Resolver(ast)
    cg = codegen.CodeGen(r.gvars, r.funcs)
    return cg.pretty_printer()

def check_golden(tester, fs):
    (if_name, of_name) = fs
    if_obj = open(if_name, "r")
    i = if_obj.read()
    if_obj.close()
    o = eval_golden(i)
    of_obj = open(of_name, "r")
    o_golden = of_obj.read()
    of_obj.close()
    tester.assertEqual(o, o_golden)

class ParserTest(unittest.TestCase):

    def test_case1(self):
        check_golden(self, cases[0])

    def test_case2(self):
        check_golden(self, cases[1])

    def test_case3(self):
        check_golden(self, cases[2])

    def test_case4(self):
        check_golden(self, cases[3])

    def test_case5(self):
        check_golden(self, cases[4])

    def test_case6(self):
        check_golden(self, cases[5])

    def test_case7(self):
        check_golden(self, cases[6])

    def test_case8(self):
        check_golden(self, cases[7])

    def test_case9(self):
        check_golden(self, cases[8])

if __name__ == "__main__":
    unittest.main()
