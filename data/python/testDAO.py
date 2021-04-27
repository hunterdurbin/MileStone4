import unittest
from data.python.DataAccessObject import MySQL_DAO
from data.python.Encoder import *
import json


# TODO: test here to see if the correct parameters are defined
# Think of making an abstract class in Java that GUARANTEES our functions are here
# We want to cut the dependency from the database when checking the function
class DAO_Methods_UnitTest(unittest.TestCase):
    DAO: MySQL_DAO = None

    @classmethod
    def setUpClass(cls):
        DAO_Methods_UnitTest.DAO = MySQL_DAO(True)  # Turn on the method testing feature for the DAO

    @classmethod
    def tearDownClass(cls):
        DAO_Methods_UnitTest.DAO = None

    def test_insert_msg(self):
        pass

    def test_insert_msg_batch(self):
        pass

    def test_delete_msgs_older_5min(self):
        pass

    def test_read_all_ship_positions_from_tile(self):
        result = self.DAO.read_all_ship_positions_from_tile(81293)
        self.assertEqual(1, result)

    def test_read_last_5_ship_positions_from_mmsi(self):
        result = self.DAO.read_last_5_ship_positions_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_ship_current_position_from_mmsi(self):
        result = self.DAO.read_ship_current_position_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_all_ship_positions_from_port(self):
        result = self.DAO.read_all_ship_positions_from_port(412)
        self.assertEqual(1, result)

    def test_read_all_ships_headed_to_port(self):
        result = self.DAO.read_all_ships_headed_to_port('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_1(self):
        result = self.DAO.read_all_ports_from_name('PRT')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_2(self):
        result = self.DAO.read_all_ports_from_name('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_all_ship_positions_from_tile_scale3(self):
        result = self.DAO.read_all_ship_positions_from_tile_scale3('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_vessel_information_1(self):
        result = self.DAO.read_vessel_information(123456789)
        self.assertEqual(1, result)

    def test_read_vessel_information_2(self):
        result = self.DAO.read_vessel_information(123456789, 48912, 'Ever Given', 'EVGI')
        self.assertEqual(1, result)

    def test_find_sub_map_tiles(self):
        result = self.DAO.find_sub_map_tiles(347)
        self.assertEqual(1, result)

    def test_get_tile_png(self):
        result = self.DAO.get_tile_png(347)
        self.assertEqual(1, result)


class DAO_UnitTest(unittest.TestCase):
    DAO: MySQL_DAO = None

    @classmethod
    def setUpClass(cls):
        DAO_UnitTest.DAO = MySQL_DAO()

    @classmethod
    def tearDownClass(cls):
        DAO_UnitTest.DAO = None

    def test_insert_msg(self):
        pass

    def test_insert_msg_batch(self):
        pass

    def test_delete_msgs_older_5min(self):
        pass

    def test_read_all_ship_positions_from_tile(self):
        pass

    def test_read_last_5_ship_positions_from_mmsi(self):
        actual = self.DAO.read_last_5_ship_positions_from_mmsi(230631000)
        expected = json.dumps(
            {"MMSI": 230631000,
             "Positions":
                 [
                     {"lat": "54.749385", "long": "12.841955"},
                     {"lat": "54.749220", "long": "12.841198"},
                     {"lat": "54.749025", "long": "12.840288"},
                     {"lat": "54.748793", "long": "12.839228"},
                     {"lat": "54.748630", "long": "12.838472"}
                 ],
             "IMO": 9468920
             }
        )
        self.assertEqual(expected, actual)

    def test_read_ship_current_position_from_mmsi(self):
        actual = self.DAO.read_ship_current_position_from_mmsi(230631000)
        expected = json.dumps(
            {
                'MMSI': 230631000,
                'lat': '54.749385',
                'long': '12.841955',
                'IMO': 9468920
            }
        )
        self.assertEqual(expected, actual)

    def test_read_all_ship_positions_from_port(self):
        pass

    def test_read_all_ships_headed_to_port(self):
        pass

    def test_read_all_ports_from_name(self):
        pass

    def test_read_all_ship_positions_from_tile_scale3(self):
        pass

    def test_read_vessel_information(self):
        pass

    def test_find_sub_map_tiles(self):
        pass

    def test_get_tile_png(self):
        pass


class Encoder_UnitTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        pass

    @classmethod
    def tearDownClass(cls):
        pass

    def test_encode_1(self):
        actual = encode(MMSI=123456789, Positions=[])
        expected = json.dumps(
            {
                "MMSI": 123456789,
                "Positions": []
            }
        )

        self.assertEqual(expected, actual)

    def test_encode_2(self):
        actual = encode(MMSI=123456789, Positions=[{'lat': 42.412, 'long': 49.124}])
        expected = json.dumps(
            {
                "MMSI": 123456789,
                "Positions": [{'lat': 42.412, 'long': 49.124}]
            }
        )

        self.assertEqual(expected, actual)

    def test_decode_1(self):
        actual = decode('{"Hunter": [6, 5, 14, 125]}')
        expected = json.loads('{"Hunter": [6, 5, 14, 125]}')
        self.assertEqual(expected, actual)

    def test_decode_2(self):
        actual = decode('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,"MsgType":'
                        '"position_report","Position":{"type":"Point","coordinates":[55.218332,13.371672]},'
                        '"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}')
        expected = json.loads('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,"MsgType":'
                              '"position_report","Position":{"type":"Point","coordinates":[55.218332,13.371672]},'
                              '"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}')
        self.assertEqual(expected, actual)

    def test_extract_timestamp_1(self):
        actual = extract_timestamp("2020-11-18T00:00:00.000Z")
        expected = "2020-11-18 00:00:00"
        self.assertEqual(expected, actual)

    def test_extract_timestamp_2(self):
        actual = extract_timestamp("2020-11-18T00:00:01.000Z")
        expected = "2020-11-18 00:00:01"
        self.assertEqual(expected, actual)

    def test_extract_message_position_1(self):
        actual = extract_message_position({"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":249579000,
                                           "MsgType":"position_report",
                                           "Position":{"type":"Point","coordinates":[54.968268,13.886702]},
                                           "Status":"Under way using engine","RoT":1.6,"SoG":14.3,"CoG":72.7,
                                           "Heading":73})
        expected = {'MsgType': 'position_report', 'MMSI': 249579000, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A', 'Latitude': 54.968268, 'Longitude': 13.886702,
                    'Status': 'Under way using engine', 'RoT': 1.6, 'SoG': 14.3, 'CoG': 72.7, 'Heading': 73}
        self.assertEqual(expected, actual)

    def test_extract_message_position_2(self):
        actual = extract_message_position({"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":257961000,
                                           "MsgType":"position_report","Position":
                                               {"type":"Point","coordinates":[55.00316,12.809015]},
                                           "Status":"Under way using engine","RoT":0,"SoG":0.2,"CoG":225.6,
                                           "Heading":240})
        expected = {'MsgType': 'position_report', 'MMSI': 257961000, 'Timestamp': '2020-11-18 00:00:00', 'Class': 'Class A', 'Latitude': 55.00316,
                    'Longitude': 12.809015, 'Status': 'Under way using engine', 'RoT': 0, 'SoG': 0.2, 'CoG': 225.6,
                    'Heading': 240}
        self.assertEqual(expected, actual)

    def test_extract_message_static_1(self):
        actual = extract_message_static({"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":219023635,
                                         "MsgType":"static_data","IMO":"Unknown","CallSign":"OX3103","Name":"SKJOLD R",
                                         "VesselType":"Other","CargoTye":"No additional information","Length":12,
                                         "Breadth":4,"Draught":1.5,"Destination":"HANSTHOLM",
                                         "ETA":"2021-07-14T23:00:00.000Z","A":8,"B":4,"C":2,"D":2})
        expected = {'MsgType': 'static_data', 'MMSI': 219023635, 'IMO': 'Unknown', 'Timestamp': '2020-11-18 00:00:00', 'Class': 'Class A',
                    'CallSign': 'OX3103', 'Name': 'SKJOLD R', 'VesselType': 'Other', 'Length': 12, 'Breadth': 4,
                    'Draught': 1.5, 'Destination': 'HANSTHOLM', 'ETA': '2021-07-14 23:00:00'}
        self.assertEqual(expected, actual)

    def test_extract_message_static_2(self):
        actual = extract_message_static({"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":265011000,
                                         "MsgType":"static_data","IMO":8616087,"CallSign":"SBEN","Name":"SOFIA",
                                         "VesselType":"Cargo","Length":72,"Breadth":11,"Draught":3.7,
                                         "Destination":"DK VEJ","ETA":"2020-11-18T10:00:00.000Z",
                                         "A":59,"B":13,"C":6,"D":5})
        expected = {'MsgType': 'static_data', 'MMSI': 265011000, 'IMO': 8616087, 'Timestamp': '2020-11-18 00:00:00', 'Class': 'Class A',
                    'CallSign': 'SBEN', 'Name': 'SOFIA', 'VesselType': 'Cargo', 'Length': 72, 'Breadth': 11,
                    'Draught': 3.7, 'Destination': 'DK VEJ', 'ETA': '2020-11-18 10:00:00'}
        self.assertEqual(expected, actual)

    def test_extract_message_1(self):
        actual = extract_message('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":257961000,'
                                 '"MsgType":"position_report","Position":'
                                 '{"type":"Point","coordinates":[55.00316,12.809015]},'
                                 '"Status":"Under way using engine","RoT":0,"SoG":0.2,"CoG":225.6,"Heading":240}')
        expected = {'MsgType': 'position_report', 'MMSI': 257961000, 'Timestamp': '2020-11-18 00:00:00', 'Class': 'Class A', 'Latitude': 55.00316,
                    'Longitude': 12.809015, 'Status': 'Under way using engine', 'RoT': 0, 'SoG': 0.2, 'CoG': 225.6,
                    'Heading': 240}
        self.assertEqual(expected, actual)

    def test_extract_message_2(self):
        actual = extract_message('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":265011000,'
                                 '"MsgType":"static_data","IMO":8616087,"CallSign":"SBEN","Name":"SOFIA",'
                                 '"VesselType":"Cargo","Length":72,"Breadth":11,"Draught":3.7,'
                                 '"Destination":"DK VEJ","ETA":"2020-11-18T10:00:00.000Z","A":59,"B":13,"C":6,"D":5}')
        expected = {'MsgType': 'static_data', 'MMSI': 265011000, 'IMO': 8616087, 'Timestamp': '2020-11-18 00:00:00', 'Class': 'Class A',
                    'CallSign': 'SBEN', 'Name': 'SOFIA', 'VesselType': 'Cargo', 'Length': 72, 'Breadth': 11,
                    'Draught': 3.7, 'Destination': 'DK VEJ', 'ETA': '2020-11-18 10:00:00'}
        self.assertEqual(expected, actual)