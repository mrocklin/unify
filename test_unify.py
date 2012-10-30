from unify import *
from unify import _unify

a,b,c = 'abc'
w,x,y,z = map(Variable, 'wxyz')

C = Compound

def test_basic():
    print list(_unify(a, x, {}))
    assert list(_unify(a, x, {})) == [{x: a}]
    assert list(_unify(1, x, {})) == [{x: 1}]
    assert list(_unify(a, a, {})) == [{}]
    assert list(_unify((w, x), (y, z), {})) == [{w: y, x: z}]
    assert list(_unify(x, (a, b), {})) == [{x: (a, b)}]

    assert list(_unify((a, b), (x, x), {})) == []
    assert list(_unify((y, z), (x, x), {}))!= []
    assert list(_unify((a, (b, c)), (a, (x, y)), {})) == [{x: b, y: c}]

def test_ops():
    assert list(_unify(C('Add', (a,b,c)), C('Add', (a,x,y)), {})) == \
            [{x:b, y:c}]
    assert list(_unify(C('Add', (C('Mul', (1,2)), b,c)), C('Add', (x,y,c)), {})) == \
            [{x: C('Mul', (1,2)), y:b}]

def test_associative():
    c1 = C('Add', (1,2,3))
    c2 = C('Add', (x,y))
    result = list(_unify(c1, c2, {}))
    assert tuple(_unify(c1, c2, {})) == ({x: 1, y: C('Add', (2, 3))},
                                         {x: C('Add', (1, 2)), y: 3})

def test_commutative():
    c1 = C('CAdd', (1,2,3))
    c2 = C('CAdd', (x,y))
    result = list(_unify(c1, c2, {}))
    print result
    assert {x: 1, y: C('CAdd', (2, 3))} in result
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
