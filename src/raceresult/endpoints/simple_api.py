"""SimpleAPI endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import SimpleAPIItem

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class SimpleAPIEndpoint:
    """SimpleAPI endpoint for managing key/URL mappings."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[SimpleAPIItem]:
        """Return all SimpleAPI entries."""
        result = await self._client.get_json(self._event_id, "simpleapi/get")
        return [SimpleAPIItem.model_validate(x) for x in (result or [])]

    async def delete(self, key: str) -> None:
        """Delete a SimpleAPI entry by key."""
        await self._client.get(self._event_id, "simpleapi/delete", {"key": key})

    async def save(self, items: list[SimpleAPIItem]) -> None:
        """Save SimpleAPI entries (merge with existing)."""
        data = [item.model_dump(by_alias=True) for item in items]
        await self._client.post_json(self._event_id, "simpleapi/save", data=data)

    async def save_all(self, items: list[SimpleAPIItem]) -> None:
        """Save SimpleAPI entries, replacing all existing entries."""
        data = [item.model_dump(by_alias=True) for item in items]
        await self._client.post_json(self._event_id, "simpleapi/saveall", data=data)
