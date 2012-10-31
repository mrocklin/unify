from sympy import Basic, Wild
from sympy.core.operations import AssocOp
from unify import Compound, Variable, _unify

def is_associative(x):
    return isinstance(x, Compound) and issubclass(x.op, AssocOp)

def is_commutative(x):
    return isinstance(x, Compound) and _build(x).is_commutative

def destruct(s):
    """ Turn a SymPy object into a Compound Tuple """
    if isinstance(s, Wild):
        return Variable(s)
    if not isinstance(s, Basic) or s.is_Atom:
        return s
    return Compound(s.__class__, tuple(map(destruct, s.args)))

def _build(t):
    if isinstance(t, Variable):
        return t.arg
    if not isinstance(t, Compound):
        return t
    # This does auto-evaluation. Watch out!
    return t.op(*map(construct, t.args))

def construct(t):
    """ Turn a Compound Tuple into a SymPy object """
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

    ds = _unify(destruct(x), destruct(y), {}, is_associative=is_associative,
                                              is_commutative=is_commutative)
    for d in ds:
        yield {construct(k): construct(v) for k, v in d.items()}
