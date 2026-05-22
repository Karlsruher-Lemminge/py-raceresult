"""Certificates endpoint for Raceresult API."""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.certificate import Certificate

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class CertificatesEndpoint:
    """Certificates API endpoint."""

    def __init__(self, client: RaceResultClient, event_id: str):
        self._client = client
        self._event_id = event_id

    async def names(self) -> list[str]:
        """Return names of all certificates."""
        result = await self._client.get_json(self._event_id, "certificates/names")
        return result if result else []

    async def get(self, name: str) -> Certificate:
        """Return a certificate by name."""
        result = await self._client.get_json(
            self._event_id, "certificates/get", {"name": name}
        )
        return Certificate.model_validate(result)

    async def save(self, item: Certificate) -> None:
        """Save a certificate."""
        await self._client.post_json(
            self._event_id, "certificates/save", data=item.model_dump(by_alias=True)
        )

    async def delete(self, name: str) -> None:
        """Delete a certificate."""
        await self._client.get(self._event_id, "certificates/delete", {"name": name})

    async def copy(self, name: str, new_name: str) -> None:
        """Create a copy of a certificate."""
        await self._client.get(
            self._event_id, "certificates/copy", {"name": name, "newName": new_name}
        )

    async def rename(self, name: str, new_name: str) -> None:
        """Rename a certificate."""
        await self._client.get(
            self._event_id, "certificates/rename", {"name": name, "newName": new_name}
        )

    async def new(self, name: str) -> None:
        """Create a new certificate."""
        await self._client.get(self._event_id, "certificates/new", {"name": name})

    async def thumbnail(self, name: str, max_width: int, max_height: int) -> bytes:
        """Return a thumbnail image of a certificate."""
        params = {"name": name, "maxWidth": max_width, "maxHeight": max_height}
        return await self._client.get(self._event_id, "certificates/thumbnail", params)

    async def preview_jpg(self, name: str, page: int = 1, dpi: int = 96, lang: str = "") -> bytes:
        """Return a JPG preview of a certificate page."""
        params = {"name": name, "page": page, "dpi": dpi, "lang": lang}
        return await self._client.get(self._event_id, "certificates/previewJPG", params)

    async def create_pdf(self, name: str, page: int = 0, bib: int = 0, lang: str = "") -> bytes:
        """Render a certificate as PDF."""
        params = {"name": name, "page": page, "bib": bib, "lang": lang, "format": "pdf"}
        return await self._client.get(self._event_id, "certificates/create", params)

    async def create_jpg(
        self, name: str, page: int = 0, bib: int = 0, dpi: int = 96, lang: str = ""
    ) -> bytes:
        """Render a certificate as JPG."""
        params = {"name": name, "page": page, "bib": bib, "dpi": dpi, "lang": lang, "format": "jpg"}
        return await self._client.get(self._event_id, "certificates/create", params)
