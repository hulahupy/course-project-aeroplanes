from functools import total_ordering
from typing import Any, Dict, Optional


@total_ordering
class Aeroplane:
    """Класс для представления самолёта"""

    def __init__(
        self,
        callsign: str,
        origin_country: str,
        velocity: Optional[float],
        geo_altitude: Optional[float],
        icao24: str = "N/A",
        longitude: Optional[float] = None,
        latitude: Optional[float] = None,
        on_ground: bool = True,
    ):
        self._icao24 = icao24
        self._callsign = callsign
        self._origin_country = origin_country
        self._velocity = self._validate_velocity(velocity)
        self._geo_altitude = self._validate_altitude(geo_altitude)
        self._longitude = longitude
        self._latitude = latitude
        self._on_ground = on_ground

    @property
    def icao24(self) -> str:
        return self._icao24

    @property
    def callsign(self) -> str:
        return self._callsign

    @property
    def origin_country(self) -> str:
        return self._origin_country

    @property
    def velocity(self) -> Optional[float]:
        return self._velocity

    @property
    def geo_altitude(self) -> Optional[float]:
        return self._geo_altitude

    @staticmethod
    def _validate_velocity(value: Optional[float]) -> Optional[float]:
        if value is None:
            return None
        if value < 0:
            raise ValueError(f"Скорость не может быть отрицательной: {value}")
        return float(value)

    @staticmethod
    def _validate_altitude(value: Optional[float]) -> Optional[float]:
        if value is None:
            return None
        if value < -1000:
            raise ValueError(f"Высота не может быть меньше -1000: {value}")
        return float(value)

    def __eq__(self, other) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return self.velocity == other.velocity and self.geo_altitude == other.geo_altitude

    def __lt__(self, other) -> bool:
        if not isinstance(other, Aeroplane):
            return NotImplemented
        return (self.velocity or 0) < (other.velocity or 0)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Aeroplane":
        return cls(
            icao24=data.get("icao24", "N/A"),
            callsign=data.get("callsign", "N/A"),
            origin_country=data.get("origin_country", "Unknown"),
            velocity=data.get("velocity"),
            geo_altitude=data.get("geo_altitude"),
            longitude=data.get("longitude"),
            latitude=data.get("latitude"),
            on_ground=data.get("on_ground", True),
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "icao24": self.icao24,
            "callsign": self.callsign,
            "origin_country": self.origin_country,
            "velocity": self.velocity,
            "geo_altitude": self.geo_altitude,
            "longitude": self._longitude,
            "latitude": self._latitude,
            "on_ground": self._on_ground,
        }

    def __str__(self) -> str:
        return f"Aeroplane(callsign='{self.callsign}', country='{self.origin_country}', velocity={self.velocity})"
