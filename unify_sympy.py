from sympy import Basic, Wild
from unify import Compound, Variable, _unify

def destruct(s):
    """ Turn a SymPy object into a Compound Tuple """
    if not isinstance(s, Basic):
        return s
    if isinstance(s, Wild):
        return Variable(s)
    return Compound(s.__class__, tuple(map(destruct, s.args)))

def construct(t):
    """ Turn a Compount Tuple into a SymPy object """
    if isinstance(t, Variable):
        return t.arg
    if not isinstance(t, Compound):
        return t
    return t.op(*map(construct, t.args))

def unify(x, y, s):
    ds = _unify(destruct(x), destruct(y), {})
    for d in ds:
        yield {construct(k): construct(v) for k, v in d.items()}
