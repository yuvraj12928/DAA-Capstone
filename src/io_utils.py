"""Input and output helpers."""
from __future__ import annotations

import csv
import json
from pathlib import Path
from .models import Parcel


def load_parcels(path: str | Path) -> list[Parcel]:
    with open(path, newline="", encoding="utf-8") as file:
        return [Parcel(row["parcel_id"], row["destination"], int(row["weight"]), int(row["value"]), int(row["priority"]), int(row["deadline"])) for row in csv.DictReader(file)]


def load_graph(path: str | Path) -> dict[str, dict[str, float]]:
    with open(path, encoding="utf-8") as file:
        return json.load(file)
