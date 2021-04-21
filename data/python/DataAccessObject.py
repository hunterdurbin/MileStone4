from data.python.mysqlutils import SQL_runner
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

    @staticmethod
    def insert_msg(json_data):
        # TODO: find out a way to insert the damn data

        msg_type = extract_type(json_data)
        if msg_type == 'position_report':
            mmsi, timestamp, class_, lat, long_, status, sog, cog, heading = extract_pos_report(json_data)
        elif msg_type == 'static_data':
            pass
        return 0

    @staticmethod
    def insert_msg_batch(json_data: list):
        pass

    @staticmethod
    def delete_msgs_older_5min(current_timestamp):
        pass

    @staticmethod
    def read_all_ship_positions_from_tile(tile_id):
        query = """NOT IMPLEMENTED"""
        result = SQL_runner().run(query)
        pass

    @staticmethod
    def read_last_5_ship_positions_from_mmsi(mmsi):
        """
        Read last 5 positions of given MMSI

        :param mmsi: A ship's mmsi
        :return dict:
        """
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

        docs = {'MMSI': mmsi, 'Positions': []}
        for report in result:
            docs['Positions'].append({'lat': str(report[1]), 'long': str(report[2]), 'IMO': report[0]})
        return json.dumps(docs)

    @staticmethod
    def read_ship_current_position_from_mmsi(mmsi):
        """
        Read current position of given MMSI

        :param mmsi:
        :return:
        """
        query = """
                SELECT Vessel.IMO, Position_Report.Latitude, Position_Report.Longitude
                FROM Vessel, AIS_Message, Position_Report
                WHERE Vessel.IMO=AIS_Message.Vessel_IMO
                AND AIS_Message.Id=Position_Report.AISMessage_Id
                and AIS_Message.MMSI={}
                ORDER BY Timestamp DESC
                LIMIT 1;
                """ \
            .format(mmsi)
        docs = SQL_runner().run(query)[0]

        docs = {
            'MMSI': mmsi,
            'lat': str(docs[1]),
            'long': str(docs[2]),
            'IMO': docs[0]
        }
        return json.dumps(docs)

    @staticmethod
    def read_all_ship_positions_from_port(port_id):
        """
        Read all positions of ships headed to port with given Id

        :param port_id:
        :return:
        """
        pass

    @staticmethod
    def read_all_ships_headed_to_port(port_name, country):
        pass

    @staticmethod
    def read_all_ports_from_name(port_name, country=None):
        pass

    @staticmethod
    def read_all_ship_positions_from_tile_scale3(port_name, country):
        pass

    @staticmethod
    def read_vessel_information(mmsi, imo=None, name=None, call_sign=None):
        pass

    @staticmethod
    def find_sub_map_tiles(tile_id):
        pass

    @staticmethod
    def get_tile_png(tile_id):
        pass


MySQL_DAO.insert_msg(
    '{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,"MsgType":"position_report","Position":{"type":"Point","coordinates":[55.218332,13.371672]},"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}'
    )
