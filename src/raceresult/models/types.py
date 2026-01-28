"""Custom types for Raceresult API compatibility.

Based on:
- go-model/date/date.go
- go-model/datetime/datetime.go
- go-model/decimal/decimal.go
"""

from __future__ import annotations

from datetime import date, datetime, timezone
from decimal import Decimal as PyDecimal
from typing import Annotated, Any, Optional

from pydantic import BeforeValidator, PlainSerializer, WithJsonSchema

# Constants
DECIMAL_PLACES = 4
DECIMAL_FACTOR = 10000

# VB Zero dates used by Raceresult
VB_ZERO_DATE = date(1899, 12, 30)
GO_ZERO_DATE = date(1, 1, 1)


def _parse_rr_date(value: Any) -> date | None:
    """Parse a Raceresult date value."""
    if value is None or value == "":
        return None
    if isinstance(value, date):
        if value == VB_ZERO_DATE or value == GO_ZERO_DATE:
            return None
        return value
    if isinstance(value, str):
        if not value:
            return None
        # ISO format: YYYY-MM-DD
        try:
            parsed = date.fromisoformat(value)
            if parsed == VB_ZERO_DATE or parsed == GO_ZERO_DATE:
                return None
            return parsed
        except ValueError:
            pass
        # European format: DD.MM.YYYY
        if "." in value:
            parts = value.split(".")
            if len(parts) == 3:
                try:
                    return date(int(parts[2]), int(parts[1]), int(parts[0]))
                except ValueError:
                    pass
    return None


def _serialize_rr_date(value: date | None) -> str:
    """Serialize a date to Raceresult format."""
    if value is None:
        return ""
    return value.isoformat()


RRDate = Annotated[
    Optional[date],
    BeforeValidator(_parse_rr_date),
    PlainSerializer(_serialize_rr_date, return_type=str),
    WithJsonSchema({"type": "string", "format": "date"}, mode="serialization"),
]
"""Raceresult Date type - compatible with Go's date.Date.

Handles:
- ISO 8601 format (YYYY-MM-DD)
- European format (DD.MM.YYYY)
- VB zero date (1899-12-30) as None
- Go zero date (0001-01-01) as None
"""


def _parse_rr_datetime(value: Any) -> datetime | None:
    """Parse a Raceresult datetime value."""
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return value
    if isinstance(value, str):
        if not value:
            return None
        # Try RFC3339 (with timezone)
        if "T" in value:
            try:
                return datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                pass
        # Try datetime format: YYYY-MM-DD HH:MM:SS
        if " " in value and len(value) == 19:
            try:
                return datetime.strptime(value, "%Y-%m-%d %H:%M:%S").replace(
                    tzinfo=timezone.utc
                )
            except ValueError:
                pass
        # Try date-only format: YYYY-MM-DD
        if len(value) == 10:
            try:
                d = date.fromisoformat(value)
                return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
            except ValueError:
                pass
        # European datetime: DD.MM.YYYY HH:MM:SS
        if "." in value:
            parts = value.split(" ")
            date_parts = parts[0].split(".")
            if len(date_parts) == 3:
                try:
                    d = date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                    if len(parts) > 1:
                        time_parts = parts[1].split(":")
                        return datetime(
                            d.year,
                            d.month,
                            d.day,
                            int(time_parts[0]),
                            int(time_parts[1]) if len(time_parts) > 1 else 0,
                            int(time_parts[2]) if len(time_parts) > 2 else 0,
                            tzinfo=timezone.utc,
                        )
                    return datetime(d.year, d.month, d.day, tzinfo=timezone.utc)
                except (ValueError, IndexError):
                    pass
    return None


def _serialize_rr_datetime(value: datetime | None) -> str:
    """Serialize a datetime to Raceresult format."""
    if value is None:
        return ""
    # Check if it's VB zero date
    if (
        value.year == 1899
        and value.month == 12
        and value.day == 30
        and value.hour == 0
        and value.minute == 0
        and value.second == 0
    ):
        return ""
    # Use RFC3339 format if timezone is set
    if value.tzinfo is not None:
        return value.isoformat()
    # Use simple format without timezone
    if value.hour == 0 and value.minute == 0 and value.second == 0:
        return value.strftime("%Y-%m-%d")
    return value.strftime("%Y-%m-%d %H:%M:%S")


RRDateTime = Annotated[
    Optional[datetime],
    BeforeValidator(_parse_rr_datetime),
    PlainSerializer(_serialize_rr_datetime, return_type=str),
    WithJsonSchema({"type": "string", "format": "date-time"}, mode="serialization"),
]
"""Raceresult DateTime type - compatible with Go's datetime.DateTime.

Handles:
- RFC3339 format with timezone
- YYYY-MM-DD HH:MM:SS format (assumed UTC)
- Date-only format
- European formats
"""


def _parse_rr_decimal(value: Any) -> PyDecimal:
    """Parse a Raceresult decimal value."""
    if value is None:
        return PyDecimal(0)
    if isinstance(value, PyDecimal):
        return value
    if isinstance(value, (int, float)):
        return PyDecimal(str(value))
    if isinstance(value, str):
        if not value:
            return PyDecimal(0)
        # Handle comma as decimal separator
        value = value.replace(",", ".")
        try:
            return PyDecimal(value)
        except Exception:
            return PyDecimal(0)
    return PyDecimal(0)


def _serialize_rr_decimal(value: PyDecimal) -> float:
    """Serialize a decimal to JSON-compatible format."""
    return float(value)


RRDecimal = Annotated[
    PyDecimal,
    BeforeValidator(_parse_rr_decimal),
    PlainSerializer(_serialize_rr_decimal, return_type=float),
    WithJsonSchema({"type": "number"}, mode="serialization"),
]
"""Raceresult Decimal type - compatible with Go's decimal.Decimal.

Go implementation uses fixed-point with 4 decimal places (factor 10000).
Python's Decimal provides arbitrary precision, which is sufficient.
"""


def decimal_from_int(value: int) -> PyDecimal:
    """Create a decimal from an integer (no decimal places)."""
    return PyDecimal(value)


def decimal_from_float(value: float) -> PyDecimal:
    """Create a decimal from a float, rounded to 4 decimal places."""
    return PyDecimal(str(round(value, DECIMAL_PLACES)))


def decimal_to_duration_seconds(value: PyDecimal) -> float:
    """Convert a Raceresult decimal time to seconds."""
    return float(value)


def duration_seconds_to_decimal(seconds: float) -> PyDecimal:
    """Convert seconds to a Raceresult decimal time."""
    return PyDecimal(str(round(seconds, DECIMAL_PLACES)))
