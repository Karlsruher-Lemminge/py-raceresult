"""Pictures endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class PicturesEndpoint:
    """Pictures API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self, folder: str = "") -> list[str]:
        """Return picture names in the given folder."""
        result = await self._client.get_json(
            self._event_id, "pictures/names", {"folder": folder}
        )
        return result if result else []

    async def get(self, name: str) -> bytes:
        """Return the picture with the given name."""
        return await self._client.get(self._event_id, "pictures/get", {"name": name})

    async def thumbnail(self, name: str, max_width: int, max_height: int) -> bytes:
        """Return a thumbnail of the picture."""
        params = {"name": name, "maxWidth": max_width, "maxHeight": max_height}
        return await self._client.get(self._event_id, "pictures/thumbnail", params)

    async def info(self, name: str) -> str:
        """Return metadata about the picture."""
        result = await self._client.get(self._event_id, "pictures/info", {"name": name})
        return result.decode("utf-8")

    async def delete(self, name: str) -> None:
        """Delete a picture."""
        await self._client.get(self._event_id, "pictures/delete", {"name": name})

    async def import_picture(self, folder: str, name: str, content: bytes) -> None:
        """Upload a picture."""
        params = {"folder": folder, "name": name}
        await self._client.post(self._event_id, "pictures/import", params, data=content)
