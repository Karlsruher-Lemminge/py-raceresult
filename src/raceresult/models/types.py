"""Custom types for Raceresult API compatibility.

Based on:
- go-model/date/date.go
- go-model/datetime/datetime.go
- go-model/decimal/decimal.go
"""

from __future__ import annotations

from datetime import date, datetime
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
        if value in (VB_ZERO_DATE, GO_ZERO_DATE):
            return None
        return value
    if isinstance(value, str):
        if not value:
            return None
        # ISO format: YYYY-MM-DD
        try:
            parsed = date.fromisoformat(value)
            if parsed in (VB_ZERO_DATE, GO_ZERO_DATE):
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


def _is_zero_datetime(value: datetime) -> bool:
    """Whether a datetime is one of the zero values Go treats as empty.

    Mirrors go-model/datetime/datetime.go:144-149 (IsZero), which covers
    both the VB zero date 1899-12-30 and Go's own 0001-01-01 zero time.
    """
    return value.date() in (VB_ZERO_DATE, GO_ZERO_DATE) and (
        value.hour,
        value.minute,
        value.second,
    ) == (0, 0, 0)


def _parse_rr_datetime(value: Any) -> datetime | None:
    """Parse a Raceresult datetime value.

    Zoneless wire forms are returned as NAIVE datetimes on purpose. Go
    tracks this with an explicit `hasZone` flag (datetime.go:104-118) and
    re-emits such values without a zone, reinterpreting them in the event's
    timezone later. Stamping UTC on them here would silently turn an
    event-local time into a UTC instant on the next save.
    """
    if value is None or value == "":
        return None
    if isinstance(value, datetime):
        return None if _is_zero_datetime(value) else value
    if isinstance(value, str):
        if not value:
            return None
        parsed: datetime | None = None
        # RFC3339 (carries a zone) -- go datetime.go:118-123
        if "T" in value:
            try:
                parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
            except ValueError:
                parsed = None
        # Zoneless datetime: YYYY-MM-DD HH:MM:SS -- go datetime.go:111-117
        if parsed is None and " " in value and len(value) == 19:
            try:
                parsed = datetime.strptime(value, "%Y-%m-%d %H:%M:%S")
            except ValueError:
                parsed = None
        # Zoneless date only: YYYY-MM-DD -- go datetime.go:105-110
        if parsed is None and len(value) == 10:
            try:
                d = date.fromisoformat(value)
                parsed = datetime(d.year, d.month, d.day)
            except ValueError:
                parsed = None
        # European datetime: DD.MM.YYYY [HH:MM:SS]
        if parsed is None and "." in value:
            parts = value.split(" ")
            date_parts = parts[0].split(".")
            if len(date_parts) == 3:
                try:
                    d = date(int(date_parts[2]), int(date_parts[1]), int(date_parts[0]))
                    if len(parts) > 1:
                        time_parts = parts[1].split(":")
                        parsed = datetime(
                            d.year,
                            d.month,
                            d.day,
                            int(time_parts[0]),
                            int(time_parts[1]) if len(time_parts) > 1 else 0,
                            int(time_parts[2]) if len(time_parts) > 2 else 0,
                        )
                    else:
                        parsed = datetime(d.year, d.month, d.day)
                except (ValueError, IndexError):
                    parsed = None
        if parsed is not None and _is_zero_datetime(parsed):
            return None
        return parsed
    return None


def _serialize_rr_datetime(value: datetime | None) -> str:
    """Serialize a datetime to Raceresult format.

    Mirrors go-model/datetime/datetime.go:152-166 (ToString). The server
    parses datetimes with a strict length switch (datetime.go:104-131) and
    rejects anything else with "date time format not supported", so
    sub-second precision must be dropped -- Go's time.RFC3339 layout has no
    fractional part, and datetime.now() would otherwise be unsendable.
    """
    if value is None or _is_zero_datetime(value):
        return ""
    value = value.replace(microsecond=0)
    # Zoned values go out as RFC3339 -- go datetime.go:157-159
    if value.tzinfo is not None:
        return value.isoformat()
    # Zoneless midnight collapses to a bare date -- go datetime.go:160-162
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
- RFC3339 format with timezone -> aware datetime
- YYYY-MM-DD HH:MM:SS format -> NAIVE datetime (Go's hasZone=false)
- Date-only format -> naive datetime at midnight
- European formats -> naive datetime
- VB zero date (1899-12-30) and Go zero date (0001-01-01) as None

Zoneless values stay naive so they round-trip unchanged; use
:func:`align_timezone` before comparing one against an aware datetime.
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


def align_timezone(value: datetime, reference: datetime) -> datetime:
    """Make ``value`` comparable to ``reference`` the way Go does.

    Raceresult datetimes may or may not carry a timezone (see
    :func:`_parse_rr_datetime`), so a naive value and an aware one can meet
    in a comparison. Go resolves that by reading the zoneless side in the
    other side's location (go-model/datetime/datetime.go:29-41, Before),
    rather than raising as Python would.
    """
    if (value.tzinfo is None) == (reference.tzinfo is None):
        return value
    if value.tzinfo is None:
        return value.replace(tzinfo=reference.tzinfo)
    return value.astimezone(reference.tzinfo) if reference.tzinfo else value.replace(tzinfo=None)
