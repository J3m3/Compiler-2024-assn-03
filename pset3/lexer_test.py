"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""
# This file defines test cases for our ToyPL lexer.
import ply.lex as lex
import lexer
import unittest
import sys

cases = [
    ("assessment/test01.toypl", "assessment/test01_lex_result") 
    ,
    ("assessment/test02.toypl", "assessment/test02_lex_result") 
    ,
    ("assessment/test03.toypl", "assessment/test03_lex_result") 
    ,
    ("assessment/test04.toypl", "assessment/test04_lex_result") 
    ,
    ("assessment/test05.toypl", "assessment/test05_lex_result")
    ,
    ("assessment/test06.toypl", "assessment/test06_lex_result")  
    ,
    ("assessment/test07.toypl", "assessment/test07_lex_result") 
    ,
    ("assessment/test08.toypl", "assessment/test08_lex_result") 
    ,
    ("assessment/test09.toypl", "assessment/test09_lex_result") 
]


def eval_golden(i):
    return str(lexer.lex_str(i))


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


class LexerTest(unittest.TestCase):

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
