"""Rankings endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import Ranking

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class RankingsEndpoint:
    """Rankings API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[Ranking]:
        """Return all rankings."""
        result = await self._client.get_json(self._event_id, "ranks/get")
        return [Ranking.model_validate(x) for x in (result or [])]

    async def get_one(self, id: int) -> Ranking:
        """Return the ranking with the given ID."""
        result = await self._client.get_json(self._event_id, "ranks/get", {"id": id})
        return Ranking.model_validate(result)

    async def delete(self, id: int) -> None:
        """Delete a ranking."""
        await self._client.get(self._event_id, "ranks/delete", {"id": id})

    async def save(self, items: list[Ranking]) -> list[int]:
        """Save rankings and return their IDs."""
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "ranks/save", data=data)
        return result if result else []
