from unify import *
from unify import _unify

a,b,c = 'abc'
w,x,y,z = map(Variable, 'wxyz')

C = Compound

def is_associative(x):
    return isinstance(x, Compound) and (x.op in {'Add', 'Mul', 'CAdd', 'CMul'})
def is_commutative(x):
    return isinstance(x, Compound) and (x.op in {'CAdd', 'CMul'})


def unify(a, b, d):
    return _unify(a, b, d, is_associative=is_associative,
                           is_commutative=is_commutative)

def test_basic():
    print list(unify(a, x, {}))
    assert list(unify(a, x, {})) == [{x: a}]
    assert list(unify(1, x, {})) == [{x: 1}]
    assert list(unify(a, a, {})) == [{}]
    assert list(unify((w, x), (y, z), {})) == [{w: y, x: z}]
    assert list(unify(x, (a, b), {})) == [{x: (a, b)}]

    assert list(unify((a, b), (x, x), {})) == []
    assert list(unify((y, z), (x, x), {}))!= []
    assert list(unify((a, (b, c)), (a, (x, y)), {})) == [{x: b, y: c}]

def test_ops():
    assert list(unify(C('Add', (a,b,c)), C('Add', (a,x,y)), {})) == \
            [{x:b, y:c}]
    assert list(unify(C('Add', (C('Mul', (1,2)), b,c)), C('Add', (x,y,c)), {})) == \
            [{x: C('Mul', (1,2)), y:b}]

def test_associative():
    c1 = C('Add', (1,2,3))
    c2 = C('Add', (x,y))
    result = list(unify(c1, c2, {}))
    assert tuple(unify(c1, c2, {})) == ({x: 1, y: C('Add', (2, 3))},
                                         {x: C('Add', (1, 2)), y: 3})

def test_commutative():
    c1 = C('CAdd', (1,2,3))
    c2 = C('CAdd', (x,y))
    result = list(unify(c1, c2, {}))
    print result
    assert  {x: 1, y: C('CAdd', (2, 3))} in result
    assert ({x: 2, y: C('CAdd', (1, 3))} in result or
            {x: 2, y: C('CAdd', (3, 1))} in result)

def test_combinations_assoc():
    print list(allcombinations((1,2,3), (a,b), True))
    assert set(allcombinations((1,2,3), (a,b), True)) == \
            {(((1, 2), (3,)), (a, b)), (((1,), (2, 3)), (a, b))}

def test_combinations_comm():
    print list(allcombinations((1,2,3), (a,b), None))
    assert set(allcombinations((1,2,3), (a,b), None)) == \
            {(((1,), (2, 3)), ('a', 'b')), (((2,), (3, 1)), ('a', 'b')),
             (((3,), (1, 2)), ('a', 'b')), (((1, 2), (3,)), ('a', 'b')),
             (((2, 3), (1,)), ('a', 'b')), (((3, 1), (2,)), ('a', 'b'))}

def test_CondVariable():
    expr = C('CAdd', (1, 2))
    x = Variable('x')
    y = CondVariable('y', lambda a: a % 2 == 0)
    z = CondVariable('z', lambda a: a > 3)
    pattern = C('CAdd', (x, y))
    assert list(unify(expr, pattern, {})) == \
            [{x: 1, y: 2}]

    z = CondVariable('z', lambda a: a > 3)
    pattern = C('CAdd', (z, y))

    assert list(unify(expr, pattern, {})) == []
