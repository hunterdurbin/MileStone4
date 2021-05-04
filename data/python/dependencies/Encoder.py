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

    :param json_doc: (str) - a string format of a json document
    :returns: python dictionary
    :return type: dict
    """
    return json.loads(json_doc)


def extract_message(json_doc):
    """
    Extracts an AIS message. Can either pass a static message or position report.
    If a position report is passed, return value is that of the function 'extract_message_position()'
    If static data is passed, return value is that of the function 'extract_message_static()'
    If the message type is neither of the above, an empty dictionary will be returned.

    :param json_doc: Static data json or Position report json
    :returns: dictionary containing the static data, position report, or an empty dict
    :return type: dict
    """
    if type(json_doc) == str:
        _dict = decode(json_doc)
    else:
        _dict = json_doc
    if _dict['MsgType'] == 'position_report':
        return extract_message_position(_dict)
    elif _dict['MsgType'] == 'static_data':
        return extract_message_static(_dict)
    return {}


def extract_message_position(pos_report: dict):
    """
    Given a raw position report as a dictionary, a dictionary of correctly parsed data
    will be returned.
    The format will be that of:
    {'MMSI': ..., 'Timestamp': ..., 'Class': ..., 'Latitude': ..., 'Longitude':...,
    'Status: ..., 'RoT': ..., 'SoG': ..., 'CoG': ..., 'Heading': ...}
    If a key is not present in the pos_report, the key-value will not be returned in the resulting dict.

    :param pos_report: (dict) - position report dictionary
    :returns: parsed position report dictionary
    :return type: dict
    """
    if type(pos_report) != dict:
        raise TypeError('Expected arg \'pos_report\' to be type dict in \'extract_message_position\'')
    if pos_report['MsgType'] != 'position_report':
        raise ValueError('Expected arg \'pos_report\' to be a position report')

    result = dict()
    result['MsgType'] = 'position_report'
    if 'MMSI' in pos_report:
        result['MMSI'] = pos_report['MMSI']
    if 'Timestamp' in pos_report:
        result['Timestamp'] = extract_timestamp(pos_report['Timestamp'])
    if 'Class' in pos_report:
        result['Class'] = pos_report['Class']
    if 'Position' in pos_report:
        result['Latitude'] = pos_report['Position']['coordinates'][0]
        result['Longitude'] = pos_report['Position']['coordinates'][1]
    if 'Status' in pos_report:
        result['Status'] = pos_report['Status']
    if 'RoT' in pos_report:
        result['RoT'] = pos_report['RoT']
    if 'SoG' in pos_report:
        result['SoG'] = pos_report['SoG']
    if 'CoG' in pos_report:
        result['CoG'] = pos_report['CoG']
    if 'Heading' in pos_report:
        result['Heading'] = pos_report['Heading']
    return result


def extract_message_static(static_report: dict):
    """
    Given a raw static data report as a dictionary, a dictionary of correctly parsed data
    will be returned.
    The format will be that of:
    {'MMSI': ..., 'IMO': ..., 'Timestamp': ..., 'Class': ..., 'CallSign': ...,
    'Name': ..., 'VesselType': ..., 'CargoType': ..., 'Length': ..., 'Breadth': ...,
    'Destination': ..., 'ETA': ...}
    If a key is not present in the pos_report, the key-value will not be returned in the resulting dict.

    :param static_report: (dict) - static data dictionary
    :returns: parsed static data report dictionary
    :return type: dict
    """
    if type(static_report) != dict:
        raise TypeError('Expected arg \'static_report\' to be type dict in \'extract_message_position\'')
    if static_report['MsgType'] != 'static_data':
        raise ValueError('Expected arg \'static_report\' to be a static data report')

    result = dict()
    result['MsgType'] = 'static_data'
    if 'MMSI' in static_report:
        result['MMSI'] = static_report['MMSI']
    if 'IMO' in static_report:
        result['IMO'] = static_report['IMO']
    if 'Timestamp' in static_report:
        result['Timestamp'] = extract_timestamp(static_report['Timestamp'])
    if 'Class' in static_report:
        result['Class'] = static_report['Class']
    if 'CallSign' in static_report:
        result['CallSign'] = static_report['CallSign']
    if 'Name' in static_report:
        result['Name'] = static_report['Name']
    if 'VesselType' in static_report:
        result['VesselType'] = static_report['VesselType']
    if 'CargoType' in static_report:
        result['CargoType'] = static_report['CargoType']
    if 'Length' in static_report:
        result['Length'] = static_report['Length']
    if 'Breadth' in static_report:
        result['Breadth'] = static_report['Breadth']
    if 'Draught' in static_report:
        result['Draught'] = static_report['Draught']
    if 'Destination' in static_report:
        result['Destination'] = static_report['Destination']
    if 'ETA' in static_report:
        result['ETA'] = extract_timestamp(static_report['ETA'])
    return result


def default(o):
    """
    Helper method used for json.dumps function
    """
    if isinstance(o, Decimal):
        return str(o)
    raise TypeError("Object of type {} is not JSON serializable".format(type(o).__name__))


def extract_timestamp(timestamp_raw: str):
    """
    Takes a raw timestamp, e.g. "2020-11-18T00:00:00.000Z"
    and returns a MySQL formatted timestamp, e.g. "2020-11-18 00:00:00"

    :param timestamp_raw: (str) - raw timestamp from ais messages
    :returns: a MySQL formatted timestamp
    :return type: str
    """
    if type(timestamp_raw) != str:
        raise TypeError('arg \'timestamp_raw\' in \'extract_timestamp\' should be type str')
    if len(timestamp_raw) != 24:
        raise ValueError('arg \'timestamp_raw\' should be exactly 24 characters')

    timestamp = timestamp_raw.replace('T', ' ').replace('Z', '')[0:19]
    return timestamp

