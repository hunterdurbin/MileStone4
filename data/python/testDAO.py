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
        json.dumps(expected)
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

    def test_encode(self):
        actual = encode(MMSI=123456789, Positions=[])
        expected = json.dumps(
            {
                "MMSI": 123456789,
                "Positions": []
            }
        )

        self.assertEqual(expected, actual)

    def test_encode_multiple_pos(self):
        actual = encode_multiple_pos(mmsi=902134356, positions=[[42.2141, 23.412], [41.9523, 51.124]], imo=93120)
        expected = json.dumps(
            {
                'MMSI': 902134356,
                'Positions': [
                    {'lat': 42.2141, 'long': 23.412},
                    {'lat': 41.9523, 'long': 51.124}
                ],
                'IMO': 93120
            }
        )
        self.assertEqual(expected, actual)

    def test_encode_pos(self):
        actual = encode_pos(mmsi=902134356, position=[42.2141, 23.412], imo=93120)
        expected = json.dumps(
            {
                'MMSI': 902134356,
                'lat': 42.2141,
                'long': 23.412,
                'IMO': 93120
            }
        )
        self.assertEqual(expected, actual)
