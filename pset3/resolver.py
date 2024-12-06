"""
__author__ = "Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"
__copyright__ = "Copyright 2024, Jieung Kim, SoonWon Moon, Jay Hwan Lee"
__credits__ = ["Jieung Kim", "SoonWon Moon", "Jay Hwan Lee"]
__license__ = "MIT"
__version__ = "1.0.0"
__maintainer__ = "Jieung Kim"
__email__ = "jieungkim@yonsei.ac.kr"
"""

# This file is used to rewrite identifiers with proper names
# in AST to manage their scope effectively
# This is accomplished in two steps:
# 1. generate a symbol table
# 2. Resolve the identifiers with the appropriate names

####################################
# 1st pass : generate symbol table
####################################

# The symbol table in our compiler consists of three sub-symbol
# tables, described below.

# stable = (ntable, vtable, ftable)
# ntable = Map NIDENT stable
# vtable = Map LIDENT ('const' | 'var')
# ftable = Set LIDENT

# The top-level program's symbol table (stable) is composed of
# three distinct symbol tables: namespaces, variables, and functions.
# 1. The symbol table for namespaces maps a namespace name to its
#    corresponding symbol table. Each namespace's symbol table also
#    consists of three symbol tables: namespaces, variables, and functions.
# 2. The sub-symbol table for variables in each symbol table maps
#    an identifier of each variable to its type, either "const" or "var".
# 3. The sub-symbol table for functions in each symbol table is a set
#    of functions defined within that scope.


def collect_symbol_tables(namespaces, consts, variables, functions):
    namespace_table = generate_namespace_tables(namespaces)
    variable_table = generate_constant_symbol_table(
        consts
    ) | generate_variable_symbol_table(variables)
    function_table = generate_function_symbol_table(functions)
    return (namespace_table, variable_table, function_table)


def generate_program_symbol_table(ast):
    if ast[0] != "program":
        print(f"Error : not a valid function call")
        exit()

    return collect_symbol_tables(ast[1], ast[2], ast[3], ast[4])


def generate_namespace_symbol_table(ast):
    if ast[0] != "namespace":
        print(f"Error : not a valid function call")
        exit()

    return collect_symbol_tables(ast[2], ast[3], ast[4], ast[5])


def generate_namespace_tables(namespaces):
    return {n[1]: generate_namespace_symbol_table(n) for n in namespaces}


def generate_constant_symbol_table(constants):
    return {c[0]: "const" for c in constants}


def generate_variable_symbol_table(variables):
    return {v: "var" for v in variables}


def generate_function_symbol_table(functions):
    return {f[1] for f in functions}


# Auxiliary Functions for Symbol Tables
# These auxiliary functions can be used to implement
# the following `Resolver` class.
def generate_global_name(paths, var_name):
    if paths == []:
        return f":{var_name}"
    else:
        full_path = ".".join(paths)
        return f":{full_path}.{var_name}"


def get_focused_symbol_table(table, namespaces):
    match namespaces:
        case []:
            return table
        case [namespace, *namespaces]:
            if namespace in table[0]:
                return get_focused_symbol_table(table[0][namespace], namespaces)
            else:
                return None


def get_prefix_namespaces(namespace_stacks):
    for i in reversed(range(len(namespace_stacks) + 1)):
        yield namespace_stacks[:i]


####################################
# 2nd pass : name resolution
####################################
# The following class provides name resolution in the abstract
# syntax tree (AST), which is the output of our parser. The AST
# contains all the necessary information for intermediate code
# generation. However, directly implementing intermediate code
# generation from the AST is challenging due to the namespace
# feature in our ToyPL. To simplify this process, instead of
# managing it in a single complex pass, we implement the
# `Resolver` class. This class generates two useful pieces of
# information for intermediate code generation: "gvars" and "funcs".
#
# 1. "gvars" stores the defined variables (either constant or not)
#    within the function along with their absolute paths. The
#    absolute path for each variable serves as the key in this
#    unordered map, and the associated value is the integer value
#    stored in the variable. If a variable does not store any value,
#    its value is marked as `None`.
#
# 2. "funcs" stores all the functions in the program that need to be
#    translated into intermediate code in the next step. It contains
#    all the necessary information to translate each function into
#    the appropriate intermediate code.
#
# How It Works
# The `Resolver` class first creates a symbol table for the program
# using the functions defined above in the first line of the
# `__init__` method. It then traverses the program to update "gvars"
# and "funcs" by using the `traverse_ast` function, which you need to
# implement.
# You can add any other auxiliary functions (either within this class
# or outside of it) and fields necessary to implement this. The only
# requirement is to preserve the calling API defined below (in the
# `main` function) and in the test file (`resolver_test.py`).
#
# Example: This is the example of the generated "gvars" and "funcs"
# using this Resolver class (and "traverse_ast"). This example is
# "example/example01.toypl". You also can see  more examples in
# the "assessment" directory.

# Input:
"""
amespace Util
  func exp(m,n)
  var r
  begin
    r <- 1;
    return r;
  end
  func isqrt(n)
  begin
   return 1
  end
  func is_prime(n)
  const a := 1
  var r, i
  begin
    r <- call isqrt(n);
    i <- 2;
    return 1;
  end
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

namespace Godel
  var code, prime
  func init_put()
  begin
    code <- 1;
    prime <- 2
  end
  func init_get()
  begin
    code <- 1
  end
end

func main()
var r, x, _
begin
  _ <- call Godel.init_put();
  x <- 1;
  print(Godel.code);
  _ <- call Godel.init_get();
  x <- 1
end
"""

# Desired output of "gvar" and" funcs"
# Please carefully look at this result to figure out the
# desired behavior of this 'Resolver' class, especially,
# the following aspects:
# 1. what are stored in "gvar" and "funcs"?
# 2. how do we store names in "gvar" and "funcs"?
# 3. how do we store parameters, constant and non-constant
#    variables, and function bodies in "funcs"?
"""
{
    'gvars': {':Godel.code': None, ':Godel.prime': None}, 
    'funcs': {
        ':Util.exp': (['m', 'n'], [], ['r'],
            [('assign', 'r', ('number', 1)), 
             ('return', ('var', 'r'))]
        ), 
        ':Util.isqrt': (['n'], [], [], 
            [('return', ('number', 1))]
        ),
        ':Util.is_prime': (['n'], [('a', 1)], ['r', 'i'], 
            [('call', 'r', ':Util.isqrt', [('var', 'n')]), 
             ('assign', 'i', ('number', 2)), ('return', ('number', 1))]
        ), 
        ':Util.next_prime': (['n'], [], ['p'],
            [('assign', 'p', ('number', 0)), 
             ('while', ('==', ('var', 'p'), ('number', 0)), 
             ('stmts', 
                 [('assign', 'n', ('+', ('var', 'n'), ('number', 1))), 
                  ('call', 'p', ':Util.is_prime', [('var', 'n')])])
             ), 
             ('return', ('var', 'n'))]
        ),
        ':Godel.init_put': ([], [], [], 
            [('assign', ':Godel.code', ('number', 1)), 
             ('assign', ':Godel.prime', ('number', 2))]
        ),
        ':Godel.init_get': ([], [], [], 
            [('assign', ':Godel.code', ('number', 1))]
        ),
        ':main': ([], [], ['r', 'x', '_'], 
            [('call', '_', ':Godel.init_put', []), 
             ('assign', 'x', ('number', 1)), 
             ('print', ('var', ':Godel.code')), 
             ('call', '_', ':Godel.init_get', []), 
             ('assign', 'x', ('number', 1))]
        )
    }
}
"""


################################################################
# HW3 part start
# IMPLEMENT THE FOLLOWING CLASS
# To see how results are generated, refer to the test oracles in
# the [assessment] directory.
################################################################
class Resolver:

    def __init__(self, ast):
        self.abs_stable = generate_program_symbol_table(ast)  # stable
        self.gvars = {}  # Map GIDENT (None | int)
        self.funcs = {}  # Map GIDENT (params, consts, vars, stmts)
        # print(self.abs_stable)
        # print(ast)
        self.traverse_ast(ast)

    def traverse_ast(self, ast):
        _program = ast[0]
        namespace_decs = ast[1]
        const_decs = ast[2]
        var_decs = ast[3]
        func_decs = ast[4]

        self.resolve_namespaces(namespace_decs, [])
        self.resolve_consts(const_decs, [])
        self.resolve_vars(var_decs, [])
        self.resolve_funcs(func_decs, [])

    def resolve_namespaces(self, namespace_decs, namespace_stack):
        for namespace in namespace_decs:
            name = namespace[1]
            subnamespace_decs = namespace[2]
            const_decs = namespace[3]
            var_decs = namespace[4]
            func_decs = namespace[5]

            self.resolve_namespaces(subnamespace_decs, [*namespace_stack, name])
            self.resolve_consts(const_decs, [*namespace_stack, name])
            self.resolve_vars(var_decs, [*namespace_stack, name])
            self.resolve_funcs(func_decs, [*namespace_stack, name])

    def resolve_consts(self, const_decs, namespace_stack):
        for const in const_decs:
            name = generate_global_name(namespace_stack, const[0])
            # TODO integrate with `resolve_ident`
            self.gvars[name] = None if len(const) == 1 else const[1]

    def resolve_vars(self, var_decs, namespace_stack):
        for var in var_decs:
            name = generate_global_name(namespace_stack, var)
            # TODO integrate with `resolve_ident`
            is_uninitialized = type(var) == str
            self.gvars[name] = None if is_uninitialized else var[1]

    # TODO
    def resolve_ident(self, path_type, paths, name, namespace_stack, func_node):
        """
        stable = (ntable, vtable, ftable)
        ntable = Map NIDENT stable
        vtable = Map LIDENT ('const' | 'var')
        ftable = Set LIDENT

        (
            {
                'Foo': ({}, {'x': 'const'}, set()),
                'Bar': ({'Foo': ({}, {'x': 'const'}, {'foo'})}, {'x': 'const'}, set()),
                'Main': ({'Foo': ({}, {'x': 'const'}, set())}, {'x': 'const'}, {'main'})
            },

            {'x': 'const', 'y': 'var'},

            {'main'}
        )
        """


        # local variable
        # function argument
        # If the identifier is a local variable or given as an argument,
        # we should not do anything but just use the ident as-is.

        params = func_node[2]
        local_consts = [i for i, _value in func_node[3]]
        local_vars = func_node[4]
        # print(f"local idents: {[*params, *local_consts, *local_vars]}")
        if name in [*params, *local_consts, *local_vars]:
            return name
        
        if path_type == "abs":
            return generate_global_name(paths, name)

        # print("-------------------------")
        # print(f"path_type: {path_type}")
        # print(f"paths: {paths}")
        # print(f"ident: {ident}")
        # print(f"namespace_stack: {namespace_stack}")

        # print(f"params: {params}")
        # print(f"consts: {local_consts}")
        # print(f"vars: {local_vars}")

        for pref_namespaces in get_prefix_namespaces(namespace_stack):
            # print(f"pref_namespaces: {pref_namespaces}")
            focused_stable = get_focused_symbol_table(self.abs_stable, pref_namespaces)
            # print(f"focused_stable: {focused_stable}")

            for p in paths:
                focused_stable = focused_stable[0].get(p, None)
                if focused_stable is None:
                    break
            else:
                _, vtable, ftable =  focused_stable
                if name in vtable or name in ftable:
                    return generate_global_name([*pref_namespaces, *paths], name)
            
        raise Exception(f"No symbol {name} found")

    def resolve_stmts(self, stmts, resolved_stmts, namespace_stack, func_node):
        for stmt in stmts:
            resolved_stmt = [*stmt]
            stmt_type = stmt[0]
            match stmt_type:
                case "stmts":
                    resolved_substmts = self.resolve_stmts(stmt[1], [], namespace_stack, func_node)
                    resolved_stmts.append((stmt_type, resolved_substmts))
                case "read":
                    path_type, paths, ident_name = stmt[1]
                    resolved_stmt[1] = self.resolve_ident(path_type, paths, ident_name, namespace_stack, func_node)
                    resolved_stmts.append(tuple(resolved_stmt))
                case "assign":
                    path_type, paths, ident_name = stmt[1]
                    resolved_stmt[1] = self.resolve_ident(path_type, paths, ident_name, namespace_stack, func_node)
                    resolved_stmt[2] = self.resolve_expr(stmt[2], namespace_stack, func_node)
                    resolved_stmts.append(tuple(resolved_stmt))
                case "print":
                    resolved_stmt[1] = self.resolve_expr(stmt[1], namespace_stack, func_node)
                    resolved_stmts.append(tuple(resolved_stmt))
                case "if":
                    _, cond_expr, true_stmt, false_stmt = stmt
                    resolved_stmt[1] = self.resolve_expr(cond_expr, namespace_stack, func_node)
                    resolved_stmt[2] = self.resolve_stmts([true_stmt], [], namespace_stack, func_node)[0]
                    resolved_stmt[3] = self.resolve_stmts([false_stmt], [], namespace_stack, func_node)[0]
                    resolved_stmts.append(tuple(resolved_stmt))
                case "call":
                    # print(stmt)
                    _, ret_ident, func_ident, args = stmt

                    ret_path_type, ret_paths, ret_name = ret_ident
                    resolved_stmt[1] = self.resolve_ident(ret_path_type, ret_paths, ret_name, namespace_stack, func_node)

                    func_path_type, func_paths, func_name = func_ident
                    # print(func_ident)
                    resolved_stmt[2] = self.resolve_ident(func_path_type, func_paths, func_name, namespace_stack, func_node)
                    resolved_stmt[3] = [
                        self.resolve_expr(arg, namespace_stack, func_node) for arg in stmt[3]
                    ]
                    resolved_stmts.append(tuple(resolved_stmt))
                case "return":
                    _, expr = stmt
                    resolved_stmt[1] = self.resolve_expr(expr, namespace_stack, func_node)
                    resolved_stmts.append(tuple(resolved_stmt))
                case "while":
                    _, cond_expr, inner_stmt = stmt
                    resolved_stmt[1] = self.resolve_expr(cond_expr, namespace_stack, func_node)
                    resolved_stmt[2] = self.resolve_stmts([inner_stmt], [], namespace_stack, func_node)[0]
                    resolved_stmts.append(tuple(resolved_stmt))
                case _:
                    resolved_stmts.append(tuple(resolved_stmt))

        return resolved_stmts

    def resolve_funcs(self, func_decs, namespace_stack):
        # print("---------------------")
        # print(namespace_stack)
        for func in func_decs:
            name = generate_global_name(namespace_stack, func[1])
            # print(name)

            params = func[2]
            consts = func[3]
            vars = func[4]
            stmts = func[5]

            # print(stmts)
            resolved_stmts = self.resolve_stmts(stmts, [], namespace_stack, func)

            self.funcs[name] = (params, consts, vars, resolved_stmts)
            # print(self.funcs)

    def resolve_expr(self, expr, namespace_stack, func_node):
        expr_type = expr[0]
        match expr_type:
            case "var":
                # print(f"{namespace_stack}:{expr}")
                path_type, paths, ident_name = expr[1]
                return (
                    expr_type,
                    self.resolve_ident(path_type, paths, ident_name, namespace_stack, func_node),
                )
            case "+" | "-" | "*" | "/" | "%":
                return (
                    expr_type,
                    self.resolve_expr(expr[1], namespace_stack, func_node),
                    self.resolve_expr(expr[2], namespace_stack, func_node),
                )
            case "or" | "and":
                return (
                    expr_type,
                    self.resolve_expr(expr[1], namespace_stack, func_node),
                    self.resolve_expr(expr[2], namespace_stack, func_node),
                )
            case "==" | "/=" | "<" | "<=" | ">" | ">=":
                return (
                    expr_type,
                    self.resolve_expr(expr[1], namespace_stack, func_node),
                    self.resolve_expr(expr[2], namespace_stack, func_node),
                )
            case _:
                return expr


################################################################
# HW3 part end
# NOTE: do not touch the remaining parts of this file.
###############################################################
# Below is the code to run the `Resolver`.
# Your implementation should work properly with the following interface.
import ply.lex as lex
import ply.yacc as yacc
import lexer
import parser
import sys


def main(filename):
    file_obj = open(filename, "r")
    inputs = file_obj.read()
    file_obj.close()
    lexer.lexer.lineno = 1
    ast = parser.parser.parse(inputs)
    r = Resolver(ast)
    print(str({"gvars": r.gvars, "funcs": r.funcs}))


if __name__ == "__main__":
    filename = sys.argv[1]
    main(filename)
