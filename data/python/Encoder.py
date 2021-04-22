import json


def encode_json(**kwargs):
    """
    Take in any number of key arguments and return a json string

    :param **kwargs: Any number of key arguments
    :returns: document containing the kwargs
    :return type: json
    """
    return json.dumps(encode(**kwargs))


def encode(**kwargs):
    """
    Take in any number of key arguments and return a json string

    :param **kwargs: Any number of key arguments
    :returns: document containing the kwargs
    :return type: dict
    """
    _dict = dict()
    for item, value in kwargs.items():
        _dict[item] = value
    return _dict


def encode_batch_dict(batch, *args):
    """
    Encodes a batch of identical structured iterables. Uses args to map each value to the iterable value.
    e.g.
    encode_batch([[10, 20], [40, 60]], 'foo', 'bar') -> [{'foo': 10, 'bar': 20}, {'foo': 40, 'bar': 60}]
    encode_batch([[10], [40]], 'foo') -> [{'foo': 10}, {'foo': 40}]

    :param batch: Arrays or Tuples of identical size
    :param args: any number of string arguments wanting to map for each iterable in the batch
    :returns: array containing documents of identical structure
    :return type: array
    """
    size = len(batch[0])

    result = []
    for _list in batch:
        if size != len(_list):
            raise Exception('Batch sizes of the arrays are not equal')

        result.append(encode(**dict(zip((arg for arg in args), _list))))

    return result



































