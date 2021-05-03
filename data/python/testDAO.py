import unittest
from data.python.DataAccessObject import MySQL_DAO
from data.python.Encoder import *
import data.python.dbTestSetup
import json


class DAO_Methods_UnitTest(unittest.TestCase):
    """
    Test methods exist in the DAO and check if the methods take the correct argument types.
    """
    DAO: MySQL_DAO = None

    @classmethod
    def setUpClass(cls):
        DAO_Methods_UnitTest.DAO = MySQL_DAO(True)  # Turn on the method testing feature for the DAO

    @classmethod
    def tearDownClass(cls):
        DAO_Methods_UnitTest.DAO = None

    def test_insert_msg_batch_interface_1(self):
        """
        Function `insert_msg_batch` takes an array of dictionaries as an input
        """
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
             "Status": "Under way using engine", "RoT": 0, "SoG": 0.2, "CoG": 225.6, "Heading": 240}
        ])
        batch_len = 4
        self.assertEqual(batch_len, actual)

    def test_insert_msg_batch_interface_2(self):
        """
        Function `insert_msg_batch` fails nicely if input is not array
        """
        actual = self.DAO.insert_msg_batch(
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 304858000,
             "MsgType": "position_report",
             "Position": {"type": "Point", "coordinates": [55.218332, 13.371672]},
             "Status": "Under way using engine", "SoG": 10.8, "CoG": 94.3, "Heading": 97}
        )
        expected = -1
        self.assertEqual(expected, actual)

    def test_insert_msg_batch_interface_3(self):
        """
        Function `insert_msg_batch` fails nicely if contents of array aren't all dictionaries
        """
        actual = self.DAO.insert_msg_batch([
            {"Timestamp": "2020-11-18T00:00:00.000Z", "Class": "Class A", "MMSI": 304858000,
             "MsgType": "position_report", "Position": {"type": "Point", "coordinates": [55.218332, 13.371672]},
             "Status": "Under way using engine", "SoG": 10.8, "CoG": 94.3, "Heading": 97},
            'Vessel'
        ])
        expected = -1
        self.assertEqual(expected, actual)

    def test_insert_msg_interface_1(self):
        """
        Function `insert_msg` takes a string as input
        """
        actual = self.DAO.insert_msg('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":304858000,'
                                     '"MsgType":"position_report",'
                                     '"Position":{"type":"Point","coordinates":[55.218332,12.371672]},'
                                     '"Status":"Under way using engine","SoG":10.8,"CoG":94.3,"Heading":97}')
        self.assertEqual(1, actual)

    def test_insert_msg_interface_2(self):
        """
        Function `insert_msg` fails nicely if input is not a str
        """
        actual = self.DAO.insert_msg(3)
        self.assertEqual(-1, actual)

    def test_delete_msgs_older_5min_interface_1(self):
        """
        Function `delete_msgs_older_5min` takes MySQL formatted str as input
        """
        actual = self.DAO.delete_msgs_older_5min("2020-11-18 00:00:00")
        expected = 1
        self.assertEqual(expected, actual)

    def test_delete_msgs_older_5min_interface_2(self):
        """
        Function `delete_msgs_older_5min` takes Python formatted str as input
        """
        actual = self.DAO.delete_msgs_older_5min("2020-11-18T00:00:00.000Z")
        expected = 1
        self.assertEqual(expected, actual)

    def test_delete_msgs_older_5min_interface_3(self):
        """
        Function `delete_msgs_older_5min` fails nicely if input is not formatted correctly
        """
        actual = self.DAO.delete_msgs_older_5min("2020-11-18 00:00:00.000")
        expected = -1
        self.assertEqual(expected, actual)

    def test_delete_msgs_older_5min_interface_4(self):
        """
        Function `delete_msgs_older_5min` fails nicely if input is not str
        """
        actual = self.DAO.delete_msgs_older_5min(2020-11-18)
        expected = -1
        self.assertEqual(expected, actual)

    def test_read_all_recent_ship_positions_interface_1(self):
        """
        Function `read_all_recent_ship_positions` exists
        """
        actual = self.DAO.read_all_recent_ship_positions()
        self.assertEqual(1, actual)

    def test_read_ship_recent_position_from_mmsi_interface_1(self):
        """
        Function `read_ship_recent_position_from_mmsi` takes int as input
        """
        result = self.DAO.read_ship_recent_position_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_ship_recent_position_from_mmsi_interface_2(self):
        """
        Function `read_ship_recent_position_from_mmsi` fails nicely if input is not int
        """
        result = self.DAO.read_ship_recent_position_from_mmsi("123456789")
        self.assertEqual(-1, result)

    def test_read_vessel_information_interface_1(self):
        """
        Function `read_vessel_information` takes int as the only input
        """
        result = self.DAO.read_vessel_information(123456789)
        self.assertEqual(1, result)

    def test_read_vessel_information_interface_2(self):
        """
        Function `read_vessel_information` takes mmsi as int, imo as int, name as str, and call_sign as str
        """
        result = self.DAO.read_vessel_information(123456789, 48912, 'Ever Given', 'EVGI')
        self.assertEqual(1, result)

    def test_read_vessel_information_interface_3(self):
        """
        Function `read_vessel_information` fails nicely if mmsi is not an int
        """
        result = self.DAO.read_vessel_information('123456789', 48912, 'Ever Given', 'EVGI')
        self.assertEqual(-1, result)

    def test_read_vessel_information_interface_4(self):
        """
        Function `read_vessel_information` fails nicely if imo is not an int
        """
        result = self.DAO.read_vessel_information(123456789, '48912', 'Ever Given', 'EVGI')
        self.assertEqual(-1, result)

    def test_read_vessel_information_interface_5(self):
        """
        Function `read_vessel_information` fails nicely if call_sign is not str
        """
        result = self.DAO.read_vessel_information(123456789, 48912, 'Ever Given', 3452)
        self.assertEqual(-1, result)

    def test_read_all_ship_positions_from_tile_interface_1(self):
        """
        Function `read_all_ship_positions_from_tile` takes int as input
        """
        result = self.DAO.read_all_ship_positions_from_tile(81293)
        self.assertEqual(1, result)

    def test_read_all_ship_positions_from_tile_interface_2(self):
        """
        Function `read_all_ship_positions_from_tile` fails nicely if input is not an int
        """
        result = self.DAO.read_all_ship_positions_from_tile('81293')
        self.assertEqual(-1, result)

    def test_read_all_ports_from_name_interface_1(self):
        """
        Function `read_all_ports_from_name` takes only one input as a str
        """
        result = self.DAO.read_all_ports_from_name('PRT')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_interface_2(self):
        """
        Function `read_all_ports_from_name` takes two inputs, which are both type str
        """
        result = self.DAO.read_all_ports_from_name('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_all_ports_from_name_interface_3(self):
        """
        Function `read_all_ports_from_name` fails nicely if first input is not str
        """
        result = self.DAO.read_all_ports_from_name(123)
        self.assertEqual(-1, result)

    def test_read_all_ports_from_name_interface_4(self):
        """
        Function `read_all_ports_from_name` fails nicely if first input is str, but second input is not str
        """
        result = self.DAO.read_all_ports_from_name('PRT', 123)
        self.assertEqual(-1, result)

    def test_read_all_ship_positions_from_tile_scale3_interface___(self):
        result = self.DAO.read_all_ship_positions_from_tile_scale3('PRT', 'USA')
        self.assertEqual(1, result)

    def test_read_last_5_ship_positions_from_mmsi_interface_1(self):
        """
        Function `read_last_5_ship_positions_from_mmsi` takes int as only input
        """
        result = self.DAO.read_last_5_ship_positions_from_mmsi(123456789)
        self.assertEqual(1, result)

    def test_read_last_5_ship_positions_from_mmsi_interface_2(self):
        """
        Function `read_last_5_ship_positions_from_mmsi` fails nicely if input is not int
        """
        result = self.DAO.read_last_5_ship_positions_from_mmsi('123456789')
        self.assertEqual(-1, result)

    def test_read_all_ship_positions_to_port_interface(self):
        result = self.DAO.read_all_ship_positions_to_port(412)
        self.assertEqual(1, result)

    def test_read_all_ships_headed_to_port_interface____(self):
        result = self.DAO.read_all_ships_headed_to_port('PRT', 'USA')
        self.assertEqual(1, result)

    def test_find_sub_map_tiles_interface_1(self):
        """
        Function `find_sub_map_tiles` takes int as input
        """
        result = self.DAO.find_sub_map_tiles(347)
        self.assertEqual(1, result)

    def test_find_sub_map_tiles_interface_2(self):
        """
        Function `find_sub_map_tiles` fails nicely if input is not int
        """
        result = self.DAO.find_sub_map_tiles('347')
        self.assertEqual(-1, result)

    def test_get_tile_png_interface_1(self):
        """
        Function `get_tile_png` takes int as input
        """
        result = self.DAO.get_tile_png(347)
        self.assertEqual(1, result)

    def test_get_tile_png_interface_2(self):
        """
        Function `get_tile_png` fails nicely if input is not int
        """
        result = self.DAO.get_tile_png('347')
        self.assertEqual(-1, result)








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
        expected = json.dumps(1)
        self.assertEqual(expected, actual)

    # Test static data is inserted correctly
    def test_insert_msg_2(self):
        actual = self.DAO.insert_msg('{"Timestamp":"2020-11-18T00:00:00.000Z","Class":"Class A","MMSI":210169000,'
                                     '"MsgType":"static_data","IMO":9584865,"CallSign":"5BNZ3",'
                                     '"Name":"KATHARINA SCHEPERS","VesselType":"Cargo","CargoTye":'
                                     '"Category X","Length":152,"Breadth":24,"Draught":7.8,"Destination":"NODRM",'
                                     '"ETA":"2020-11-18T09:00:00.000Z","A":143,"B":9,"C":13,"D":11}')
        expected = json.dumps(1)
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
        """
        Delete msgs from the first 3 minutes (incrementally)
        Deletes msgs older than or equal to 2020-11-18 00:00:00,
        then older than or equal to 2020-11-18T00:00:01.000Z,
        then older than or equal to 2020-11-18 00:02:00,
        finally older than or equal to 2020-11-18T00:00:03.000Z.

        There are 4 assertions in here. I did not know how to make an incrementing test of this delete method
        using multiple methods.
        """
        actual_zero_minute = self.DAO.delete_msgs_older_5min("2020-11-18 00:05:00")
        actual_first_minute = self.DAO.delete_msgs_older_5min("2020-11-18T00:06:00.000Z")
        actual_second_minute = self.DAO.delete_msgs_older_5min("2020-11-18 00:07:00")
        actual_third_minute = self.DAO.delete_msgs_older_5min("2020-11-18T00:08:00.000Z")
        self.assertEqual(json.dumps(252), actual_zero_minute)
        self.assertEqual(json.dumps(12736), actual_first_minute)
        self.assertEqual(json.dumps(12804), actual_second_minute)
        self.assertEqual(json.dumps(12808), actual_third_minute)
        pass

    def test_read_all_recent_ship_positions(self):
        actual = self.DAO.read_all_recent_ship_positions()
        pass

    def test_read_last_5_ship_positions_from_mmsi(self):
        """
        Read the last 5 positions for vessel with an MMSI of 230631000
        """
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
        """
        Read the most recent position for the vessel with an MMSI of 230631000
        """
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
        """
        Read the ports matching
        """
        actual = self.DAO.read_all_ports_from_name("Nyborg")
        expected = json.dumps(
            [
                {"Id": 381,
                 "Name": "Nyborg",
                 "Country": "Denmark",
                 "Latitude": "55.298889",
                 "Longitude": "10.810833",
                 "MapView1_Id": 1,
                 "MapView2_Id": 5331,
                 "MapView3_Id": 53312},
                {"Id": 4970,
                 "Name": "Nyborg",
                 "Country": "Denmark",
                 "Latitude": "55.306944",
                 "Longitude": "10.790833",
                 "MapView1_Id": 1,
                 "MapView2_Id": 5331,
                 "MapView3_Id": 53312}
            ]

        )
        self.assertEqual(expected, actual)

    def test_read_all_ship_positions_from_tile(self):
        actual = self.DAO.read_all_ship_positions_from_tile(51351)
        # print(actual)
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
        actual = self.DAO.find_sub_map_tiles(5531)
        expected = json.dumps(
            [
                {"Id": 55311, "Name": "43G21", "LongitudeW": "12.000000", "LatitudeS": "57.250000",
                 "LongitudeE": "12.500000", "LatitudeN": "57.500000", "Scale": "3", "RasterFile": "43G21.png",
                 "ImageWidth": 2000, "ImageHeight": 2000, "ActualLongitudeW": "12.000000", "ActualLatitudeS":
                     "57.240181", "ActualLongitudeE": "12.500000", "ActualLatitudeN": "57.509749",
                 "ContainerMapView_Id": 5531},
                {"Id": 55312, "Name": "43G22", "LongitudeW": "12.500000", "LatitudeS": "57.250000",
                 "LongitudeE": "13.000000", "LatitudeN": "57.500000", "Scale": "3", "RasterFile": "43G22.png",
                 "ImageWidth": 2000, "ImageHeight": 2000, "ActualLongitudeW": "12.500000", "ActualLatitudeS":
                     "57.240181", "ActualLongitudeE": "13.000000", "ActualLatitudeN": "57.509749",
                 "ContainerMapView_Id": 5531},
                {"Id": 55313, "Name": "43G23", "LongitudeW": "12.000000", "LatitudeS": "57.000000",
                 "LongitudeE": "12.500000", "LatitudeN": "57.250000", "Scale": "3", "RasterFile": "43G23.png",
                 "ImageWidth": 2000, "ImageHeight": 2000, "ActualLongitudeW": "12.000000", "ActualLatitudeS":
                     "56.989261", "ActualLongitudeE": "12.500000", "ActualLatitudeN": "57.260664",
                 "ContainerMapView_Id": 5531},
                {"Id": 55314, "Name": "43G24", "LongitudeW": "12.500000", "LatitudeS": "57.000000",
                 "LongitudeE": "13.000000", "LatitudeN": "57.250000", "Scale": "3", "RasterFile": "43G24.png",
                 "ImageWidth": 2000, "ImageHeight": 2000, "ActualLongitudeW": "12.500000", "ActualLatitudeS":
                     "56.989261", "ActualLongitudeE": "13.000000", "ActualLatitudeN": "57.260664",
                 "ContainerMapView_Id": 5531}
            ]
        )
        self.assertEqual(expected, actual)

    def test_get_tile_png(self):
        actual = self.DAO.get_tile_png(1)
        expected = json.dumps("1010010100111110011111010100101110111000011011101100111")
        self.assertEqual(expected, actual)
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
