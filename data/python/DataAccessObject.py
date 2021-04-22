from data.python.mysqlutils import SQL_runner
from data.python.Encoder import *
import json


#NoahConn Test Push


# Move these to own module
def extract_type(json_data):
    docs = json.loads(json_data)
    type = docs['MsgType']
    return type


def extract_pos_report(json_data):

    docs = json.loads(json_data)
    values = (docs['MMSI'],
              docs['Timestamp'],
              docs['Class'],
              docs['Position']['coordinates'][0],
              docs['Position']['coordinates'][1],
              docs['Status'],
              docs['SoG'],
              docs['CoG'],
              docs['Heading']
              )
    return values


class MySQL_DAO:

    def __init__(self, stub=False):
        self.is_stub = stub

    def insert_msg(self, json_data):
        """
        Insert an AIS message (Position Report or Static Data).

        :param json_data: A single json string of a message to insert
        :returns: 1/0 for success/failure upon message insertion.
        :return type: json
        """
        # TODO: find out a way to insert the damn data

        msg_type = extract_type(json_data)
        if msg_type == 'position_report':
            mmsi, timestamp, class_, lat, long_, status, sog, cog, heading = extract_pos_report(json_data)
        elif msg_type == 'static_data':
            pass
        return 0

    def insert_msg_batch(self, json_data: list):
        """
        Insert a batch of AIS messages (Static Data and/or Position Reports).

        :param json_data: A list of json string AIS messages to insert
        :returns: Number of insertions made.
        :return type: json
        """
        pass

    def delete_msgs_older_5min(self, current_timestamp):
        """
        Delete all AIS messages whose timestamp is more than 5 minutes older than current time.

        :param current_timestamp:
        :returns: Number of deleted AIS messages.
        :return type: json
        """
        pass

    def read_all_ship_positions_from_tile(self, tile_id):
        """
        Read all ship positions in the given tile.

        :param tile_id:
        :returns: Array of ship documents in a json string.
        :return type: json
        """

        if self.is_stub:
            if type(tile_id) == int:
                return 1
            return -1

        query = """NOT IMPLEMENTED"""
        result = SQL_runner().run(query)
        pass

    def read_last_5_ship_positions_from_mmsi(self, mmsi: int):
        """
        Read last 5 positions of given MMSI.

        :param mmsi: A ship's mmsi
        :returns: Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, "IMO": ... ]}.
        :return type: json
        """

        if self.is_stub:
            if type(mmsi) == int:
                return 1
            return -1

        # TODO: remake this query into 2 queries... 1 for getting the msgs... 1 for getting imo (if exists)
        query = """
                SELECT Vessel.IMO, Position_Report.Latitude, Position_Report.Longitude
                FROM Vessel, AIS_Message, Position_Report
                WHERE Vessel.IMO=AIS_Message.Vessel_IMO
                AND AIS_Message.Id=Position_Report.AISMessage_Id
                AND AIS_Message.MMSI={}
                ORDER BY Timestamp DESC
                LIMIT 5;
                """ \
            .format(mmsi)
        result = SQL_runner().run(query)
        imo = result[0][0]
        positions = [[pos[1], pos[2]] for pos in result]

        docs = encode_multiple_pos(mmsi, positions, imo)
        return docs

    def read_ship_current_position_from_mmsi(self, mmsi: int):
        """
        Read current position of given MMSI.

        :param mmsi: A ship's mmsi
        :returns: Position document of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ... }.
        :return type: json
        """

        if self.is_stub:
            if type(mmsi) == int:
                return 1
            return -1

        # TODO: remake this query into 2 queries... 1 for getting the msgs... 1 for getting imo (if exists)
        query = """
                SELECT Vessel.IMO, Position_Report.Latitude, Position_Report.Longitude
                FROM Vessel, AIS_Message, Position_Report
                WHERE Vessel.IMO=AIS_Message.Vessel_IMO
                AND AIS_Message.Id=Position_Report.AISMessage_Id
                AND AIS_Message.MMSI={}
                ORDER BY Timestamp DESC
                LIMIT 1;
                """ \
            .format(mmsi)
        result = SQL_runner().run(query)[0]
        imo, lat, long_ = result[0], result[1], result[2]

        docs = encode_pos(mmsi, [lat, long_], imo)
        return docs

    def read_all_ship_positions_from_port(self, port_id: int):
        """
        Read all positions of ships headed to port with given Id.

        :param port_id:
        :return: Array of position documents of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ...}.
        :return type: json
        """

        if self.is_stub:
            if type(port_id) == int:
                return 1
            return -1

        pass

    def read_all_ships_headed_to_port(self, port_name: str, country: str):
        """
        Read all positions of ships headed to given port (as read from static data, or user input).

        :param port_name:
        :param country:
        :returns: If unique matching port: array of of Position documents of the form
                    {"MMSI": ..., "lat": ..., "long": ..., "IMO": ...}.
                    Otherwise: an Array of Port documents.
        :return type:
        """

        if self.is_stub:
            if type(port_name) == str and type(country) == str:
                return 1
            return -1

        pass

    def read_all_ports_from_name(self, port_name: str, country=None):
        """
        Read all ports matching the given name and (optional) country.

        :param port_name:
        :param country:
        :returns: Array of Port documents.
        :return type: json
        """

        if self.is_stub:
            if type(port_name) == str and (type(country) == str or country is None):
                return 1
            return -1

        pass

    def read_all_ship_positions_from_tile_scale3(self, port_name: str, country: str):
        """
        Read all ship positions in the tile of scale 3 containing the given port.

        :param port_name:
        :param country:
        :returns: If unique matching port: Array of Position documents (see above).
                    Otherwise: an Array of Port documents.
        :return type: json
        """

        if self.is_stub:
            if type(port_name) == str and type(country) == str:
                return 1
            return -1

        pass

    def read_vessel_information(self, mmsi: int, imo=None, name=None, call_sign=None):
        """
        Read permanent or transient vessel information matching the given MMSI, and 0 or more additional criteria:
        IMO, Name, CallSign.

        :param mmsi:
        :param imo:
        :param name:
        :param call_sign:
        :returns: a Vessel document, with available and/or relevant properties.
        :return type: json
        """

        if self.is_stub:
            if type(mmsi) == int and (imo is None or type(imo) == int) and (name is None or type(name) == str) and (call_sign is None or type(call_sign) == str):
                return 1
            return -1

        pass

    def find_sub_map_tiles(self, tile_id: int):
        """
        Given a background map tile for zoom level 1 (2), find the 4 tiles of zoom level 2 (3) that are contained in it.

        :param tile_id:
        :returns: Array of map tile description documents.
        :return type: json
        """

        if self.is_stub:
            if type(tile_id) == int:
                return 1
            return -1

        pass

    def get_tile_png(self, tile_id: int):
        """
        Given a tile Id, get the actual tile (a PNG file).

        :param tile_id:
        :returns: binary data for the PNG file for the tile_id.
        :return type: json
        """

        if self.is_stub:
            if type(tile_id) == int:
                return 1
            return -1

        pass


# MySQL_DAO().insert_msg(
#     '{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,"MsgType":"position_report","Position":{"type":"Point","coordinates":[55.218332,13.371672]},"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}'
#     )
