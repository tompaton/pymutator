=========
PyMutator
=========

Mutate nested Python objects using a method inspired by SolidJS's
setState function for updating stores.

https://www.solidjs.com/docs/latest/api#updating-stores


Examples
========

update lists by index

    >>> from pymutator import mutate
    >>> mutate([1, 2, 3, 4, 5], 3, 'D')
    [1, 2, 3, 'D', 5]

update lists by list of indices

    >>> mutate([1, 2, 3, 4, 5], [1, 3], 'D')
    [1, 'D', 3, 'D', 5]

update lists by filter predicate

    >>> mutate([1, 2, 3, 4, 5], lambda i: i%2, 'odd')
    ['odd', 2, 'odd', 4, 'odd']

update list with computed value

    >>> mutate([1, 2, 3, 4, 5], 3, lambda i: f'D{i}')
    [1, 2, 3, 'D4', 5]

update dict

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, 'b', 'B')
    {'a': 1, 'b': 'B', 'c': 3}

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, b='B')
    {'a': 1, 'b': 'B', 'c': 3}

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, {'b': 'B'})
    {'a': 1, 'b': 'B', 'c': 3}

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, ['b', 'x'], 'B')
    {'a': 1, 'b': 'B', 'c': 3, 'x': 'B'}

update dict with filter predicate

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, lambda i: i%2, 'odd')
    {'a': 'odd', 'b': 2, 'c': 'odd'}

update dict with computed value

    >>> mutate({'a': 1, 'b': 2, 'c': 3}, 'b', lambda i: f'B{i}')
    {'a': 1, 'b': 'B2', 'c': 3}

update object

    >>> class O:
    ...     def __init__(self): self.a = 1
    >>> o = O()
    >>> mutate(o, 'a', 2) and o.a
    2

    >>> mutate(o, a=3) and o.a
    3

    >>> mutate(o, {'a': 4}) and o.a
    4

    >>> mutate(o, 'a', lambda i: i+1) and o.a
    5

updating nested objects

    >>> store = {
    ...    'todos': [
    ...            {'task': 'Finish work', 'completed': False},
    ...            {'task': 'Go grocery shopping', 'completed': False},
    ...            {'task': 'Make dinner', 'completed': False},
    ...        ]
    ...    }

    >>> mutate(store, 'todos', [0, 2], 'completed', True)
    {'todos': [{'task': 'Finish work', 'completed': True}, {'task': 'Go grocery shopping', 'completed': False}, {'task': 'Make dinner', 'completed': True}]}

    >>> mutate(store, 'todos', lambda todo: todo['completed'],
    ...        'task', lambda t: t + '!')
    {'todos': [{'task': 'Finish work!', 'completed': True}, {'task': 'Go grocery shopping', 'completed': False}, {'task': 'Make dinner!', 'completed': True}]}


Running tests
=============

    $ pytest --doctest_glob="*.rst"
