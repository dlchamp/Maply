from typing import NamedTuple


class Country(NamedTuple):
    """Represents a country loaded from the csv."""

    code: str
    name: str
    lat: str
    lon: str
