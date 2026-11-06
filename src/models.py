"""Data models for the Mini-Courier Planner."""
from dataclasses import dataclass

@dataclass(frozen=True)
class Parcel:
    parcel_id: str
    destination: str
    weight: int
    value: int
    priority: int
    deadline: int

@dataclass
class RouteResult:
    path: list[str]
    distance: float
