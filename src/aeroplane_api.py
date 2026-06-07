from typing import Any, Dict, List, Union

import requests

from src.base_api import BaseAPI


class AeroplaneAPI(BaseAPI):
    """Класс для работы с API nominatim и opensky"""

    NOMINATIM_URL = "https://nominatim.openstreetmap.org/search"
    OPENSKY_URL = "https://opensky-network.org/api/states/all"

    def __init__(self, timeout: int = 30, test_mode: bool = True):
        self.session = requests.Session()
        self.timeout = timeout
        self.test_mode = test_mode
        self.session.headers.update({"User-Agent": "AeroplaneTracker/1.0"})

    def _get_mock_coordinates(self, country_name: str) -> Dict[str, float]:
        """Получение тестовых координат для страны"""
        mock_coords = {
            "russia": {"south": 41.0, "north": 82.0, "west": 19.0, "east": 169.0},
            "united states": {
                "south": 24.0,
                "north": 49.0,
                "west": -125.0,
                "east": -66.0,
            },
            "germany": {"south": 47.0, "north": 55.0, "west": 5.0, "east": 15.0},
            "france": {"south": 42.0, "north": 51.0, "west": -5.0, "east": 8.0},
        }

        country_lower = country_name.lower()
        for key, coords in mock_coords.items():
            if key in country_lower:
                return coords

        return {"south": -90.0, "north": 90.0, "west": -180.0, "east": 180.0}

    def _get_mock_aeroplanes(self) -> List[Dict[str, Any]]:
        """Получение тестовых данных о самолётах"""
        return [
            {
                "icao24": "abc123",
                "callsign": "AFL123",
                "origin_country": "Russia",
                "time_position": 1234567890,
                "last_contact": 1234567890,
                "longitude": 37.6176,
                "latitude": 55.7558,
                "geo_altitude": 10500.0,
                "on_ground": False,
                "velocity": 850.5,
                "true_track": 90.0,
                "vertical_rate": 0.0,
                "sensors": [],
                "baro_altitude": 10400.0,
                "transponder_code": "1234",
                "special_flag": 0,
            },
            {
                "icao24": "def456",
                "callsign": "SVO789",
                "origin_country": "Russia",
                "time_position": 1234567890,
                "last_contact": 1234567890,
                "longitude": 30.2642,
                "latitude": 59.8944,
                "geo_altitude": 11200.0,
                "on_ground": False,
                "velocity": 820.3,
                "true_track": 270.0,
                "vertical_rate": 150.0,
                "sensors": [],
                "baro_altitude": 11100.0,
                "transponder_code": "5678",
                "special_flag": 0,
            },
        ]

    def get_country_coordinates(self, country_name: str) -> Dict[str, float]:
        """Получение координат страны"""
        if self.test_mode:
            print("(Используются тестовые координаты)")
            return self._get_mock_coordinates(country_name)

        params: Dict[str, Union[str, int]] = {"q": country_name, "format": "json", "limit": 1}
        try:
            response = self.session.get(self.NOMINATIM_URL, params=params, timeout=self.timeout)
            response.raise_for_status()
            data = response.json()
            if not data:
                raise ValueError(f"Страна '{country_name}' не найдена")
            bounding_box = data[0].get("boundingbox", [])
            return {
                "south": float(bounding_box[0]),
                "north": float(bounding_box[1]),
                "west": float(bounding_box[2]),
                "east": float(bounding_box[3]),
            }
        except Exception as e:
            raise Exception(f"Ошибка при получении координат: {str(e)}")

    def get_aeroplanes_in_area(self, bounds: Dict[str, float]) -> List[Dict[str, Any]]:
        """Получение самолётов в заданной области"""
        if self.test_mode:
            print("(Используются тестовые данные о самолётах)")
            return self._get_mock_aeroplanes()

        # Реальная реализация с API...
        return []

    def get_aeroplanes_by_country(self, country_name: str) -> List[Dict[str, Any]]:
        """Получение всех самолётов в воздушном пространстве страны"""
        print(f"Получение координат для {country_name}...")
        bounds = self.get_country_coordinates(country_name)
        print("Запрос данных о самолётах...")
        return self.get_aeroplanes_in_area(bounds)
