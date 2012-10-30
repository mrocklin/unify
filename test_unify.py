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

