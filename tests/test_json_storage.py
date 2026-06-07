import os
import tempfile
import unittest

from src.aeroplane import Aeroplane
from src.json_storage import JSONStorage


class TestJSONStorage(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(suffix=".json", delete=False)
        self.temp_file.close()
        self.storage = JSONStorage(filepath=self.temp_file.name)

    def tearDown(self):
        if os.path.exists(self.temp_file.name):
            os.remove(self.temp_file.name)

    def test_add_and_get_aeroplane(self):
        aeroplane = Aeroplane("AFL123", "Russia", 850.5, 10500, icao24="abc123")
        self.storage.add_aeroplane(aeroplane)
        all_planes = self.storage.get_all_aeroplanes()
        self.assertEqual(len(all_planes), 1)
        self.assertEqual(all_planes[0].callsign, "AFL123")

    def test_get_by_country(self):
        a1 = Aeroplane("A1", "Russia", 100, 10000, icao24="aaa111")
        a2 = Aeroplane("A2", "USA", 200, 20000, icao24="bbb222")
        self.storage.add_aeroplanes([a1, a2])
        russian = self.storage.get_aeroplanes_by_country("Russia")
        self.assertEqual(len(russian), 1)
        self.assertEqual(russian[0].callsign, "A1")

    def test_delete_aeroplane(self):
        a1 = Aeroplane("TEST", "Russia", 100, 10000, icao24="abc123")
        self.storage.add_aeroplane(a1)
        self.assertTrue(self.storage.delete_aeroplane("abc123"))
        self.assertEqual(len(self.storage.get_all_aeroplanes()), 0)

    def test_top_by_altitude(self):
        a1 = Aeroplane("A1", "RU", 100, 5000, icao24="aaa111")
        a2 = Aeroplane("A2", "RU", 100, 15000, icao24="bbb222")
        a3 = Aeroplane("A3", "RU", 100, 10000, icao24="ccc333")
        self.storage.add_aeroplanes([a1, a2, a3])
        top = self.storage.get_top_by_altitude(2)
        self.assertEqual(len(top), 2)
        self.assertEqual(top[0].geo_altitude, 15000)
        self.assertEqual(top[1].geo_altitude, 10000)
