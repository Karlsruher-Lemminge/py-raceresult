"""OverwriteValues endpoint for Raceresult API."""

from __future__ import annotations

from decimal import Decimal
from typing import TYPE_CHECKING

from raceresult.endpoints.participants import Identifier

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class OverwriteValuesEndpoint:
    """Overwrite values API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def count(
        self,
        identifier: Identifier,
        result: int = 0,
        contest: int = 0,
        filter_expr: str = "",
    ) -> int:
        """Return the number of overwrite values matching the given filters."""
        params = {
            identifier.name: identifier.value,
            "result": result,
            "contest": contest,
            "filter": filter_expr,
        }
        resp = await self._client.get_json(self._event_id, "overwritevalues/count", params)
        return int(resp)

    async def delete(
        self,
        identifier: Identifier,
        result: int = 0,
        contest: int = 0,
        filter_expr: str = "",
    ) -> None:
        """Delete overwrite values matching the given filters."""
        params = {
            identifier.name: identifier.value,
            "result": result,
            "contest": contest,
            "filter": filter_expr,
        }
        await self._client.get(self._event_id, "overwritevalues/delete", params)

    async def save(self, identifier: Identifier, result: int, value: Decimal) -> None:
        """Save an overwrite value for a participant result."""
        params = {
            identifier.name: identifier.value,
            "result": result,
            "value": str(value),
        }
        await self._client.get(self._event_id, "overwritevalues/save", params)
