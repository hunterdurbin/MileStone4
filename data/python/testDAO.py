import unittest
from data.python.DataAccessObject import MySQL_DAO
import json


class DAO_Methods_UnitTest(unittest.TestCase):
    DAO = MySQL_DAO()


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
                     {"lat": "54.749385", "long": "12.841955", "IMO": 9468920},
                     {"lat": "54.749220", "long": "12.841198", "IMO": 9468920},
                     {"lat": "54.749025", "long": "12.840288", "IMO": 9468920},
                     {"lat": "54.748793", "long": "12.839228", "IMO": 9468920},
                     {"lat": "54.748630", "long": "12.838472", "IMO": 9468920}
                 ]
             }
        )
        json.dumps(expected)
        self.assertEqual(actual, expected)

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
        self.assertEqual(actual, expected)

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
