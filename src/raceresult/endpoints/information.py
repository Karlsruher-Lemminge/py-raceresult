"""Information endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class InformationEndpoint:
    """General information / name database API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def frequent_names(self, prefix: str, max_no: int = 10) -> list[str]:
        """Return frequent first names that start with the given prefix."""
        params = {"prefix": prefix, "maxNo": max_no}
        result = await self._client.get_json(
            self._event_id, "information/frequentnames", params
        )
        return result if result else []

    async def get_sex(self, name: str) -> str:
        """Return the inferred gender for a given first name."""
        result = await self._client.get(
            self._event_id, "information/getsex", {"name": name}
        )
        return result.decode("utf-8")

    async def add_first_name(self, name: str, sex: str) -> None:
        """Add a first name with its gender to the name database."""
        params = {"name": name, "sex": sex}
        await self._client.get(self._event_id, "information/addfirstname", params)
