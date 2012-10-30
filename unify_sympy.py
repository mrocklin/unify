from sympy import Basic, Wild
from unify import Compound, Variable, _unify

def destruct(s):
    """ Turn a SymPy object into a Compound Tuple """
    if isinstance(s, Wild):
        return Variable(s)
    if not isinstance(s, Basic) or s.is_Atom:
        return s
    return Compound(s.__class__, tuple(map(destruct, s.args)))

def construct(t):
    """ Turn a Compount Tuple into a SymPy object """
    if isinstance(t, Variable):
        return t.arg
    if not isinstance(t, Compound):
        return t
    return Basic.__new__(t.op, *map(construct, t.args))

def unify(x, y, s):
    """ Structural unification of two expressions possibly containing Wilds

    >>> from unify_sympy import unify
    >>> from sympy import Wild
    >>> from sympy.abc import x, y, z
    >>> expr = 2*x + y + z
    >>> pattern = 2*Wild('p') + Wild('q')
    >>> list(unify(expr, pattern, {}))
    [{p_: x, q_: y + z}]

    >>> expr = x + y + z
    >>> pattern = Wild('p') + Wild('q')
    >>> list(unify(expr, pattern, {}))
    [{p_: z, q_: x + y}, {p_: y + z, q_: x}]
    """

    ds = _unify(destruct(x), destruct(y), {})
    for d in ds:
        yield {construct(k): construct(v) for k, v in d.items()}
