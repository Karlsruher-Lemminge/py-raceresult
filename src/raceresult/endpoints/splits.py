"""Splits endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import Split

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class SplitsEndpoint:
    """Splits API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self, contest: int = 0) -> list[Split]:
        """Return splits for one or all contests."""
        result = await self._client.get_json(
            self._event_id, "splits/get", {"contest": contest}
        )
        return [Split.model_validate(x) for x in (result or [])]

    async def get_one(self, id: int) -> Split:
        """Return the split with the given ID."""
        result = await self._client.get_json(self._event_id, "splits/get", {"id": id})
        return Split.model_validate(result)

    async def delete(self, ids: list[int]) -> None:
        """Delete splits by ID."""
        params = {"id": ",".join(str(i) for i in ids)}
        await self._client.get(self._event_id, "splits/delete", params)

    async def save(self, items: list[Split]) -> list[int]:
        """Save splits and return their IDs."""
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "splits/save", data=data)
        return result if result else []
