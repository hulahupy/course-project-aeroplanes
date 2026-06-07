import unittest

from src.aeroplane import Aeroplane


class TestAeroplane(unittest.TestCase):
    """Тесты для класса Aeroplane"""

    def setUp(self):
        self.aeroplane = Aeroplane(
            callsign="UAL1621", origin_country="United States", velocity=268.79, geo_altitude=10203.18
        )

    def test_creation(self):
        """Тест создания объекта"""
        self.assertEqual(self.aeroplane.callsign, "UAL1621")
        self.assertEqual(self.aeroplane.origin_country, "United States")
        self.assertEqual(self.aeroplane.velocity, 268.79)
        self.assertEqual(self.aeroplane.geo_altitude, 10203.18)

    def test_validation_negative_velocity(self):
        """Тест валидации отрицательной скорости"""
        with self.assertRaises(ValueError):
            Aeroplane("TEST", "USA", -100, 10000)

    def test_comparison(self):
        """Тест сравнения самолётов"""
        a1 = Aeroplane("A1", "USA", 100, 10000)
        a2 = Aeroplane("A2", "USA", 200, 20000)

        self.assertTrue(a1 < a2)
        self.assertTrue(a2 > a1)

    def test_to_dict(self):
        """Тест преобразования в словарь"""
        data = self.aeroplane.to_dict()
        self.assertEqual(data["callsign"], "UAL1621")
        self.assertEqual(data["origin_country"], "United States")
