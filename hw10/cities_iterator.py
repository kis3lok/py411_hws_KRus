from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Iterator, List, Dict, Optional, Any

@dataclass
class City:
    """
    Датакласс для хранения информации о городе
    """
    name: str
    population: int
    subject: str
    district: str
    latitude: float
    longitude: float


