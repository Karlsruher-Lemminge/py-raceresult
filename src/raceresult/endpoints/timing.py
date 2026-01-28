"""Timing/ChipFile endpoint for Raceresult API.

Based on go-webapi/eventapi_chipfile.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.timing import ChipFileEntry

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class ChipFileEndpoint:
    """Chip file API endpoint.

    Based on go-webapi/eventapi_chipfile.go.

    The chip file maps transponder codes to identification strings (e.g., bib numbers).

    Example:
        async with RaceResultClient() as client:
            await client.login(api_key="...")
            chipfile = ChipFileEndpoint(client, "event123")
            entries = await chipfile.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def get(self) -> list[ChipFileEntry]:
        """Get the entire chip file.

        Based on go-webapi/eventapi_chipfile.go:22-40.

        Returns:
            List of chip file entries
        """
        content = await self._client.get(self._event_id, "chipfile/get")
        text = content.decode("utf-8")

        entries = []
        for line in text.split("\r\n"):
            parts = line.split(";")
            if len(parts) == 2:
                entries.append(
                    ChipFileEntry(
                        transponder=parts[0],
                        identification=parts[1],
                    )
                )
        return entries

    async def save(self, entries: list[ChipFileEntry]) -> None:
        """Save a new chip file.

        Based on go-webapi/eventapi_chipfile.go:43-53.

        Args:
            entries: Chip file entries to save
        """
        lines = [f"{e.transponder};{e.identification}" for e in entries]
        data = "\r\n".join(lines).encode("utf-8")
        await self._client.post(
            self._event_id,
            "chipfile/save",
            data=data,
            content_type="text/plain",
        )

    async def clear(self) -> None:
        """Clear the entire chip file.

        Based on go-webapi/eventapi_chipfile.go:56-59.
        """
        await self._client.get(self._event_id, "chipfile/clear")
