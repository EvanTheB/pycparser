#!/usr/bin/env python3

import sys
import os
from pycparser import c_parser, c_ast, parse_file


def main(args):
    parser = c_parser.CParser()

    for arg in args:
        ast = parse_file(arg)
        # ast = parser.parse(arg)
        ast.show(showcoord=True)
        walk_tree(ast, {})


def walk_tree(node, scope):
    for child in node:
        typ = type(child)

        if typ == c_ast.Decl:
            scope[child.name] = child.type

        elif typ == c_ast.FuncDef:
            # functions : FuncDecl(args, type)
            scope[child.decl.name] = child.decl.type
            func_scope = dict(scope)
            if child.decl.type.args:
                for param in child.decl.type.args.params:
                    func_scope[param.name] = param.type
            walk_tree(child.body, func_scope)

        elif typ == c_ast.ID:
            print(f"{child.name} is in scope:", child.name in scope)

        else:
            walk_tree(child, dict(scope))


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
