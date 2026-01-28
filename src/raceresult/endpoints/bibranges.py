"""Bib ranges endpoint for Raceresult API.

Based on go-webapi/eventapi_bibranges.go.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from raceresult.models.event import BibRange

if TYPE_CHECKING:
    from raceresult.client import RaceResultClient


class BibRangesEndpoint:
    """Bib Ranges API endpoint.

    Based on go-webapi/eventapi_bibranges.go.

    Example:
        async with RaceResultAPI() as api:
            await api.login(api_key="...")
            event = api.event("event123")
            ranges = await event.bibranges.get()
    """

    def __init__(self, client: RaceResultClient, event_id: str):
        """Initialize the endpoint.

        Args:
            client: HTTP client instance
            event_id: Event ID
        """
        self._client = client
        self._event_id = event_id

    async def pdf(self) -> bytes:
        """Get PDF with all bib ranges.

        Based on go-webapi/eventapi_bibranges.go:22-24.

        Returns:
            PDF file as bytes
        """
        return await self._client.get(self._event_id, "bibranges/pdf")

    async def get(self, contest: int = 0, id: int = 0) -> list[BibRange]:
        """Get bib ranges matching the given filters.

        Based on go-webapi/eventapi_bibranges.go:27-42.

        Args:
            contest: Contest ID filter (0 for all)
            id: Bib range ID filter (0 for all)

        Returns:
            List of matching bib ranges
        """
        params = {
            "contest": contest,
            "id": id,
        }
        result = await self._client.get_json(self._event_id, "bibranges/get", params)
        if not result:
            return []
        return [BibRange.model_validate(item) for item in result]

    async def delete(self, id: int) -> None:
        """Delete a bib range.

        Based on go-webapi/eventapi_bibranges.go:45-51.

        Args:
            id: Bib range ID
        """
        params = {"id": id}
        await self._client.get(self._event_id, "bibranges/delete", params)

    async def save(self, items: list[BibRange]) -> list[int]:
        """Save bib ranges.

        Based on go-webapi/eventapi_bibranges.go:54-60.

        Args:
            items: Bib ranges to save

        Returns:
            List of saved bib range IDs
        """
        data = [item.model_dump(by_alias=True) for item in items]
        result = await self._client.post_json(self._event_id, "bibranges/save", data=data)
        return result if result else []
