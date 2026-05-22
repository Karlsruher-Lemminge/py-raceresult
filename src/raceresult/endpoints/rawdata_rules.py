"""RawDataRules endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import RawDataRule

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class RawDataRulesEndpoint:
    """Raw data rules API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self, id: int = 0, result_id: int = 0) -> list[RawDataRule]:
        """Return one or all raw data rules."""
        params = {"id": id, "resultID": result_id}
        result = await self._client.get_json(self._event_id, "rawdatarules/get", params)
        return [RawDataRule.model_validate(x) for x in (result or [])]

    async def delete(self, id: int) -> None:
        """Delete a raw data rule."""
        await self._client.get(self._event_id, "rawdatarules/delete", {"id": id})

    async def save(self, items: list[RawDataRule]) -> list[int]:
        """Save raw data rules and return their IDs."""
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "rawdatarules/save", data=data)
        return result if result else []
