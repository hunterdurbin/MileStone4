

# TODO: make test method
def insert_ais_message_tuple_builder(msg_content: dict):
    keys = ""
    values = ""
    if 'Timestamp' in msg_content:
        keys = f"{keys}, Timestamp"
        values = f"{values}, '{msg_content['Timestamp']}'"
    if 'MMSI' in msg_content:
        keys = f"{keys}, MMSI"
        values = f"{values}, {msg_content['MMSI']}"
    if 'Class' in msg_content:
        keys = f"{keys}, Class"
        values = f"{values}, '{msg_content['Class']}'"

    if keys == "":
        return "", ""

    keys = keys[2:]
    values = values[2:]
    return keys, values


# TODO: make test method
def insert_position_report_tuple_builder(msg_content: dict):
    keys = ""
    values = ""
    if 'Status' in msg_content:
        keys = f"{keys}, NavigationalStatus"
        values = f"{values}, '{msg_content['Status']}'"
    if 'Longitude' in msg_content:
        keys = f"{keys}, Longitude"
        values = f"{values}, {msg_content['Longitude']}"
    if 'Latitude' in msg_content:
        keys = f"{keys}, Latitude"
        values = f"{values}, {msg_content['Latitude']}"
    if 'RoT' in msg_content:
        keys = f"{keys}, RoT"
        values = f"{values}, {msg_content['RoT']}"
    if 'SoG' in msg_content:
        keys = f"{keys}, SoG"
        values = f"{values}, {msg_content['SoG']}"
    if 'CoG' in msg_content:
        keys = f"{keys}, CoG"
        values = f"{values}, {msg_content['CoG']}"
    if 'Heading' in msg_content:
        keys = f"{keys}, Heading"
        values = f"{values}, {msg_content['Heading']}"

    if keys == "":
        return "", ""

    keys = keys[2:]
    values = values[2:]
    return keys, values


def insert_static_data_tuple_builder(msg_content: dict):
    keys = ""
    values = ""
    if 'IMO' in msg_content:
        if msg_content['IMO'] != 'Unknown':
            keys = f"{keys}, AISIMO"
            values = f"{values}, {msg_content['IMO']}"
    if 'CallSign' in msg_content:
        keys = f"{keys}, CallSign"
        values = f"{values}, '{msg_content['CallSign']}'"
    if 'Name' in msg_content:
        keys = f"{keys}, Name"
        values = f"{values}, '{msg_content['Name']}'"
    if 'VesselType' in msg_content:
        keys = f"{keys}, VesselType"
        values = f"{values}, '{msg_content['VesselType']}'"
    if 'CargoType' in msg_content:
        keys = f"{keys}, CargoType"
        values = f"{values}, '{msg_content['CargoType']}'"
    if 'Length' in msg_content:
        keys = f"{keys}, Length"
        values = f"{values}, {msg_content['Length']}"
    if 'Breadth' in msg_content:
        keys = f"{keys}, Breadth"
        values = f"{values}, {msg_content['Breadth']}"
    if 'Draught' in msg_content:
        keys = f"{keys}, Draught"
        values = f"{values}, {msg_content['Draught']}"
    if 'Destination' in msg_content:
        keys = f"{keys}, AISDestination"
        values = f"{values}, '{msg_content['Destination']}'"
    if 'ETA' in msg_content:
        keys = f"{keys}, ETA"
        values = f"{values}, '{msg_content['ETA']}'"

    if keys == "":
        return "", ""

    keys = keys[2:]
    values = values[2:]
    return keys, values