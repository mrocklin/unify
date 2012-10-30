from unify import *
from unify import _unify

a,b,c = 'abc'
w,x,y,z = map(Variable, 'wxyz')

C = Compound

def test_basic():
    assert _unify(a, x, {}) == {x: a}
    assert _unify(1, x, {}) == {x: 1}
    assert _unify(a, a, {}) == {}
    assert _unify((w, x), (y, z), {}) == {w: y, x: z}
    assert _unify(x, (a, b), {}) == {x: (a, b)}

    assert _unify((a, b), (x, x), {}) == None
    assert _unify((y, z), (x, x), {}) != None
    assert _unify((a, (b, c)), (a, (x, y)), {}) == {x: b, y: c}

def test_ops():
    assert _unify(C('Add', (a,b,c)), C('Add', (a,x,y)), {}) == {x:b, y:c}
    assert _unify(C('Add', (C('Mul', (1,2)), b,c)), C('Add', (x,y,c)), {}) == \
            {x: C('Mul', (1,2)), y:b}

