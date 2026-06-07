from abc import ABC, abstractmethod
from typing import Any, Dict, List


class BaseAPI(ABC):
    """Абстрактный класс для работы с API"""

    @abstractmethod
    def get_country_coordinates(self, country_name: str) -> Dict[str, float]:
        """
        Получение географических координат страны

        Args:
            country_name: Название страны

        Returns:
            Словарь с координатами: {'north': float, 'south': float,
                                     'east': float, 'west': float}
        """
        pass

    @abstractmethod
    def get_aeroplanes_in_area(self, bounds: Dict[str, float]) -> List[Dict[str, Any]]:
        """
        Получение информации о самолётах в заданной области

        Args:
            bounds: Границы области (north, south, east, west)

        Returns:
            Список словарей с данными о самолётах
        """
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country_name: str) -> List[Dict[str, Any]]:
        """
        Получение информации о самолётах в воздушном пространстве страны

        Args:
            country_name: Название страны

        Returns:
            Список словарей с данными о самолётах
        """
        pass
