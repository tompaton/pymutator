import pytest
from pymutator import mutate


@pytest.fixture
def list1():
    return [1, 2, 3, 4, 5]


def test_mutate_list1(list1):
    assert mutate(list1, 3, 'D') is list1
    assert list1 == [1, 2, 3, 'D', 5]


def test_mutate_list2(list1):
    assert mutate(list1, [1, 3], 'x') is list1
    assert list1 == [1, 'x', 3, 'x', 5]


def test_mutate_list3(list1):
    assert mutate(list1, lambda i: i%2, 'odd') is list1
    assert list1 == ['odd', 2, 'odd', 4, 'odd']


def test_mutate_list4(list1):
    assert mutate(list1, 3, None) is list1
    assert list1 == [1, 2, 3, None, 5]


def test_mutate_list5(list1):
    assert mutate(list1, 3, lambda v: f'D{v}') is list1
    assert list1 == [1, 2, 3, 'D4', 5]


def test_mutate_list6(list1):
    assert mutate(list1, slice(1, 3), 'x') is list1
    assert list1 == [1, 'x', 4, 5]


def test_mutate_list7(list1):
    assert mutate(list1, slice(1, 3), ['x', 'y']) is list1
    assert list1 == [1, 'x', 'y', 4, 5]


def test_mutate_list8(list1):
    assert mutate(list1, slice(1, 3), []) is list1
    assert list1 == [1, 4, 5]


def test_mutate_list9(list1):
    assert mutate(list1, slice(1, 3), 'xy') is list1
    assert list1 == [1, 'x', 'y', 4, 5]


def test_mutate_list10(list1):
    assert mutate(list1, slice(1, 3), ['xy']) is list1
    assert list1 == [1, 'xy', 4, 5]


def test_mutate_list11(list1):
    assert mutate(list1, slice(2), []) is list1
    assert list1 == [3, 4, 5]


def test_mutate_list12(list1):
    assert mutate(list1, slice(2, 3), []) is list1
    assert list1 == [1, 2, 4, 5]


@pytest.fixture
def dict1():
    return {'a': 1, 'b': 2, 'c': 3}

def test_mutate_dict1(dict1):
    assert mutate(dict1, 'b', 'B') is dict1
    assert dict1 == {'a': 1, 'b': 'B', 'c': 3}


def test_mutate_dict2(dict1):
    assert mutate(dict1, {'a': 'A', 'x': 'X'}) is dict1
    assert dict1 == {'a': 'A', 'b': 2, 'c': 3, 'x': 'X'}


def test_mutate_dict3(dict1):
    assert mutate(dict1, ['b', 'x'], 'X') is dict1
    assert dict1 == {'a': 1, 'b': 'X', 'c': 3, 'x': 'X'}


def test_mutate_dict4(dict1):
    assert mutate(dict1, a='A', x='X') is dict1
    assert dict1 == {'a': 'A', 'b': 2, 'c': 3, 'x': 'X'}


def test_mutate_dict6(dict1):
    assert mutate(dict1, 'b', lambda v: f'B{v}') is dict1
    assert dict1 == {'a': 1, 'b': 'B2', 'c': 3}


@pytest.fixture
def obj1():
    class O1:
        def __init__(self):
            self.a = 1
    return O1()

def test_mutate_obj1(obj1):
    assert mutate(obj1, 'a', 'A') is obj1
    assert mutate(obj1, 'b', 'B') is obj1
    assert obj1.a == 'A'
    assert obj1.b == 'B'


def test_mutate_obj2(obj1):
    assert mutate(obj1, {'a': 'A', 'b': 'B'}) is obj1
    assert obj1.a == 'A'
    assert obj1.b == 'B'


def test_mutate_obj3(obj1):
    assert mutate(obj1, a='A', b='B') is obj1
    assert obj1.a == 'A'
    assert obj1.b == 'B'


def test_mutate_obj4(obj1):
    assert mutate(obj1, 'a', lambda v: v + 1) is obj1
    assert obj1.a == 2


@pytest.fixture
def dict2():
    return {'a': 1, 'b': {'c': 3}}


def test_mutate_deep1(dict2):
    assert mutate(dict2, 'b', 'c', 'x') is dict2
    assert dict2 == {'a': 1, 'b': {'c': 'x'}}


def test_mutate_deep2():
    d = {'a': 1, 'b': {'c': [2, 3, {'d': 4}], 'e': {'f': 5}}}

    assert mutate(d, 'b', 'c', 0, 'x') is d
    assert d == {'a': 1, 'b': {'c': ['x', 3, {'d': 4}], 'e': {'f': 5}}}


def test_mutate_deep3(dict2):
    assert mutate(dict2, 'b', 'x', 'X') is dict2
    assert dict2 == {'a': 1, 'b': {'c': 3, 'x': 'X'}}


def test_mutate_deep4():
    store = {
        'todos': [
            {'task': 'Finish work', 'completed': False},
            {'task': 'Go grocery shopping', 'completed': False},
            {'task': 'Make dinner', 'completed': False},
        ]
    }

    assert mutate(store, 'todos', [0, 2], 'completed', True) is store
    assert store == {
        'todos': [
            {'task': 'Finish work', 'completed': True},
            {'task': 'Go grocery shopping', 'completed': False},
            {'task': 'Make dinner', 'completed': True},
        ]
    }

    assert mutate(store, 'todos', lambda todo: todo['completed'],
                  'task', lambda t: t + '!') is store
    assert store == {
        'todos': [
            {'task': 'Finish work!', 'completed': True},
            {'task': 'Go grocery shopping', 'completed': False},
            {'task': 'Make dinner!', 'completed': True},
        ]
    }


def test_mutate_deep5():
    d = {'a': {'update': True, 'value': 1},
         'b': {'update': False, 'value': 2},
         'c': {'update': True, 'value': 3}}

    assert mutate(d, lambda v: v['update'], 'value', lambda value: value + 1) is d
    assert d == {'a': {'update': True, 'value': 2},
                 'b': {'update': False, 'value': 2},
                 'c': {'update': True, 'value': 4}}


def test_mutate_deep6():
    d = {'a': {'c': 2}, 'b': {'c': 3}}

    assert mutate(d, ['a', 'b'], 'c', 'X') is d
    assert d == {'a': {'c': 'X'}, 'b': {'c': 'X'}}
