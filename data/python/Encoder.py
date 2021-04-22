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
    return json.dumps(kwargs, default=default)


def encode_multiple_pos(mmsi, positions, imo):
    """
    Encode a document in the form of {MMSI: ..., Positions: [{"lat": ..., "long": ...}], "IMO": ... }

    :param mmsi: (int) - A ship's mmsi
    :param positions: (list) - A list containing lists of position reports. Each list should be the form of [lat, long]
    :param imo: (int) - A ship's imo
    :returns: A document
    :return type: json
    """
    result = {
        'MMSI': mmsi,
        'Positions': [],
        'IMO': imo
    }
    for position_report in positions:
        result['Positions'].append({'lat': position_report[0], 'long': position_report[1]})
    return json.dumps(result, default=default)


def encode_pos(mmsi, position, imo):
    """
    Encode a document in the form of {MMSI: ..., "lat": ..., "long": ..., "IMO": ... }

    :param mmsi: (int) - A ship's mmsi
    :param position: A list containing a position report. Should be the form of [lat, long]
    :param imo: (int) - A ship's imo
    :returns: A document
    :return type: json
    """
    result = {
        'MMSI': mmsi,
        'lat': position[0],
        'long': position[1],
        'IMO': imo
    }
    return json.dumps(result, default=default)


def default(o):
    if isinstance(o, Decimal):
        return str(o)
    raise TypeError("Object of type {} is not JSON serializable".format(type(o).__name__))
