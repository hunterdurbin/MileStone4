import unittest
from data.python.DataAccessObject import MySQL_DAO
from data.python.Encoder import *
import data.python.dbTestSetup
import json


class DAO_Methods_UnitTest(unittest.TestCase):
    DAO: MySQL_DAO = None

    @classmethod
    def setUpClass(cls):
        DAO_Methods_UnitTest.DAO = MySQL_DAO(True)  # Turn on the method testing feature for the DAO

    @classmethod
    def tearDownClass(cls):
        DAO_Methods_UnitTest.DAO = None

    def test_insert_msg_interface(self):
        actual = self.DAO.insert_msg('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,'
                                     '"MsgType":"position_report",'
                                     '"Position":{"type":"Point","coordinates":[55.218332,12.371672]},'
                                     '"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}')
        self.assertEqual(1, actual)

    def test_insert_msg_batch_interface(self):
        actual = self.DAO.insert_msg_batch([
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 304858000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.218332, 13.371672]},
             "Status": "Under way using engine", "SoG": 10.8, "CoG": 94.3, "Heading": 97},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111840, "MsgType": "static_data",
             "IMO": "Unknown", "Name": "WIND FARM BALTIC1NW", "VesselType": "Undefined", "Length": 60, "Breadth": 60,
             "A": 30, "B": 30, "C": 30, "D": 30},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219005465,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.572602, 11.929218]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0, "CoG": 298.7, "Heading": 203},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257961000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.00316, 12.809015]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0.2, "CoG": 225.6, "Heading": 240},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111923, "MsgType": "static_data",
             "IMO": "Unknown", "Name": "BALTIC2 WINDFARM SW", "VesselType": "Undefined", "Length": 8, "Breadth": 12,
             "A": 4, "B": 4, "C": 4, "D": 8},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257385000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.219403, 13.127725]},
             "Status": "Under way using engine", "RoT": 25.7, "SoG": 12.3, "CoG": 96.5, "Heading": 101},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 376503000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.519373, 11.47914]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 7.6, "CoG": 294.4, "Heading": 290},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 229964000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.664513, 13.068712]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 9.3, "CoG": 68.2, "Heading": 71},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219570000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.07848, 12.814233]},
             "Status": "Under way using engine", "SoG": 0.8, "CoG": 65.8}
        ])
        batch_len = 9
        self.assertEqual(batch_len, actual)

    def test_delete_msgs_older_5min_interface(self):
        pass

    def test_read_all_recent_ship_positions(self):
        actual = self.DAO.read_all_recent_ship_positions()
        self.assertEqual(1, actual)

    def test_read_all_ship_positions_from_tile_interface(self):
        result = self.DAO.read_all_ship_positions_from_tile(81293)
        self.assertEqual(1, result)

    def test_read_last_5_ship_positions_from_mmsi_interface(self):
        result = self.DAO.read_last_5_ship_positions_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_ship_recent_position_from_mmsi_interface(self):
        result = self.DAO.read_ship_recent_position_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_all_ship_positions_to_port_interface(self):
        result = self.DAO.read_all_ship_positions_to_port(412)
        self.assertEqual(1, result)

    def test_read_all_ships_headed_to_port_interface(self):
        result = self.DAO.read_all_ships_headed_to_port('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_1_interface(self):
        result = self.DAO.read_all_ports_from_name('PRT')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_2_interface(self):
        result = self.DAO.read_all_ports_from_name('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_all_ship_positions_from_tile_scale3_interface(self):
        result = self.DAO.read_all_ship_positions_from_tile_scale3('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_vessel_information_1_interface(self):
        result = self.DAO.read_vessel_information(123456789)
        self.assertEqual(1, result)

    def test_read_vessel_information_2_interface(self):
        result = self.DAO.read_vessel_information(123456789, 48912, 'Ever Given', 'EVGI')
        self.assertEqual(1, result)

    def test_find_sub_map_tiles_interface(self):
        result = self.DAO.find_sub_map_tiles(347)
        self.assertEqual(1, result)

    def test_get_tile_png_interface(self):
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

    # Test position report is inserted correctly
    def test_insert_msg_1(self):
        actual = self.DAO.insert_msg('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,'
                                     '"MsgType":"position_report",'
                                     '"Position":{"type":"Point","coordinates":[55.218332,12.371672]},'
                                     '"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}')
        expected = 1
        self.assertEqual(expected, actual)

    # Test static data is inserted correctly
    def test_insert_msg_2(self):
        actual = self.DAO.insert_msg('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":210169000,'
                                     '"MsgType":"static_data","IMO":9584865,"CallSign":"5BNZ3",'
                                     '"Name":"KATHARINA SCHEPERS","VesselType":"Cargo","CargoTye":'
                                     '"Category X","Length":152,"Breadth":24,"Draught":7.8,"Destination":"NODRM",'
                                     '"ETA":"2020-11-18T09:00:00.000Z","A":143,"B":9,"C":13,"D":11}')
        expected = 1
        self.assertEqual(expected, actual)

    # Test if all 9 msgs in the batch are inserted
    def test_insert_msg_batch_1(self):
        actual = self.DAO.insert_msg_batch([
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 304858000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.218332, 13.371672]},
             "Status": "Under way using engine", "SoG": 10.8, "CoG": 94.3, "Heading": 97},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111840, "MsgType": "static_data",
             "IMO": "Unknown", "Name": "WIND FARM BALTIC1NW", "VesselType": "Undefined", "Length": 60, "Breadth": 60,
             "A": 30, "B": 30, "C": 30, "D": 30},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219005465,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.572602, 11.929218]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0, "CoG": 298.7, "Heading": 203},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257961000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.00316, 12.809015]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0.2, "CoG": 225.6, "Heading": 240},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111923, "MsgType": "static_data",
             "IMO": "Unknown", "Name": "BALTIC2 WINDFARM SW", "VesselType": "Undefined", "Length": 8, "Breadth": 12,
             "A": 4, "B": 4, "C": 4, "D": 8},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257385000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.219403, 13.127725]},
             "Status": "Under way using engine", "RoT": 25.7, "SoG": 12.3, "CoG": 96.5, "Heading": 101},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 376503000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.519373, 11.47914]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 7.6, "CoG": 294.4, "Heading": 290},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 229964000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.664513, 13.068712]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 9.3, "CoG": 68.2, "Heading": 71},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219570000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.07848, 12.814233]},
             "Status": "Under way using engine", "SoG": 0.8, "CoG": 65.8}
        ])
        expected = 9
        self.assertEqual(expected, actual)

    # Test if all 5 msgs in the batch are inserted (out of the 9 that are sent)
    def test_insert_msg_batch_2(self):
        actual = self.DAO.insert_msg_batch([
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 304858000,
             "MsgType": "false_report", "Position": {"type": "Point", "coordinates": [55.218332, 13.371672]},
             "Status": "Under way using engine", "SoG": 10.8, "CoG": 94.3, "Heading": 97},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111840, "MsgType": "static_data",
             "IMO": "Unknown", "Name": "WIND FARM BALTIC1NW", "VesselType": "Undefined", "Length": 60, "Breadth": 60,
             "A": 30, "B": 30, "C": 30, "D": 30},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219005465,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.572602, 11.929218]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0, "CoG": 298.7, "Heading": 203},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257961000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.00316, 12.809015]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0.2, "CoG": 225.6, "Heading": 240},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "AtoN", "MMSI": 992111923, "MsgType": "false_report",
             "IMO": "Unknown", "Name": "BALTIC2 WINDFARM SW", "VesselType": "Undefined", "Length": 8, "Breadth": 12,
             "A": 4, "B": 4, "C": 4, "D": 8},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257385000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.219403, 13.127725]},
             "Status": "Under way using engine", "RoT": 25.7, "SoG": 12.3, "CoG": 96.5, "Heading": 101},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 376503000,
             "MsgType": "false_report", "Position": {"type": "Point", "coordinates": [54.519373, 11.47914]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 7.6, "CoG": 294.4, "Heading": 290},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 229964000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [54.664513, 13.068712]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 9.3, "CoG": 68.2, "Heading": 71},
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219570000,
             "MsgType": "false_report", "Position": {"type": "Point", "coordinates": [55.07848, 12.814233]},
             "Status": "Under way using engine", "SoG": 0.8, "CoG": 65.8}
        ])
        expected = 5
        self.assertEqual(expected, actual)

    def test_delete_msgs_older_5min(self):
        pass

    def test_read_all_recent_ship_positions(self):
        actual = self.DAO.read_all_recent_ship_positions()
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
                 ]
             }
        )
        self.assertEqual(expected, actual)

    def test_ship_recent_position_from_mmsi(self):
        actual = self.DAO.read_ship_recent_position_from_mmsi(230631000)
        expected = json.dumps(
            {
                'MMSI': 230631000,
                'lat': '54.749385',
                'long': '12.841955'
            }
        )
        self.assertEqual(expected, actual)

    def test_read_all_ship_positions_to_port(self):
        pass

    def test_read_all_ships_headed_to_port(self):
        pass

    def test_read_all_ports_from_name(self):
        pass

    def test_read_all_ship_positions_from_tile(self):
        actual = self.DAO.read_all_ship_positions_from_tile(51351)
        print(actual)
        pass

    def test_read_vessel_information_1(self):
        actual = self.DAO.read_vessel_information(230631000)
        expected = json.dumps(
            {"IMO": 9468920,
             "Flag": "Finland",
             "Name": "Finntide",
             "Built": 2012,
             "CallSign": None,
             "Length": 217,
             "Breadth": 26,
             "Tonnage": 33816,
             "MMSI": 230631000,
             "Type": "Ro-Ro",
             "Status": "Active",
             "Owner": "14852"}

        )
        self.assertEqual(expected, actual)

    def test_read_vessel_information_2(self):
        actual = self.DAO.read_vessel_information(319904000, name="Montkaj")
        expected = json.dumps(
            {"IMO": 1000021,
             "Flag": "Cayman Islands",
             "Name": "Montkaj",
             "Built": 1995,
             "CallSign": None,
             "Length": 78,
             "Breadth": 13,
             "Tonnage": 2000,
             "MMSI": 319904000,
             "Type": "Yacht",
             "Status": "Active",
             "Owner": "2"}
        )
        self.assertEqual(expected, actual)

    def test_read_vessel_information_3(self):
        actual = self.DAO.read_vessel_information(440007100, name="Pesquera Hernan Cortes", call_sign="6287207")
        print(actual)
        expected = json.dumps(
            {"IMO": 5275569,
             "Flag": "Spain",
             "Name": "Pesquera Hernan Cortes",
             "Built": 1953,
             "CallSign": "6287207",
             "Length": 28,
             "Breadth": 5,
             "Tonnage": 145,
             "MMSI": 440007100,
             "Type": "Fishing Vessel",
             "Status": "Active",
             "Owner": None}
        )
        self.assertEqual(expected, actual)

    def test_read_vessel_information_4(self):
        actual = self.DAO.read_vessel_information(440007100, imo=5275569, call_sign="6287207")
        expected = json.dumps(
            {"IMO": 5275569,
             "Flag": "Spain",
             "Name": "Pesquera Hernan Cortes",
             "Built": 1953,
             "CallSign": "6287207",
             "Length": 28,
             "Breadth": 5,
             "Tonnage": 145,
             "MMSI": 440007100,
             "Type": "Fishing Vessel",
             "Status": "Active",
             "Owner": None}
        )
        self.assertEqual(expected, actual)

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
        actual = extract_message_position(
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 249579000,
             "MsgType": "position_report",
             "Position": {"type": "Point", "coordinates": [54.968268, 13.886702]},
             "Status": "Under way using engine", "RoT": 1.6, "SoG": 14.3, "CoG": 72.7,
             "Heading": 73})
        expected = {'MsgType': 'position_report', 'MMSI': 249579000, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A', 'Latitude': 54.968268, 'Longitude': 13.886702,
                    'Status': 'Under way using engine', 'RoT': 1.6, 'SoG': 14.3, 'CoG': 72.7, 'Heading': 73}
        self.assertEqual(expected, actual)

    def test_extract_message_position_2(self):
        actual = extract_message_position(
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 257961000,
             "MsgType": "position_report", "Position":
                 {"type": "Point", "coordinates": [55.00316, 12.809015]},
             "Status": "Under way using engine", "RoT": 0, "SoG": 0.2, "CoG": 225.6,
             "Heading": 240})
        expected = {'MsgType': 'position_report', 'MMSI': 257961000, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A', 'Latitude': 55.00316,
                    'Longitude': 12.809015, 'Status': 'Under way using engine', 'RoT': 0, 'SoG': 0.2, 'CoG': 225.6,
                    'Heading': 240}
        self.assertEqual(expected, actual)

    def test_extract_message_static_1(self):
        actual = extract_message_static({"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 219023635,
                                         "MsgType": "static_data", "IMO": "Unknown", "CallSign": "OX3103",
                                         "Name": "SKJOLD R",
                                         "VesselType": "Other", "CargoTye": "No additional information", "Length": 12,
                                         "Breadth": 4, "Draught": 1.5, "Destination": "HANSTHOLM",
                                         "ETA": "2021-07-14T23:00:00.000Z", "A": 8, "B": 4, "C": 2, "D": 2})
        expected = {'MsgType': 'static_data', 'MMSI': 219023635, 'IMO': 'Unknown', 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A',
                    'CallSign': 'OX3103', 'Name': 'SKJOLD R', 'VesselType': 'Other', 'Length': 12, 'Breadth': 4,
                    'Draught': 1.5, 'Destination': 'HANSTHOLM', 'ETA': '2021-07-14 23:00:00'}
        self.assertEqual(expected, actual)

    def test_extract_message_static_2(self):
        actual = extract_message_static({"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 265011000,
                                         "MsgType": "static_data", "IMO": 8616087, "CallSign": "SBEN", "Name": "SOFIA",
                                         "VesselType": "Cargo", "Length": 72, "Breadth": 11, "Draught": 3.7,
                                         "Destination": "DK VEJ", "ETA": "2020-11-18T10:00:00.000Z",
                                         "A": 59, "B": 13, "C": 6, "D": 5})
        expected = {'MsgType': 'static_data', 'MMSI': 265011000, 'IMO': 8616087, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A',
                    'CallSign': 'SBEN', 'Name': 'SOFIA', 'VesselType': 'Cargo', 'Length': 72, 'Breadth': 11,
                    'Draught': 3.7, 'Destination': 'DK VEJ', 'ETA': '2020-11-18 10:00:00'}
        self.assertEqual(expected, actual)

    def test_extract_message_1(self):
        actual = extract_message('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":257961000,'
                                 '"MsgType":"position_report","Position":'
                                 '{"type":"Point","coordinates":[55.00316,12.809015]},'
                                 '"Status":"Under way using engine","RoT":0,"SoG":0.2,"CoG":225.6,"Heading":240}')
        expected = {'MsgType': 'position_report', 'MMSI': 257961000, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A', 'Latitude': 55.00316,
                    'Longitude': 12.809015, 'Status': 'Under way using engine', 'RoT': 0, 'SoG': 0.2, 'CoG': 225.6,
                    'Heading': 240}
        self.assertEqual(expected, actual)

    def test_extract_message_2(self):
        actual = extract_message('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":265011000,'
                                 '"MsgType":"static_data","IMO":8616087,"CallSign":"SBEN","Name":"SOFIA",'
                                 '"VesselType":"Cargo","Length":72,"Breadth":11,"Draught":3.7,'
                                 '"Destination":"DK VEJ","ETA":"2020-11-18T10:00:00.000Z","A":59,"B":13,"C":6,"D":5}')
        expected = {'MsgType': 'static_data', 'MMSI': 265011000, 'IMO': 8616087, 'Timestamp': '2020-11-18 00:00:00',
                    'Class': 'Class A',
                    'CallSign': 'SBEN', 'Name': 'SOFIA', 'VesselType': 'Cargo', 'Length': 72, 'Breadth': 11,
                    'Draught': 3.7, 'Destination': 'DK VEJ', 'ETA': '2020-11-18 10:00:00'}
        self.assertEqual(expected, actual)
