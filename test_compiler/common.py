import ast
import glob
import inspect
import compiler.pycodegen
from .bytecode_helper import BytecodeTestCase
from types import CodeType
from os import path
from subprocess import run, PIPE


def glob_test(dir, pattern, adder):
    base_path = path.dirname(__file__)
    target_dir = path.join(base_path, dir)
    for fname in glob.glob(path.join(target_dir, pattern), recursive=True):
        modname = path.relpath(fname, base_path)
        adder(modname, fname)


class CompilerTest(BytecodeTestCase):
    def compile(self, code, peephole=True):
        code = inspect.cleandoc("\n" + code)
        tree = ast.parse(code)
        tree.filename = ""
        gen = compiler.pycodegen.ModuleCodeGenerator(tree, peephole)
        return gen.getCode()

    def run_code(self, code, peephole=True):
        compiled = self.compile(code, peephole)
        d = {}
        exec(compiled, d)
        return d

    def to_graph(self, code):
        code = inspect.cleandoc("\n" + code)
        tree = ast.parse(code)
        tree.filename = ""
        gen = compiler.pycodegen.ModuleCodeGenerator(tree, True)
        return gen.graph
