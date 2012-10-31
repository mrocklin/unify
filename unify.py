""" Generic Unification algorithm for expression trees with lists of children

The implementation is a direct translation of

Artificial Intelligence: A Modern Approach
by
Stuart Russel and Peter Norvig


It is modified in the following ways:

1.  We allow associative and commutative Compound expressions. This results in
    combinatorial blowup.
2.  We provide generic interfaces to symbolic algebra libraries in Python.
"""


from collections import namedtuple
from itertools import combinations
Compound = namedtuple('Compound', 'op args')
Variable = namedtuple('Variable', 'arg')
CondVariable = namedtuple('Variable', 'arg valid')

def iterable(x):
    """ Is x a traditional iterable? """
    return type(x) in (tuple, list, set)

def _unify(x, y, s, **fns):
    # print 'Unify: ', x, y, s
    if x == y:
        yield s
    elif isinstance(x, (Variable, CondVariable)):
        for x in _unify_var(x, y, s, **fns): yield x
    elif isinstance(y, (Variable, CondVariable)):
        for x in _unify_var(y, x, s, **fns): yield x
    elif isinstance(x, Compound) and isinstance(y, Compound):
        for sop in _unify(x.op, y.op, s, **fns):
            if len(x.args) == len(y.args):
                for x in _unify(x.args, y.args, sop, **fns): yield x
            elif is_associative(x) and is_associative(y):
                a, b = (x, y) if len(x.args) < len(y.args) else (y, x)
                if is_commutative(x) and is_commutative(y):
                    combinations = allcombinations(a.args, b.args, None)
                else:
                    combinations = allcombinations(a.args, b.args, True)
                for aaargs, bbargs in combinations:
                    aa = aaargs
                    bb = [unpack(Compound(b.op, arg)) for arg in bbargs]
                    for x in _unify(aa, bb, sop, **fns): yield x

    elif iterable(x) and iterable(y) and len(x) == len(y):
        if len(x) == 0:
            yield s
        else:
            for shead in _unify(x[0], y[0], s, **fns):
                for x in _unify(x[1:], y[1:], shead, **fns):
                    yield x

def _unify_var(var, x, s, **fns):
    # print 'UnVar: ', var, x, s
    if var in s:
        for x in _unify(s[var], x, s, **fns): yield x
    elif occur_check(var, x):
        pass
    elif isinstance(var, CondVariable) and var.valid(x):
        yield assoc(s, var, x)
    elif isinstance(var, Variable):
        yield assoc(s, var, x)

def occur_check(var, x):
    """ Return true if var occurs anywhere in x """
    if var == x:
        return True
    elif isinstance(x, Compound):
        return occur_check(var, x.args)
    elif iterable(x):
        if any(occur_check(var, xi) for xi in x): return True
    return False

def assoc(d, key, val):
    """ Return copy of d with key associated to val """
    d = d.copy()
    d[key] = val
    return d

def unpack(x):
    if isinstance(x, Compound) and len(x.args) == 1:
        return x.args[0]
    else:
        return x

def allcombinations(A, B, ordered):
    """

    """
    if len(A) == len(B):
        yield A, B
        raise StopIteration()
    sm, bg = (A, B) if len(A) < len(B) else (B, A)
    for part in kbin(range(len(bg)), len(sm), ordered=ordered):
        if bg == B:
            yield A, partition(B, part)
        else:
            yield partition(A, part), B

def index(it, ind):
    """ Fancy indexing into an iterable

    >>> index([10, 20, 30], (1, 2, 0))
    [20, 30, 10]
    """
    return type(it)([it[i] for i in ind])

def partition(it, part):
    """ Partition an iterable into pieces defined by indices

    >>> partition((10, 20, 30, 40), [[0, 1, 2], [3]])
    ((10, 20, 30), (40,))
    """

    t = type(it)
    return t([index(it, ind) for ind in part])

def is_associative(x):
    from sympy import Add, Mul
    return (isinstance(x, Compound) and (x.op in {'Add', 'Mul', 'CAdd', 'CMul'}
         or x.op in (Add, Mul)))
    # TODO: need a more general way to test for associativity

def is_commutative(x):
    from sympy import Add, Mul
    return (isinstance(x, Compound) and (x.op in {'CAdd', 'CMul'}) or
            x.op in (Add, Mul))

def kbin(l, k, ordered=True):
    """
    Return sequence ``l`` partitioned into ``k`` bins.
    If ordered is True then the order of the items in the
    flattened partition will be the same as the order of the
    items in ``l``; if False, all permutations of the items will
    be given; if None, only unique permutations for a given
    partition will be given.

    Examples
    ========

    >>> from sympy.utilities.iterables import kbin
    >>> for p in kbin(range(3), 2):
    ...     print p
    ...
    [[0], [1, 2]]
    [[0, 1], [2]]
    >>> for p in kbin(range(3), 2, ordered=False):
    ...     print p
    ...
    [(0,), (1, 2)]
    [(0,), (2, 1)]
    [(1,), (0, 2)]
    [(1,), (2, 0)]
    [(2,), (0, 1)]
    [(2,), (1, 0)]
    [(0, 1), (2,)]
    [(0, 2), (1,)]
    [(1, 0), (2,)]
    [(1, 2), (0,)]
    [(2, 0), (1,)]
    [(2, 1), (0,)]
    >>> for p in kbin(range(3), 2, ordered=None):
    ...     print p
    ...
    [[0], [1, 2]]
    [[1], [2, 0]]
    [[2], [0, 1]]
    [[0, 1], [2]]
    [[1, 2], [0]]
    [[2, 0], [1]]

    """
    from sympy.utilities.iterables import partitions
    from itertools import permutations
    def rotations(seq):
        for i in range(len(seq)):
            yield seq
            seq.append(seq.pop(0))
    if ordered is None:
        func = rotations
    else:
        func = permutations
    for p in partitions(len(l), k):
        if sum(p.values()) != k:
            continue
        for pe in permutations(p.keys()):
            rv = []
            i = 0
            for part in pe:
                for do in range(p[part]):
                    j = i + part
                    rv.append(l[i: j])
                    i = j
            if ordered:
                yield rv
            else:
                template = [len(i) for i in rv]
                for pp in func(l):
                    rvp = []
                    ii = 0
                    for t in template:
                        jj = ii + t
                        rvp.append(pp[ii: jj])
                        ii = jj
                    yield rvp
