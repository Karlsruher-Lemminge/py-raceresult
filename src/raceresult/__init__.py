"""Python API client for Raceresult."""

from raceresult.api import RaceResultAPI, EventAPI
from raceresult.client import RaceResultClient, RaceResultError
from raceresult.models.types import RRDate, RRDateTime, RRDecimal

__version__ = "0.1.0"
__all__ = [
    # Main API
    "RaceResultAPI",
    "EventAPI",
    "RaceResultClient",
    "RaceResultError",
    # Types
    "RRDate",
    "RRDateTime",
    "RRDecimal",
]
