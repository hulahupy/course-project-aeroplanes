import json
import os
import unittest

from src.api_adapter import APIAdapter


class TestAPIAdapter(unittest.TestCase):
    """Тесты для основного API адаптера"""

    def setUp(self):
        self.api = APIAdapter(test_mode=True)

    def test_get_country_coordinates(self):
        """Тест получения координат страны"""
        coords = self.api.get_country_coordinates("Russia")
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords[0], "41.0")  # south

    def test_get_aeroplanes_country_change(self):
        """Тест смены страны"""
        self.api.get_aeroplanes("Russia")
        first_country = self.api.last_country
        self.api.get_aeroplanes("Germany")
        second_country = self.api.last_country
        self.assertNotEqual(first_country, second_country)

    def test_print_aeroplanes_custom_title(self):
        """Тест вывода с пользовательским заголовком"""
        self.api.get_aeroplanes("Russia")
        try:
            self.api.print_aeroplanes(title="Тестовый заголовок")
        except Exception as e:
            self.fail(f"print_aeroplanes() с заголовком вызвал ошибку: {e}")

    def test_filter_by_country_empty_result(self):
        """Тест фильтрации по стране, которой нет в данных"""
        self.api.get_aeroplanes("Russia")
        result = self.api.filter_by_country("NonExistentCountry")
        self.assertEqual(result, [])

    def test_get_country_coordinates_invalid(self):
        """Тест получения координат для несуществующей страны"""
        coords = self.api.get_country_coordinates("InvalidCountryNameXYZ")
        self.assertEqual(len(coords), 4)
        self.assertEqual(coords[0], "-90.0")  # default south

    def test_filter_by_country(self):
        """Тест фильтрации по стране"""
        self.api.get_aeroplanes("Russia")
        us_planes = self.api.filter_by_country("United States")
        for plane in us_planes:
            self.assertEqual(plane["origin_country"], "United States")

    def test_filter_by_country_case_insensitive(self):
        """Тест фильтрации по стране (регистронезависимо)"""
        self.api.get_aeroplanes("Russia")
        result_lower = self.api.filter_by_country("russia")
        result_upper = self.api.filter_by_country("RUSSIA")
        result_capitalized = self.api.filter_by_country("Russia")
        self.assertEqual(len(result_lower), len(result_upper))
        self.assertEqual(len(result_lower), len(result_capitalized))

    def test_top_by_altitude(self):
        """Тест получения топ N по высоте"""
        self.api.get_aeroplanes("Russia")
        top = self.api.get_top_by_altitude(3)
        self.assertEqual(len(top), 3)
        altitudes = [p.get("geo_altitude", 0) for p in top]
        self.assertEqual(altitudes, sorted(altitudes, reverse=True))

    def test_top_by_altitude_n_greater_than_total(self):
        """Тест топа по высоте когда N больше количества самолётов"""
        self.api.get_aeroplanes("Russia")
        total = len(self.api.aeroplanes)
        top = self.api.get_top_by_altitude(total + 10)
        self.assertEqual(len(top), total)

    def test_get_aeroplanes(self):
        """Тест получения самолётов по стране"""
        result = self.api.get_aeroplanes("Russia")
        self.assertIsNotNone(result)
        self.assertGreater(len(result), 0)

    def test_get_aeroplanes_invalid_country(self):
        """Тест получения самолётов для несуществующей страны"""
        result = self.api.get_aeroplanes("InvalidCountryNameXYZ")
        self.assertIsNotNone(result)

    def test_get_aeroplanes_multiple_calls(self):
        """Тест нескольких вызовов get_aeroplanes для разных стран"""
        russia_planes = self.api.get_aeroplanes("Russia")
        self.assertGreater(len(russia_planes), 0)

        usa_planes = self.api.get_aeroplanes("United States")
        self.assertGreater(len(usa_planes), 0)
        self.assertEqual(len(self.api.aeroplanes), len(usa_planes))

    def test_print_statistics(self):
        """Тест вывода статистики (проверяем, что функция не падает)"""
        self.api.get_aeroplanes("Russia")
        try:
            self.api.print_statistics()
        except Exception as e:
            self.fail(f"print_statistics() вызвал ошибку: {e}")

    def test_print_aeroplanes_empty(self):
        """Тест вывода пустого списка"""
        empty_api = APIAdapter(test_mode=True)
        try:
            empty_api.print_aeroplanes()
        except Exception as e:
            self.fail(f"print_aeroplanes() вызвал ошибку: {e}")

    def test_print_aeroplanes_with_data(self):
        """Тест вывода списка самолётов"""
        self.api.get_aeroplanes("Russia")
        try:
            self.api.print_aeroplanes()
        except Exception as e:
            self.fail(f"print_aeroplanes() вызвал ошибку: {e}")

    def test_filter_by_altitude_range_no_match(self):
        """Тест фильтрации по высоте без подходящих самолётов"""
        self.api.get_aeroplanes("Russia")
        filtered = self.api.filter_by_altitude_range(20000, 30000)
        self.assertEqual(filtered, [])

    def test_filter_by_speed_range_no_match(self):
        """Тест фильтрации по скорости без подходящих самолётов"""
        self.api.get_aeroplanes("Russia")
        filtered = self.api.filter_by_speed_range(2000, 3000)
        self.assertEqual(filtered, [])

    def test_parse_aeroplanes_empty_states(self):
        """Тест парсинга пустого списка состояний"""
        result = self.api._parse_aeroplanes([])
        self.assertEqual(result, [])

    def test_parse_aeroplanes_invalid_state(self):
        """Тест парсинса некорректного состояния"""
        invalid_states = [[], [1, 2, 3], ["a", "b"]]
        for state in invalid_states:
            result = self.api._parse_aeroplanes([state])
            self.assertEqual(result, [])


class TestAPIAdapterExtra(unittest.TestCase):
    """Дополнительные тесты для API адаптера"""

    def setUp(self):
        self.api = APIAdapter(test_mode=True)
        self.api.get_aeroplanes("Russia")

    def test_top_by_speed(self):
        """Тест получения топ N по скорости"""
        top = self.api.get_top_by_speed(3)
        self.assertEqual(len(top), 3)
        speeds = [p.get("velocity", 0) for p in top]
        self.assertEqual(speeds, sorted(speeds, reverse=True))

    def test_top_by_speed_n_greater_than_total(self):
        """Тест топа по скорости когда N больше количества самолётов"""
        total = len(self.api.aeroplanes)
        top = self.api.get_top_by_speed(total + 10)
        self.assertEqual(len(top), total)

    def test_filter_by_altitude_range(self):
        """Тест фильтрации по диапазону высот"""
        filtered = self.api.filter_by_altitude_range(10000, 11000)
        for plane in filtered:
            alt = plane.get("geo_altitude", 0)
            self.assertGreaterEqual(alt, 10000)
            self.assertLessEqual(alt, 11000)

    def test_filter_by_speed_range(self):
        """Тест фильтрации по диапазону скоростей"""
        filtered = self.api.filter_by_speed_range(800, 900)
        for plane in filtered:
            speed = plane.get("velocity", 0)
            self.assertGreaterEqual(speed, 800)
            self.assertLessEqual(speed, 900)

    def test_save_and_load(self):
        """Тест сохранения и загрузки данных"""
        test_file = "data/test_aeroplanes.json"
        self.api.save_to_file(test_file)
        self.assertTrue(os.path.exists(test_file))

        new_api = APIAdapter(test_mode=False)
        new_api.load_from_file(test_file)
        self.assertIsNotNone(new_api.aeroplanes)

        # Очистка
        if os.path.exists(test_file):
            os.remove(test_file)

    def test_save_to_file_no_data(self):
        """Тест сохранения когда нет данных"""
        empty_api = APIAdapter(test_mode=True)
        test_file = "data/empty_test.json"
        empty_api.save_to_file(test_file)
        self.assertFalse(os.path.exists(test_file))

    def test_load_from_file_not_exists(self):
        """Тест загрузки из несуществующего файла"""
        api = APIAdapter(test_mode=False)
        result = api.load_from_file("nonexistent.json")
        self.assertFalse(result)

    def test_load_from_file_empty_data(self):
        """Тест загрузки из файла с пустыми данными"""
        test_file = "data/empty_aeroplanes.json"
        os.makedirs("data", exist_ok=True)
        with open(test_file, "w", encoding="utf-8") as f:
            json.dump({"aeroplanes": []}, f)

        api = APIAdapter(test_mode=False)
        result = api.load_from_file(test_file)
        self.assertTrue(result)
        self.assertEqual(api.aeroplanes, [])

        os.remove(test_file)

    def test_statistics(self):
        """Тест получения статистики"""
        stats = self.api.get_statistics()
        self.assertGreater(stats["total"], 0)
        self.assertIn("countries_count", stats)
        self.assertIn("avg_velocity", stats)

    def test_filter_by_country_no_data(self):
        """Тест фильтрации по стране без данных"""
        empty_api = APIAdapter(test_mode=True)
        result = empty_api.filter_by_country("Russia")
        self.assertEqual(result, [])

    def test_get_top_by_altitude_no_data(self):
        """Тест топа по высоте без данных"""
        empty_api = APIAdapter(test_mode=True)
        result = empty_api.get_top_by_altitude(5)
        self.assertEqual(result, [])

    def test_get_top_by_speed_no_data(self):
        """Тест топа по скорости без данных"""
        empty_api = APIAdapter(test_mode=True)
        result = empty_api.get_top_by_speed(5)
        self.assertEqual(result, [])

    def test_filter_by_altitude_range_no_data(self):
        """Тест фильтрации по высоте без данных"""
        empty_api = APIAdapter(test_mode=True)
        result = empty_api.filter_by_altitude_range(10000, 20000)
        self.assertEqual(result, [])

    def test_filter_by_speed_range_no_data(self):
        """Тест фильтрации по скорости без данных"""
        empty_api = APIAdapter(test_mode=True)
        result = empty_api.filter_by_speed_range(800, 900)
        self.assertEqual(result, [])

    def test_get_statistics_no_data(self):
        """Тест статистики без данных"""
        empty_api = APIAdapter(test_mode=True)
        stats = empty_api.get_statistics()
        self.assertEqual(stats["total"], 0)
        self.assertEqual(stats["airborne"], 0)
        self.assertEqual(stats["grounded"], 0)

    def test_multiple_country_requests(self):
        """Тест последовательных запросов для разных стран"""
        countries = ["Russia", "United States", "Germany"]
        for country in countries:
            result = self.api.get_aeroplanes(country)
            self.assertIsNotNone(result)
            self.assertIsNotNone(self.api.last_country)
