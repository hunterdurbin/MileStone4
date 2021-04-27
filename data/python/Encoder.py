import json
from decimal import Decimal


def encode(**kwargs):
    """
    Take in any number of key arguments and return a json string
    e.g.
    encode(**{foo: 14, bar: 94}) -> {foo: 14, bar: 94}
    encode(foo=14, bar=94) -> {foo: 14, bar: 94}

    Note that specified order permutation may not apply since dictionary ordering is not guaranteed.

    :returns: document containing the kwargs
    :return type: json
    """
    _dict = dict()
    for key, value in kwargs.items():
        _dict[key] = value
    return json.dumps(_dict, default=default)


def decode(json_doc):
    """
    Decode a document into a python dictionary

    :param json_doc:
    :returns: python dictionary
    :return type: dict
    """
    return json.loads(json_doc)


def default(o):
    if isinstance(o, Decimal):
        return str(o)
    raise TypeError("Object of type {} is not JSON serializable".format(type(o).__name__))
