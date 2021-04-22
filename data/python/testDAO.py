import unittest
from data.python.DataAccessObject import MySQL_DAO
from data.python.Encoder import encode, encode_batch_dict, encode_json
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

    def test_encode_json(self):
        actual = encode_json(MMSI=123456789, Positions=[])
        expected = json.dumps(
            {
                'MMSI': 123456789,
                'Positions': []
            }
        )
        self.assertEqual(expected, actual)

    def test_encode(self):
        actual = encode(MMSI=123456789, Positions=[])
        expected = {
            'MMSI': 123456789,
            'Positions': []
            }

        self.assertEqual(expected, actual)


    def test_encode_batch_json(self):
        actual = encode_batch_dict([[901234567, 90, 12], [312342134, 13, 90]], 'MMSI', 'lat', 'long')
        expected = \
            [
                {
                    'MMSI':901234567,
                    'lat':90,
                    'long':12
                },
                {
                    'MMSI': 312342134,
                    'lat': 13,
                    'long': 90
                }
            ]

        self.assertEqual(expected, actual)
