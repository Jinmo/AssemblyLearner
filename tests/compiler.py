import unittest
from _utils import go
from asmlearner.library.compiler import asm

class CompilerTestCase(unittest.TestCase):
    def test_compile(self):
        p = { "suffix": "____suffix____" }

        s = { "answer": "answer" }
        print s['answer']
        asm.compileProblem(p, s)

def run():
    go(CompilerTestCase)
