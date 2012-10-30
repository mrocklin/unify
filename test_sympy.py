from sympy import Add, Basic
from unify import *
from unify_sympy import destruct, construct

def test_destruct():
    expr     = Basic(1, 2, 3)
    expected = Compound(Basic, (1, 2, 3))
    assert destruct(expr) == expected
