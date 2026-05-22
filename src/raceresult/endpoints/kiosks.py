"""Kiosks endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.kiosk import Kiosk

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class KiosksEndpoint:
    """Kiosks (Check-In) API endpoint.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            names = await event.kiosks.names()
            kiosk = await event.kiosks.get(names[0])
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Get names of all kiosks."""
        result = await self._client.get_json(self._event_id, "kiosks/names")
        return result if result else []

    async def get(self, name: str) -> Kiosk:
        """Get a kiosk configuration by name."""
        result = await self._client.get_json(self._event_id, "kiosks/get", {"name": name})
        return Kiosk.model_validate(result)

    async def save(self, kiosk: Kiosk) -> None:
        """Save a kiosk configuration."""
        data = kiosk.model_dump(by_alias=True)
        await self._client.post_json(self._event_id, "kiosks/save", data=data)

    async def delete(self, name: str) -> None:
        """Delete a kiosk."""
        await self._client.get(self._event_id, "kiosks/delete", {"name": name})

    async def new(self, name: str) -> None:
        """Create a new kiosk."""
        await self._client.get(self._event_id, "kiosks/new", {"name": name})

    async def copy(self, name: str, new_name: str) -> None:
        """Copy a kiosk."""
        await self._client.get(self._event_id, "kiosks/copy", {"name": name, "newName": new_name})

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a kiosk."""
        await self._client.get(self._event_id, "kiosks/rename", {"name": name, "newName": new_name})
