from dependencies.mysqlutils import MySQLConnectionManager
from dependencies.Encoder import *
from dependencies.mysqlBuilder import *
import json, os, datetime


#NoahConn Test Push

class MySQL_DAO:

    def __init__(self, stub=False):
        self.is_stub = stub
        self.config = '../sql/connection_data.conf'

    def insert_msg_batch(self, batch: list):
        """
        Insert a batch of AIS messages (Static Data and/or Position Reports)

        :param batch: A list of dictionary AIS messages to insert
        :returns: Number of insertions made.
        :return type: json
        """

        if type(batch) != list:
            if not self.is_stub:
                print('Expected \'batch\' to be a list.')
            return -1

        for _dict in batch:
            if type(_dict) != dict:
                if not self.is_stub:
                    print('Expected every value in list \'batch\' to be of type \'dict\'.')
                return -1

        if self.is_stub:
            return len(batch)

        successes = 0
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()

            for msg_dict in batch:
                msg_dict = extract_message(msg_dict)
                ais_keys, ais_values = insert_ais_message_tuple_builder(msg_dict)
                query_ais_message = "INSERT INTO AIS_MESSAGE ({}) VALUES ({});" \
                    .format(ais_keys, ais_values)
                cursor.execute(query_ais_message)

                if 'MsgType' not in msg_dict:
                    con.rollback()
                    continue

                if msg_dict['MsgType'] == 'position_report':
                    pos_keys, pos_values = insert_position_report_tuple_builder(msg_dict)
                    query_pos_report = "INSERT INTO POSITION_REPORT " \
                                       "(AISMessage_Id, {}, LastStaticData_Id, MapView1_Id, MapView2_Id, MapView3_Id) " \
                                       "VALUES " \
                                       "(LAST_INSERT_ID(), {}, NULL, NULL, NULL, NULL);" \
                        .format(pos_keys, pos_values)
                    cursor.execute(query_pos_report)

                elif msg_dict['MsgType'] == 'static_data':
                    static_keys, static_values = insert_static_data_tuple_builder(msg_dict)
                    query_static_data = "INSERT INTO STATIC_DATA " \
                                        "(AISMessage_Id, {}, DestinationPort_Id) " \
                                        "VALUES " \
                                        "(LAST_INSERT_ID(), {}, NULL); " \
                        .format(static_keys, static_values)
                    cursor.execute(query_static_data)
                else:
                    con.rollback()
                    continue

                successes += cursor.rowcount
                con.commit()

        return successes

    def insert_msg(self, json_data: str):
        """
        Insert an AIS message (Position Report or Static Data)

        :param json_data: (str) - A single json formatted string of a message to insert
        :returns: 1/0 for success/failure upon message insertion.
        :return type: json
        """

        try:
            msg_content = extract_message(json_data)
        except Exception as e:
            if not self.is_stub:
                print(e)
            return -1

        if self.is_stub:
            return 1

        if 'MsgType' not in msg_content:
            return json.dumps(0)  # message was not successfully inserted

        ais_keys, ais_values = insert_ais_message_tuple_builder(msg_content)
        query_ais_message = """INSERT INTO AIS_MESSAGE ({})VALUES ({});"""\
            .format(ais_keys, ais_values)

        try:
            with MySQLConnectionManager(self.config) as con:
                cursor = con.cursor()
                cursor.execute(query_ais_message)

                if msg_content['MsgType'] == 'position_report':
                    pos_keys, pos_values = insert_position_report_tuple_builder(msg_content)
                    query_pos_report = "INSERT INTO POSITION_REPORT " \
                                       "(AISMessage_Id, {}, LastStaticData_Id, MapView1_Id, MapView2_Id, MapView3_Id) " \
                                       "VALUES " \
                                       "(LAST_INSERT_ID(), {}, NULL, NULL, NULL, NULL);" \
                        .format(pos_keys, pos_values)

                    cursor.execute(query_pos_report)
                elif msg_content['MsgType'] == 'static_data':
                    static_keys, static_values = insert_static_data_tuple_builder(msg_content)
                    query_static_data = "INSERT INTO STATIC_DATA " \
                                        "(AISMessage_Id, {}, DestinationPort_Id) " \
                                        "VALUES " \
                                        "(LAST_INSERT_ID(), {}, NULL); "\
                        .format(static_keys, static_values)
                    cursor.execute(query_static_data)
                con.commit()
        except Exception as e:
            print(e)
            return json.dumps(0)
        return json.dumps(1)

    def delete_msgs_older_5min(self, current_timestamp: str):
        """
        Delete all AIS messages whose timestamp is more than 5 minutes older than current time

        :param current_timestamp: (str) - Current timestamp in MySQL format or in python format
        :returns: Number of deletions. This includes the sum of AIS_MESSAGE along with POSITION_REPORT rows and STATIC_DATA rows. (Basically the return number is double the AIS_MESSAGE rows deleted)
        :return type: json
        """

        if type(current_timestamp) != str:
            return -1
        if len(current_timestamp) != 24 and len(current_timestamp) != 19:
            return -1

        timestamp = current_timestamp
        if len(current_timestamp) == 24:
            timestamp = extract_timestamp(current_timestamp)

        if self.is_stub:
            return 1

        delta = datetime.timedelta(minutes=5)
        date = datetime.datetime.strptime(timestamp, '%Y-%m-%d %H:%M:%S')
        timestamp_minus_5_min = date - delta

        query_temp_tables = """
            CREATE TEMPORARY TABLE OLD_POSITIONS 
            SELECT AISMessage_Id 
            FROM POSITION_REPORT, AIS_MESSAGE 
            WHERE POSITION_REPORT.AISMessage_Id=AIS_MESSAGE.Id 
            AND Timestamp<="{0}";
            
            CREATE TEMPORARY TABLE OLD_STATIC  
            SELECT AISMessage_Id 
            FROM STATIC_DATA, AIS_MESSAGE 
            WHERE STATIC_DATA.AISMessage_Id=AIS_MESSAGE.Id 
            AND Timestamp<="{0}";
        """.format(timestamp_minus_5_min)

        query_delete_rows = """
        DELETE FROM POSITION_REPORT 
        WHERE AISMessage_Id 
        IN( SELECT AISMessage_Id FROM OLD_POSITIONS );
        
        DELETE FROM AIS_MESSAGE 
        WHERE Id 
        IN( SELECT AISMessage_Id FROM OLD_POSITIONS );
        
        
        DELETE FROM STATIC_DATA 
        WHERE AISMessage_Id 
        IN( SELECT AISMessage_Id FROM OLD_STATIC );
        
        DELETE FROM AIS_MESSAGE 
        WHERE Id 
        IN( SELECT AISMessage_Id FROM OLD_STATIC );
        """

        total_rows_deleted = 0
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query_temp_tables, multi=True):
                result.fetchall()
            for result in cursor.execute(query_delete_rows, multi=True):
                total_rows_deleted += result.rowcount
            con.commit()
        return json.dumps(total_rows_deleted, default=default)

    def read_all_recent_ship_positions(self):
        """
        Read all most recent ship positions

        :returns: Array of ship documents as json files
        :return type: json
        """
        if self.is_stub:
            return 1


        query = """
        CREATE TEMPORARY TABLE RECENT_VESSELS 
        SELECT MMSI, MAX(Timestamp) AS Timestamp 
        FROM AIS_MESSAGE, POSITION_REPORT  
        WHERE AIS_MESSAGE.Id=POSITION_REPORT.AISMessage_Id  
        GROUP BY MMSI;

        SELECT AM.MMSI, PR.latitude, PR.longitude  
        FROM AIS_MESSAGE as AM, POSITION_REPORT as PR, recent_vessels as RV  
        WHERE AM.Id=PR.AISMessage_Id  
        AND AM.MMSI=RV.MMSI 
        AND AM.timestamp=RV.timestamp;
        """

        ship_positions = []
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            iterator = cursor.execute(query, multi=True)

            if iterator is None:
                return json.dumps([])

            for result in iterator:
                if result.with_rows:
                    ships = result.fetchall()
                    for ship in ships:
                        ship_positions.append({'MMSI': ship[0], 'lat': ship[1], 'long': ship[2]})

        ship_positions = json.dumps(ship_positions, default=default)
        return ship_positions

    def read_ship_recent_position_from_mmsi(self, mmsi: int):
        """
        Read current position of given MMSI.

        :param mmsi: (int) - mmsi of a vessel
        :returns: Position document of the form {"MMSI": ..., "lat": ..., "long": ..., "IMO": ... }.
        :return type: json
        """
        if type(mmsi) != int:
            return -1

        if self.is_stub:
            return 1

        query_pos = "SELECT POSITION_REPORT.Latitude, POSITION_REPORT.Longitude " \
                    "FROM AIS_MESSAGE, POSITION_REPORT " \
                    "WHERE AIS_MESSAGE.Id=POSITION_REPORT.AISMessage_Id " \
                    "AND AIS_MESSAGE.MMSI={} " \
                    "ORDER BY Timestamp DESC " \
                    "LIMIT 1;"\
            .format(mmsi)

        _lat = None
        _long = None
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            iterator = cursor.execute(query_pos, multi=True)
            if iterator is not None:
                for result in iterator:
                    if result.with_rows:
                        for lat, long in result.fetchall():
                            _lat = lat
                            _long = long

        return encode(MMSI=mmsi, lat=_lat, long=_long)

    def read_vessel_information(self, mmsi: int, imo=None, name=None, call_sign=None):
        """
        Read permanent or transient vessel information matching the given MMSI, and 0 or more additional criteria:
        IMO, Name, CallSign

        :param mmsi: (int) - mmsi of the vessel
        :param imo: (optional, int) - imo of the vessel
        :param name: (optional, int) - name of the vessel
        :param call_sign: ((optional, int) - call sign of the vessel
        :returns: a Vessel document, with available and/or relevant properties.
        :return type: json
        """
        if type(mmsi) != int or (imo is not None and type(imo) != int) or (name is not None and type(name) != str) \
                or (call_sign is not None and type(call_sign) != str):
            return -1

        if self.is_stub:
            return 1


        optional_args = ";"
        optional_args = f"AND IMO={imo} {optional_args} " if imo is not None else optional_args
        optional_args = f"AND Name=\"{name}\" {optional_args} " if name is not None else optional_args
        optional_args = f"AND CallSign=\"{call_sign}\" {optional_args} " if call_sign is not None else optional_args

        query = """
            SELECT * 
            FROM VESSEL 
            WHERE MMSI={} 
            {}
        """.format(mmsi, optional_args)

        vessel = None
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    vessel = result.fetchall()[0]

        return encode(IMO=vessel[0], Flag=vessel[1], Name=vessel[2], Built=vessel[3], CallSign=vessel[4],
                      Length=vessel[5], Breadth=vessel[6], Tonnage=vessel[7], MMSI=vessel[8], Type=vessel[9],
                      Status=vessel[10], Owner=vessel[11])

    def read_all_ship_positions_from_tile(self, tile_id):
        """
        Read all most recent ship positions in the given tile.

        :param tile_id: (int) - id of the tile searching in
        :returns: Array of ship documents in a json string.
        :return type: json
        """
        if type(tile_id) != int:
            return -1

        if self.is_stub:
            return 1

        query = """
        CREATE TEMPORARY TABLE RECENT_VESSELS 
        SELECT MMSI, MAX(Timestamp) AS Timestamp 
        FROM AIS_MESSAGE, POSITION_REPORT  
        WHERE AIS_MESSAGE.Id=POSITION_REPORT.AISMessage_Id  
        AND (MapView1_Id={0} OR MapView2_Id={0} OR MapView3_Id={0})
        GROUP BY MMSI;
        
        select ais_message.mmsi, position_report.latitude, position_report.longitude 
        from recent_vessels, ais_message, position_report 
        where recent_vessels.mmsi=ais_message.mmsi 
        and recent_vessels.timestamp=ais_message.timestamp 
        and ais_message.id=position_report.aismessage_id ;
        """.format(tile_id)

        ships = None
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    ships = result.fetchall()

        ship_documents = []
        if ships:
            for ship in ships:
                ship_documents.append({"MMSI": ship[0], "lat": ship[1], "long": ship[2]})
            return json.dumps(ship_documents, default=default)
        return json.dumps([])

    def read_all_ports_from_name(self, port_name: str, country=None):
        """
        Read all ports matching the given name and (optional) country.

        :param port_name: (str) - name of the port desired
        :param country: (optional, str) - country name of the port
        :returns: Array of Port documents.
        :return type: json
        """
        if type(port_name) != str or (type(country) != str and country is not None):
            return -1

        if self.is_stub:
            return 1

        optional_args = ";"
        optional_args = f" AND Country=\"{country}\"{optional_args}" if country is not None else optional_args

        query = """
        select Id, Name, Country, Latitude, Longitude, MapView1_Id, MapView2_Id, MapView3_Id 
        from PORT 
        where Name=\"{}\" 
        {}
        """.format(port_name, optional_args)

        ports = []
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    ports = result.fetchall()

        port_documents = []
        if ports:
            for port in ports:
                port_documents.append({"Id": port[0], "Name": port[1], "Country": port[2], "Latitude": port[3],
                                       "Longitude": port[4], "MapView1_Id": port[5], "MapView2_Id": port[6],
                                       "MapView3_Id": port[7]})
            return json.dumps(port_documents, default=default)
        return json.dumps([])

    def read_all_ship_positions_from_tile_scale3(self, port_name: str, country: str):
        """
        Read all ship positions in the tile of scale 3 containing the given port.

        :param port_name: (str) - name of the port a ship is heading to
        :param country: (str) - name of the country the port is in
        :returns: If unique matching port: Array of Position documents (see above).
                    Otherwise: an Array of Port documents.
        :return type: json
        """

        if self.is_stub:
            if type(port_name) == str and type(country) == str:
                return 1
            return -1

        pass

    def read_last_5_ship_positions_from_mmsi(self, mmsi: int):
        """
        Read last 5 positions of given MMSI.

        :param mmsi: (int) - A ship's mmsi
        :returns: Document of the form {MMSI: ..., Positions: [{"lat": ..., "long": ...}, "IMO": ... ]}.
        :return type: json
        """
        if type(mmsi) != int:
            return -1

        if self.is_stub:
            return 1

        query_pos = "SELECT POSITION_REPORT.Latitude, POSITION_REPORT.Longitude " \
                    "FROM AIS_MESSAGE, POSITION_REPORT " \
                    "WHERE AIS_MESSAGE.Id=POSITION_REPORT.AISMessage_Id " \
                    "AND AIS_MESSAGE.MMSI={} " \
                    "ORDER BY Timestamp DESC LIMIT 5;" \
            .format(mmsi)

        positions = []
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            iterator = cursor.execute(query_pos, multi=True)

            if iterator is not None:
                for result in iterator:
                    if result.with_rows:
                        values = result.fetchall()
                        for lat, long in values:
                            positions.append({'lat': lat, 'long': long})

        return encode(MMSI=mmsi, Positions=positions)

    def read_all_ship_positions_to_port(self, port_id: int):
        """
        Read most recent positions of ships headed to port with given Id

        :param port_id: (int) - the port id of a desired port
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

        :param port_name: (str) - name of a port
        :param country: (str) - name of the country the port is in
        :returns: If unique matching port: array of of Position documents of the form
                    {"MMSI": ..., "lat": ..., "long": ..., "IMO": ...}.
                    Otherwise: an Array of Port documents.
        :return type: json
        """

        if self.is_stub:
            if type(port_name) == str and type(country) == str:
                return 1
            return -1



        pass

    def find_sub_map_tiles(self, tile_id: int):
        """
        Given a background map tile for zoom level 1 (2), find the 4 tiles of zoom level 2 (3) that are contained in it.

        :param tile_id: (int) - tile id of a parent tile.
        :returns: Array of map tile description documents.
        :return type: json
        """
        if type(tile_id) != int:
            return -1

        if self.is_stub:
            return 1


        query = """
        SELECT * 
        FROM MAP_VIEW 
        WHERE ContainerMapView_Id={}
        """.format(tile_id)

        tiles_list_info = []
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    tiles_list_info = result.fetchall()

        tiles_dicts = []
        if tiles_list_info:
            for tile in tiles_list_info:
                tiles_dicts.append(
                    {"Id": tile[0], "Name": tile[1], "LongitudeW": tile[2], "LatitudeS": tile[3], "LongitudeE": tile[4],
                     "LatitudeN": tile[5], "Scale": tile[6], "RasterFile": tile[7], "ImageWidth": tile[8],
                     "ImageHeight": tile[9], "ActualLongitudeW": tile[10], "ActualLatitudeS": tile[11],
                     "ActualLongitudeE": tile[12], "ActualLatitudeN": tile[13], "ContainerMapView_Id": tile[14]}
                )
            return json.dumps(tiles_dicts, default=default)
        return json.dumps([])

    def get_tile_png(self, tile_id: int):
        """
        Given a tile Id, get the actual tile (a PNG file).

        :param tile_id: (int) - tile id
        :returns: binary data for the PNG file for the tile_id.
        :return type: json
        """
        if type(tile_id) != int:
            return -1

        if self.is_stub:
            return 1

        query = """
        SELECT RasterFile 
        FROM MAP_VIEW 
        WHERE Id={};
        """.format(tile_id)

        png_name = None
        with MySQLConnectionManager(self.config) as con:
            cursor = con.cursor()
            for result in cursor.execute(query, multi=True):
                if result.with_rows:
                    png_name = result.fetchall()[0][0]

        if png_name:
            return json.dumps(''.join(format(ord(x), 'b') for x in png_name))
        return None

