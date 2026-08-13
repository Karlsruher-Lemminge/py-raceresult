"""Dependencies endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class DependenciesEndpoint:
    """Dependencies API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def show(self) -> str:
        """Return a string representation of the dependency tree."""
        result = await self._client.get(self._event_id, "dependencies/show")
        return result.decode("utf-8")

    async def circular_references(self) -> str:
        """Return a list of circular references in the event configuration."""
        result = await self._client.get(self._event_id, "dependencies/circularreferences")
        return result.decode("utf-8")
