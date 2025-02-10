import json
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from random import choice
    




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
    is_used: bool = False



