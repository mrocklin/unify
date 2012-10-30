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
Compound = namedtuple('Compound', 'op args')
Variable = namedtuple('Variable', 'arg')
CondVariable = namedtuple('Variable', 'arg valid')

def iterable(x):
    """ Is x a traditional iterable? """
    return type(x) in (tuple, list, set)

def _unify(x, y, s, **fns):
    # print 'Unify: ', x, y, s
    if s == None:
        pass
    elif x == y:
        yield s
    elif isinstance(x, (Variable, CondVariable)):
        for x in _unify_var(x, y, s, **fns): yield x
    elif isinstance(y, (Variable, CondVariable)):
        for x in _unify_var(y, x, s, **fns): yield x
    elif isinstance(x, Compound) and isinstance(y, Compound):
        for sop in _unify(x.op, y.op, s, **fns):
            if sop == None:
                pass
            elif len(x.args) == len(y.args):
                for x in _unify(x.args, y.args, sop, **fns): yield x
            elif is_associative(x) and is_associative(y):
                a, b = minmax(x, y)
                if is_commutative(x) and is_commutative(y):
                    combinations = combinations_comm(a.args, b.args)
                else:
                    combinations = combinations_assoc(a.args, b.args)
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
    elif (isinstance(var, CondVariable) and var.valid(fns['construct'])(x)
        or isinstance(var, Variable)):
        yield assoc(s, var, x)

def occur_check(var, x):
    "Return true if var occurs anywhere in x."
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

def combinations_assoc(A, B):
    """ A is small, B is Big

    """
    assert len(A) <= len(B)
    if len(A) == len(B):
        yield A, B
    else:
        for part in partitions(range(len(B)), len(A)):
            yield A, partition(B, part)

def combinations_comm(A, B):
    # TODO
    return (A, B)

def minmax(A, B):
    if len(A.args) < len(B.args):
        return A, B
    else:
        return B, A


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

def partitions(lista,bins):
    """
    Taken from StackOverflow. Written by @EnricoGiampieri.

    See the following link for discussion
    http://stackoverflow.com/questions/13131491/partition-n-items-into-k-bins-in-python-lazily
    """
    if len(lista)==1 or bins==1:
        yield [lista]
    elif len(lista)>1 and bins>1:
        for i in range(1,len(lista)):
            for part in partitions(lista[i:],bins-1):
                if len([lista[:i]]+part)==bins:
                    yield [lista[:i]]+part

def is_associative(x):
    from sympy import Add, Mul
    return (isinstance(x, Compound) and (x.op in {'Add', 'Mul'}
         or x.op in (Add, Mul)))
    # TODO: need a more general way to test for associativity

def is_commutative(x):
    # TODO
    return False
