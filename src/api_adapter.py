"""
APIAdapter - модуль для работы с API Nominatim и OpenSky
"""

import json
import os
import time
from typing import Any, Dict, List, Optional

from requests import RequestException, get


class APIAdapter:
    """Адаптер для работы с API Nominatim и OpenSky"""

    def __init__(self, timeout: int = 30, retry_count: int = 3, test_mode: bool = True):
        """
        Инициализация адаптера

        Args:
            timeout: Таймаут запроса в секундах
            retry_count: Количество повторных попыток
            test_mode: Режим тестирования (без реальных запросов)
        """
        self.openstreetmap_url = "https://nominatim.openstreetmap.org/search"
        self.opensky_url = "https://opensky-network.org/api/states/all"
        self.aeroplanes: Optional[List[Dict[str, Any]]] = None
        self.timeout = timeout
        self.retry_count = retry_count
        self.test_mode = test_mode
        self.last_country: Optional[str] = None

    def _make_request_with_retry(self, url: str, params: Dict, headers: Optional[Dict] = None) -> Any:
        """Выполнение запроса с повторными попытками при ошибке"""
        for attempt in range(self.retry_count):
            try:
                response = get(url=url, params=params, headers=headers, timeout=self.timeout)
                response.raise_for_status()
                return response
            except RequestException as e:
                if attempt == self.retry_count - 1:
                    raise Exception(f"Ошибка после {self.retry_count} попыток: {str(e)}")
                print(f"Попытка {attempt + 1} не удалась. Повтор через 2 секунды...")
                time.sleep(2)

    def _get_mock_coordinates(self, country: str) -> List[str]:
        """Получение тестовых координат для страны"""
        mock_coords = {
            "russia": ["41.0", "82.0", "19.0", "169.0"],
            "united states": ["24.0", "49.0", "-125.0", "-66.0"],
            "canada": ["41.0", "83.0", "-141.0", "-52.0"],
            "germany": ["47.0", "55.0", "5.0", "15.0"],
            "france": ["42.0", "51.0", "-5.0", "8.0"],
            "spain": ["36.0", "44.0", "-9.0", "3.0"],
            "italy": ["36.0", "47.0", "6.0", "18.0"],
            "uk": ["49.0", "60.0", "-8.0", "2.0"],
            "china": ["18.0", "54.0", "73.0", "135.0"],
            "japan": ["24.0", "46.0", "122.0", "146.0"],
        }

        country_lower = country.lower()
        for key, coords in mock_coords.items():
            if key in country_lower:
                return coords

        return ["-90.0", "90.0", "-180.0", "180.0"]

    def _get_mock_aeroplanes(self) -> List[Dict[str, Any]]:
        """Получение тестовых данных о самолётах"""
        return [
            {
                "icao24": "abc123",
                "callsign": "AFL123",
                "origin_country": "Russia",
                "longitude": 37.6176,
                "latitude": 55.7558,
                "geo_altitude": 10500.0,
                "on_ground": False,
                "velocity": 850.5,
                "baro_altitude": 10400.0,
            },
            {
                "icao24": "def456",
                "callsign": "SVO789",
                "origin_country": "Russia",
                "longitude": 30.2642,
                "latitude": 59.8944,
                "geo_altitude": 11200.0,
                "on_ground": False,
                "velocity": 820.3,
                "baro_altitude": 11100.0,
            },
            {
                "icao24": "ghi789",
                "callsign": "LED456",
                "origin_country": "Russia",
                "longitude": 30.0,
                "latitude": 59.0,
                "geo_altitude": 9800.0,
                "on_ground": False,
                "velocity": 780.2,
                "baro_altitude": 9700.0,
            },
            {
                "icao24": "jkl012",
                "callsign": "UA123",
                "origin_country": "United States",
                "longitude": -118.2437,
                "latitude": 34.0522,
                "geo_altitude": 10800.0,
                "on_ground": False,
                "velocity": 890.1,
                "baro_altitude": 10700.0,
            },
            {
                "icao24": "mno345",
                "callsign": "DL456",
                "origin_country": "United States",
                "longitude": -73.9352,
                "latitude": 40.7306,
                "geo_altitude": 9500.0,
                "on_ground": False,
                "velocity": 870.4,
                "baro_altitude": 9400.0,
            },
            {
                "icao24": "pqr678",
                "callsign": "LH789",
                "origin_country": "Germany",
                "longitude": 8.6821,
                "latitude": 50.1109,
                "geo_altitude": 10200.0,
                "on_ground": False,
                "velocity": 840.7,
                "baro_altitude": 10100.0,
            },
            {
                "icao24": "stu901",
                "callsign": "AF123",
                "origin_country": "France",
                "longitude": 2.3522,
                "latitude": 48.8566,
                "geo_altitude": 9900.0,
                "on_ground": False,
                "velocity": 830.9,
                "baro_altitude": 9800.0,
            },
            {
                "icao24": "vwx234",
                "callsign": "AFL999",
                "origin_country": "Russia",
                "longitude": 37.6176,
                "latitude": 55.7558,
                "geo_altitude": 0.0,
                "on_ground": True,
                "velocity": 0.0,
                "baro_altitude": 0.0,
            },
        ]

    def get_country_coordinates(self, country: str) -> List[str]:
        """
        Получение географических координат страны

        Args:
            country: Название страны (на английском)

        Returns:
            Список координат [south, north, west, east]
        """
        self.last_country = country

        if self.test_mode:
            print(f"(Тестовый режим) Координаты для {country}: используются тестовые данные")
            return self._get_mock_coordinates(country)

        headers_nominatim = {"User-Agent": "AeroplaneTracker/2.0"}
        params_nominatim = {"q": country, "format": "json", "limit": 1}

        try:
            response = self._make_request_with_retry(
                url=self.openstreetmap_url,
                params=params_nominatim,
                headers=headers_nominatim,
            )

            data = response.json()

            if not data:
                raise ValueError(f"Страна '{country}' не найдена")

            geo_coordinates = data[0].get("boundingbox")

            if not geo_coordinates or len(geo_coordinates) != 4:
                raise ValueError(f"Не удалось получить координаты для '{country}'")

            # Явно преобразуем в список строк
            return [str(coord) for coord in geo_coordinates]

        except Exception as e:
            print(f"Ошибка при получении координат: {e}")
            print("Переключаюсь в тестовый режим...")
            self.test_mode = True
            return self._get_mock_coordinates(country)

    def get_aeroplanes_in_area(self, bounds: List[str]) -> List[Dict[str, Any]]:
        """
        Получение самолётов в заданной области

        Args:
            bounds: Список координат [south, north, west, east]

        Returns:
            Список словарей с данными о самолётах
        """
        if self.test_mode:
            print("(Тестовый режим) Используются тестовые данные о самолётах")
            return self._get_mock_aeroplanes()

        params = {
            "lamin": bounds[0],
            "lamax": bounds[1],
            "lomin": bounds[2],
            "lomax": bounds[3],
        }

        try:
            response = self._make_request_with_retry(url=self.opensky_url, params=params)
            data = response.json()
            states = data.get("states", [])
            return self._parse_aeroplanes(states)

        except Exception as e:
            print(f"Ошибка при получении данных о самолётах: {e}")
            print("Переключаюсь в тестовый режим...")
            self.test_mode = True
            return self._get_mock_aeroplanes()

    def _parse_aeroplanes(self, states: List) -> List[Dict[str, Any]]:
        """Парсинг данных о самолётах из ответа OpenSky API"""
        aeroplanes = []

        for state in states:
            if not state or len(state) < 16:
                continue

            aeroplane = {
                "icao24": state[0],
                "callsign": state[1].strip() if state[1] else "N/A",
                "origin_country": state[2],
                "time_position": state[3],
                "last_contact": state[4],
                "longitude": state[5],
                "latitude": state[6],
                "baro_altitude": state[7],
                "on_ground": state[8],
                "velocity": state[9],
                "true_track": state[10],
                "vertical_rate": state[11],
                "sensors": state[12],
                "geo_altitude": state[13],
                "transponder_code": state[14],
                "special_flag": state[15],
            }
            aeroplanes.append(aeroplane)

        return aeroplanes

    def get_aeroplanes(self, country: str) -> List[Dict[str, Any]]:
        """
        Основной метод для получения самолётов в воздушном пространстве страны

        Args:
            country: Название страны (на английском)

        Returns:
            Список словарей с данными о самолётах
        """
        print(f"\n{'=' * 50}")
        print(f"ПОИСК САМОЛЁТОВ В СТРАНЕ: {country.upper()}")
        print(f"{'=' * 50}")

        print("1. Получение координат страны...")
        coordinates = self.get_country_coordinates(country)
        print(f"   Координаты: S:{coordinates[0]}, N:{coordinates[1]}, W:{coordinates[2]}, E:{coordinates[3]}")

        print("2. Запрос данных о самолётах...")
        aeroplanes = self.get_aeroplanes_in_area(coordinates)
        print(f"   Найдено самолётов: {len(aeroplanes)}")

        self.aeroplanes = aeroplanes
        return aeroplanes

    def get_top_by_altitude(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Получение топ N самолётов по высоте

        Args:
            n: Количество самолётов в топе

        Returns:
            Список n самолётов с наибольшей высотой
        """
        if not self.aeroplanes:
            return []

        sorted_aeroplanes = sorted(self.aeroplanes, key=lambda x: x.get("geo_altitude", 0) or 0, reverse=True)

        return sorted_aeroplanes[:n]

    def get_top_by_speed(self, n: int = 10) -> List[Dict[str, Any]]:
        """
        Получение топ N самолётов по скорости

        Args:
            n: Количество самолётов в топе

        Returns:
            Список n самолётов с наибольшей скоростью
        """
        if not self.aeroplanes:
            return []

        sorted_aeroplanes = sorted(self.aeroplanes, key=lambda x: x.get("velocity", 0) or 0, reverse=True)

        return sorted_aeroplanes[:n]

    def filter_by_country(self, country: str) -> List[Dict[str, Any]]:
        """
        Фильтрация самолётов по стране регистрации

        Args:
            country: Название страны

        Returns:
            Список самолётов, зарегистрированных в указанной стране
        """
        if not self.aeroplanes:
            return []

        return [a for a in self.aeroplanes if a.get("origin_country", "").lower() == country.lower()]

    def filter_by_altitude_range(self, min_alt: float, max_alt: float) -> List[Dict[str, Any]]:
        """
        Фильтрация самолётов по диапазону высот

        Args:
            min_alt: Минимальная высота
            max_alt: Максимальная высота

        Returns:
            Список самолётов в заданном диапазоне высот
        """
        if not self.aeroplanes:
            return []

        return [
            a
            for a in self.aeroplanes
            if a.get("geo_altitude") is not None and min_alt <= a.get("geo_altitude", 0) <= max_alt
        ]

    def filter_by_speed_range(self, min_speed: float, max_speed: float) -> List[Dict[str, Any]]:
        """
        Фильтрация самолётов по диапазону скоростей

        Args:
            min_speed: Минимальная скорость
            max_speed: Максимальная скорость

        Returns:
            Список самолётов в заданном диапазоне скоростей
        """
        if not self.aeroplanes:
            return []

        return [
            a
            for a in self.aeroplanes
            if a.get("velocity") is not None and min_speed <= a.get("velocity", 0) <= max_speed
        ]

    def get_statistics(self) -> Dict[str, Any]:
        """
        Получение статистики по текущим данным о самолётах

        Returns:
            Словарь со статистическими данными
        """
        if not self.aeroplanes:
            return {
                "total": 0,
                "airborne": 0,
                "grounded": 0,
                "countries": [],
                "avg_velocity": 0,
                "max_velocity": 0,
                "min_velocity": 0,
                "avg_altitude": 0,
                "max_altitude": 0,
            }

        airborne = [a for a in self.aeroplanes if not a.get("on_ground")]
        grounded = [a for a in self.aeroplanes if a.get("on_ground")]

        velocities = [a.get("velocity", 0) for a in self.aeroplanes if a.get("velocity")]
        altitudes = [a.get("geo_altitude", 0) for a in self.aeroplanes if a.get("geo_altitude")]

        countries = list(set(a.get("origin_country", "Unknown") for a in self.aeroplanes))

        return {
            "total": len(self.aeroplanes),
            "airborne": len(airborne),
            "grounded": len(grounded),
            "countries": countries,
            "countries_count": len(countries),
            "avg_velocity": sum(velocities) / len(velocities) if velocities else 0,
            "max_velocity": max(velocities) if velocities else 0,
            "min_velocity": min(velocities) if velocities else 0,
            "avg_altitude": sum(altitudes) / len(altitudes) if altitudes else 0,
            "max_altitude": max(altitudes) if altitudes else 0,
        }

    def print_aeroplanes(self, aeroplanes: Optional[List[Dict[str, Any]]] = None, title: str = "") -> None:
        """
        Красивый вывод информации о самолётах в консоль

        Args:
            aeroplanes: Список самолётов (если None, используются все)
            title: Заголовок для вывода
        """
        if aeroplanes is None:
            aeroplanes = self.aeroplanes

        if not aeroplanes:
            print("\nСамолёты не найдены.")
            return

        if title:
            print(f"\n{'=' * 100}")
            print(f"{title}")
            print(f"{'=' * 100}")

        print(f"\n{'Позывной':<12} {'Страна':<25} {'Скорость':<10} {'Высота':<12} {'На земле':<10}")
        print("-" * 100)

        for a in aeroplanes:
            callsign = a.get("callsign", "N/A")[:12]
            country = a.get("origin_country", "Unknown")[:25]
            velocity = a.get("velocity")
            velocity_str = f"{velocity:.1f}" if isinstance(velocity, (int, float)) else "N/A"
            altitude = a.get("geo_altitude")
            altitude_str = f"{altitude:.0f}" if isinstance(altitude, (int, float)) else "N/A"
            on_ground = "Да" if a.get("on_ground") else "✈️ Нет"

            print(f"{callsign:<12} {country:<25} {velocity_str:<10} {altitude_str:<12} {on_ground:<10}")

        print("-" * 100)
        print(f"Всего: {len(aeroplanes)} самолётов")

    def print_statistics(self) -> None:
        """Вывод статистики в консоль"""
        stats = self.get_statistics()

        if stats["total"] == 0:
            print("\nНет данных для статистики.")
            return

        print(f"\n{'=' * 50}")
        print("СТАТИСТИКА ПО САМОЛЁТАМ")
        print(f"{'=' * 50}")
        print(f"Всего самолётов: {stats['total']}")
        print(f"В воздухе: {stats['airborne']}")
        print(f"На земле: {stats['grounded']}")
        print(f"Количество стран: {stats['countries_count']}")
        print(f"Страны: {', '.join(stats['countries'])}")
        print("\nСкорость:")
        print(f"   Средняя: {stats['avg_velocity']:.1f} узлов")
        print(f"   Максимальная: {stats['max_velocity']:.1f} узлов")
        print(f"   Минимальная: {stats['min_velocity']:.1f} узлов")
        print("\nВысота:")
        print(f"   Средняя: {stats['avg_altitude']:.0f} м")
        print(f"   Максимальная: {stats['max_altitude']:.0f} м")
        print(f"{'=' * 50}")

    def save_to_file(self, filename: str = "data/aeroplanes.json") -> None:
        """Сохранение данных в JSON файл"""
        if not self.aeroplanes:
            print("Нет данных для сохранения")
            return

        os.makedirs(os.path.dirname(filename), exist_ok=True)

        with open(filename, "w", encoding="utf-8") as f:
            json.dump(
                {
                    "country": self.last_country,
                    "timestamp": time.time(),
                    "count": len(self.aeroplanes),
                    "aeroplanes": self.aeroplanes,
                },
                f,
                ensure_ascii=False,
                indent=2,
            )

        print(f"Данные сохранены в файл: {filename}")

    def load_from_file(self, filename: str = "data/aeroplanes.json") -> bool:
        """Загрузка данных из JSON файла"""
        if not os.path.exists(filename):
            print(f"Файл не найден: {filename}")
            return False

        with open(filename, "r", encoding="utf-8") as f:
            data = json.load(f)
            self.aeroplanes = data.get("aeroplanes", [])
            self.last_country = data.get("country")

        print(f"Данные загружены из файла: {filename}")
        print(f"   Страна: {self.last_country}, самолётов: {len(self.aeroplanes)}")
        return True


# Пример использования
if __name__ == "__main__":
    api = APIAdapter(test_mode=True)

    # Получение самолётов
    api.get_aeroplanes("Russia")

    # Вывод всех самолётов
    api.print_aeroplanes(title="Все самолёты")

    # Топ по высоте
    top5 = api.get_top_by_altitude(5)
    api.print_aeroplanes(top5, title="Топ 5 по высоте")

    # Топ по скорости
    top3_speed = api.get_top_by_speed(3)
    api.print_aeroplanes(top3_speed, title="Топ 3 по скорости")

    # Фильтрация по стране
    us_aeroplanes = api.filter_by_country("United States")
    api.print_aeroplanes(us_aeroplanes, title="Самолёты из США")

    # Фильтрация по высоте
    high_altitude = api.filter_by_altitude_range(10000, 20000)
    api.print_aeroplanes(high_altitude, title="Самолёты на высоте 10000-20000м")

    # Статистика
    api.print_statistics()

    # Сохранение данных
    api.save_to_file()
