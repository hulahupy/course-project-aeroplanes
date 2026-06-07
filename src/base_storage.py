from abc import ABC, abstractmethod
from typing import List

from src.aeroplane import Aeroplane


class BaseStorage(ABC):
    """Абстрактный класс для хранения информации о самолётах"""

    @abstractmethod
    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        """Добавление самолёта в хранилище"""
        pass

    @abstractmethod
    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        """Добавление нескольких самолётов"""
        pass

    @abstractmethod
    def get_all_aeroplanes(self) -> List[Aeroplane]:
        """Получение всех самолётов из хранилища"""
        pass

    @abstractmethod
    def get_aeroplanes_by_country(self, country: str) -> List[Aeroplane]:
        """Получение самолётов по стране регистрации"""
        pass

    @abstractmethod
    def get_top_by_altitude(self, n: int) -> List[Aeroplane]:
        """Получение топ N самолётов по высоте"""
        pass

    @abstractmethod
    def delete_aeroplane(self, icao24: str) -> bool:
        """Удаление самолёта по ICAO24"""
        pass

    @abstractmethod
    def clear_all(self) -> None:
        """Очистка хранилища"""
        pass
