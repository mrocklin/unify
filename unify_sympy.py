from sympy import Basic
from unify import Compound

def destruct(s):
    """ Turn a SymPy object into a Compound Tuple """
    if not isinstance(s, Basic):
        return s
    return Compound(s.__class__, tuple(map(destruct, s.args)))

def construct(t):
    """ Turn a Compount Tuple into a SymPy object """
    if not isinstance(t, Compound):
        return t
    return t.op(*t.args)
