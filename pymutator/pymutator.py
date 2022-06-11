def mutate(obj, *path, **kwargs):
    """update obj items/keys/attributes

    path:
      - dict
        do a shallow update of obj (dict or object)
      - key, value
        update dictionary key, list index or object attribute
      - [key, ...], value
        update list of dictionary keys, indices or object attributes
      - predicate, value
        update dictionary items or list entries matching predicate

      value may be a function that will be passed the old value and
      returns the new value.

      nested objects can be updated by specifying the path (keys,
      indices, predicates) to the item to change.

    kwargs:
      - do a shallow update the dict/object

    """
    if kwargs:
        # passing kwargs is the same as passing a dict
        path = list(path)
        path.append(kwargs)

    if len(path) > 2:
        # nested setting
        key, *rest = path
        for key2 in _select(obj, key):
            mutate(_get(obj, key2), *rest)

    elif len(path) == 1:
        # shallow update a dict/object from a dict
        value = path[0]
        if isinstance(value, dict):
            if isinstance(obj, dict):
                obj.update(value)
            else:
                for k, v in value.items():
                    setattr(obj, k, v)

    else:
        key, value_ = path
        if callable(value_):
            value = value_
        else:
            # function that is passed previous value and returns new value
            value = lambda v: value_

        for key2 in _select(obj, key):
            _set(obj, key2, value)

    return obj


def _select(obj, key):
    """iterate over matching keys in the given object

    key may be a single key, index or attribute, or a list of keys or
    indices, or a predicate function
    """
    if isinstance(key, list) and isinstance(obj, (dict, list)):
        # iterate over a list of indices or dictionary keys
        for i in key:
            yield i
        return

    if isinstance(obj, list) and callable(key):
        # filter list items
        for i, v in enumerate(obj):
            if key(v):
                yield i
        return

    if isinstance(obj, dict) and callable(key):
        # filter dict items
        for k, v in obj.items():
            if key(v):
                yield k
        return

    # regular key, index, attribute or slice
    yield key


def _get(obj, key):
    """get the item from the object

    list -> index, dict -> key, object -> attribute
    """
    if isinstance(obj, list):
        return obj[key]
    elif isinstance(obj, dict):
        return obj.get(key)
    else:
        return getattr(obj, key, None)


def _set(obj, key, value):
    """set the object key to the given value

    list item by index, dict value by key, object attribute

    value is a function that takes the old value and returns the new value.
    """
    if isinstance(obj, list):
        obj[key] = value(obj[key])
    elif isinstance(obj, dict):
        obj[key] = value(obj.get(key))
    else:
        setattr(obj, key, value(getattr(obj, key, None)))


# TODO: delete values - no undefined in python, maybe use a sentinel value? or slices
