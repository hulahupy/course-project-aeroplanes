import json
import os
from typing import Any, Dict, List

from src.aeroplane import Aeroplane
from src.base_storage import BaseStorage


class JSONStorage(BaseStorage):
    """Класс для сохранения информации о самолётах в JSON файл"""

    def __init__(self, filepath: str = "data/aeroplanes.json"):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        self._ensure_file_exists()

    def _ensure_file_exists(self) -> None:
        if not os.path.exists(self.filepath):
            self._save_to_file([])

    def _load_from_file(self) -> List[Dict[str, Any]]:
        """Загрузка данных из JSON файла"""
        try:
            with open(self.filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
                # Убеждаемся, что возвращаем список словарей
                if isinstance(data, list):
                    return data
                return []
        except json.JSONDecodeError, FileNotFoundError:
            return []

    def _save_to_file(self, data: List[Dict[str, Any]]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def add_aeroplane(self, aeroplane: Aeroplane) -> None:
        data = self._load_from_file()
        existing = [a for a in data if a.get("icao24") == aeroplane.icao24]
        if not existing:
            data.append(aeroplane.to_dict())
            self._save_to_file(data)

    def add_aeroplanes(self, aeroplanes: List[Aeroplane]) -> None:
        for aeroplane in aeroplanes:
            self.add_aeroplane(aeroplane)

    def get_all_aeroplanes(self) -> List[Aeroplane]:
        data = self._load_from_file()
        return [Aeroplane.from_dict(item) for item in data]

    def get_aeroplanes_by_country(self, country: str) -> List[Aeroplane]:
        data = self._load_from_file()
        filtered = [item for item in data if item.get("origin_country", "").lower() == country.lower()]
        return [Aeroplane.from_dict(item) for item in filtered]

    def get_top_by_altitude(self, n: int) -> List[Aeroplane]:
        aeroplanes = self.get_all_aeroplanes()
        with_altitude = [a for a in aeroplanes if a.geo_altitude is not None]
        sorted_aeroplanes = sorted(with_altitude, key=lambda x: x.geo_altitude or 0, reverse=True)
        return sorted_aeroplanes[:n]

    def delete_aeroplane(self, icao24: str) -> bool:
        data = self._load_from_file()
        initial_count = len(data)
        data = [item for item in data if item.get("icao24") != icao24]
        if len(data) < initial_count:
            self._save_to_file(data)
            return True
        return False

    def clear_all(self) -> None:
        self._save_to_file([])
