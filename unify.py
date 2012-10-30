from collections import namedtuple
Compound = namedtuple('Compound', 'op args')
Variable = namedtuple('Variable', 'arg')

def iterable(x):
    """ Is x a traditional iterable? """
    return type(x) in (tuple, list, set)

def _unify(x, y, s):
    print x, y, s
    if s == None:
        return None
    elif x == y:
        return s
    elif isinstance(x, Variable):
        return _unify_var(x, y, s)
    elif isinstance(y, Variable):
        return _unify_var(y, x, s)
    elif isinstance(x, Compound) and isinstance(y, Compound):
        return _unify(x.args, y.args, _unify(x.op, y.op, s))
        if is_commutative(x) and is_commutative(y):
            pass
        elif is_associative(x) and is_associative(y):
            pass
        combinations = [[x,y]] # Kludge
        for xx, yy in combinations:
            pass
            # Yield
    elif iterable(x) and iterable(y) and len(x) == len(y):
        return _unify(x[1:], y[1:], _unify(x[0], y[0], s))
    else:
        return None

def _unify_var(var, x, s):
    if var in s:
        return _unify(s[var], x, s)
    elif occur_check(var, x):
        return None
    else:
        return assoc(s, var, x)

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

def combinations_assoc(A, B):
    if len(A) == len(B):
        yield A, B
    else:
        if len(A) < len(B):
            small, big = A, B
        else:
            small, big = B, A

        for part in partitions(range(len(big)), len(small)):
            yield small, partition(big, part)


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
    if len(lista)==1 or bins==1:
        yield [lista]
    elif len(lista)>1 and bins>1:
        for i in range(1,len(lista)):
            for part in partitions(lista[i:],bins-1):
                if len([lista[:i]]+part)==bins:
                    yield [lista[:i]]+part
