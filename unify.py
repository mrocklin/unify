from collections import namedtuple
Compound = namedtuple('Compound', 'op args')
Variable = namedtuple('Variable', 'arg')

def iterable(x):
    """ Is x a traditional iterable? """
    return type(x) in (tuple, list, set)

def _unify(x, y, s):
    print 'Unify: ', x, y, s
    if s == None:
        pass
    elif x == y:
        yield s
    elif isinstance(x, Variable):
        for x in _unify_var(x, y, s): yield x
    elif isinstance(y, Variable):
        for x in _unify_var(y, x, s): yield x
    elif isinstance(x, Compound) and isinstance(y, Compound):
        for sop in _unify(x.op, y.op, s):
            if sop == None:
                pass
            elif len(x) == len(y):
                for x in _unify(x.args, y.args, sop): yield x

            elif is_associative(x) and is_associative(y):
                for xxargs, yyargs in combinations_assoc(x.args, y.args):
                    xx = [unpack(Compound(x.op, arg)) for arg in xxargs]
                    yy = [unpack(Compound(y.op, arg)) for arg in yyargs]
                    for x in _unify(xx, yy, sop): yield x

    elif iterable(x) and iterable(y) and len(x) == len(y):
        for shead in _unify(x[0], y[0], s):
            for x in _unify(x[1:], y[1:], shead):
                yield x
    else:
        pass

def _unify_var(var, x, s):
    print 'UnVar: ', var, x, s
    if var in s:
        for x in _unify(s[var], x, s): yield x
    elif occur_check(var, x):
        pass
    else:
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

